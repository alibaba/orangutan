import os
import json
import shutil
import numpy as np
from consts import PART_PROPS_KEYS_MAP, PART_PROPS_DTYPE, PART_PROPS
from consts.experiment import APP_MODE, HISTORY_DIR, SAVE_DIR, INPUT_DIR, CORTEX_OPTS, SAVE_AND_HISTORY_SUFFIX
from consts.nerve_props import STATIC_PROP_DTYPE, TYPE, DENDRITE_TYPE, STATIC_PROP_NAMES
from consts.write_cortex import WRITE_PART_PROPS
from experiments import REGION
from util import print_exe_timecost, print_time_delta
from experiments.util import get_soma_inds


class Write_n_read_cortex():

    def __init__(self, save_and_history_suffix=SAVE_AND_HISTORY_SUFFIX):
        self.save_dir = f'{SAVE_DIR}{save_and_history_suffix}'
        self.history_dir = f'{HISTORY_DIR}{save_and_history_suffix}'
        self.init_write_cortex()

    def init_write_cortex(self):
        self.dynamic_props = WRITE_PART_PROPS
        IS_COVER_PATH = False
        self.mkdir(self.save_dir, is_cover=IS_COVER_PATH)
        self.mkdir(self.history_dir, is_cover=IS_COVER_PATH)
        self.mkdir(INPUT_DIR, is_cover=False)
        self.read_posterioir_tick = None
        self.nowa_file_name = None
        self.cortex_obj = {}
        self.cortex = {}
        self.spine_inds = []

    def init_cortex_save_data(self, cortex_obj=None):
        if cortex_obj:
            self.cortex_obj = cortex_obj
            self.cortex = cortex_obj.cortex
        self.load_cortex_save_data(save_name='save_init')
        if os.path.exists(f'{self.save_dir}/save_posterior_init'):
            self.load_cortex_save_data(save_name=f'save_posterior_init')
        self.cortex_info['write_slice_static_ind_stop'] = self.cortex_info[
            'cortex_static_part_slice_stop']
        self.soma_history_inds = self.cortex['ind'][slice(
            self.cortex_info['cortex_static_part_slice_stop'])]
        self.nerve_history_inds = self.cortex['ind'][slice(
            self.cortex_info['cortex_static_part_slice_stop'],
            self.cortex_info['cortex_slice_stop'])]

    def mkdir(self, path, is_cover):
        if is_cover:
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)
        else:
            if not os.path.exists(path):
                os.makedirs(path)

    # Write the neuron state into a json file.
    def write_cortex(self,
                     cortex_obj,
                     base_data,
                     cortex_matrix_map,
                     desc="",
                     write_mode='history',
                     suffix=''):
        tick = cortex_obj.tick
        write_cortex_tick = cortex_obj.write_cortex_tick

        if write_mode == 'save':
            write_path = f'{self.save_dir}/save_init'
        elif write_mode == 'save_posterior':
            write_path = f'{self.save_dir}/save_posterior/{write_cortex_tick}'
        elif write_mode == 'history':
            if desc == 'init':
                self.mkdir(self.history_dir, is_cover=True)
                self.mkdir(f'{self.save_dir}/save_posterior', is_cover=True)
            write_path = f'{self.history_dir}/{tick}_{write_cortex_tick};{desc};{suffix}'
        else:
            print(f'[write_cortex][no write] {desc}')
            return

        self.mkdir(write_path, is_cover=True)
        with open(f'{write_path}/meta.json', mode='w+') as file:
            file.write(
                json.dumps(base_data,
                           default=lambda o: int(o) if type(o) == np.int64 else
                           f'<not serializable>:{type(o)}'))

        for prop, prop_matrix in cortex_matrix_map.items():
            np.save(f'{write_path}/{prop}', prop_matrix, allow_pickle=False)

        print(f'[write_cortex][writed] {desc}')

    def read_cortex_history(self, req_data):
        file_name = req_data['fileName']
        if self.nowa_file_name == file_name:
            return self.history_json, self.cortex
        else:
            self.nowa_file_name = file_name
            read_posterioir_tick = file_name.split(';')[0].split('_')[1]

        # Based on the current file name, load the corresponding post-synaptic receptor.
        if CORTEX_OPTS['render_load_cortex_name'] == 'cortex_save_posterior':
            self.read_posterioir_tick = read_posterioir_tick
            self.load_cortex_save_data(
                save_name=f'save_posterior/{read_posterioir_tick}')

        with open(f'{self.history_dir}/{file_name}/meta.json',
                  mode='r') as file:
            self.history_json = json.loads(file.read())
        history_inds = CORTEX_OPTS['write_slice_lambda'](self, self.cortex,
                                                         get_soma_inds, REGION,
                                                         TYPE)
        for dynamic_prop in self.dynamic_props:
            dtype = PART_PROPS[dynamic_prop][0]
            history_cortex = np.load(
                f'{self.history_dir}/{file_name}/{dynamic_prop}.npy',
                allow_pickle=False).astype(dtype)
            self.cortex[dynamic_prop][history_inds] = history_cortex
        self.cortex_info['history_cortex_slice_stop'] = self.history_json[
            'cortex_slice_stop']
        self.cortex_info['write_slice_static_ind_stop'] = self.history_json[
            'write_slice_static_ind_stop']
        self.soma_history_inds = slice(
            history_inds.start,
            self.cortex_info['write_slice_static_ind_stop']) if isinstance(
                history_inds, slice) else history_inds[slice(
                    self.cortex_info['write_slice_static_ind_stop'])]
        self.nerve_history_inds = slice(
            self.cortex_info['write_slice_static_ind_stop'],
            history_inds.stop) if isinstance(
                history_inds, slice) else history_inds[slice(
                    self.cortex_info['write_slice_static_ind_stop'], None)]

        self.history_tick = int(file_name.split(';')[0].split('_')[0])
        self.history_write_cortex_tick = int(
            file_name.split(';')[0].split('_')[1])

        return self.history_json, self.cortex

    @print_exe_timecost()
    def load_cortex_save_data(self, save_name='save_init'):
        save_dir = self.save_dir

        with open(
                f'{save_dir}/{save_name if save_name != "save_posterior/None" else "save_init"}/meta.json',
                mode='r') as cortex_info_file:
            self.cortex_info = cortex_info = json.loads(
                cortex_info_file.read())

        if save_name == 'save_init':
            self.cortex = cortex = self.cortex or {
                prop: np.full(CORTEX_OPTS['CORTEX_W'], -1, dtype)
                for prop, dtype in PART_PROPS_DTYPE
            }
            for prop, dtype in PART_PROPS_DTYPE:
                cortex[prop][:cortex_info[
                    'cortex_static_nerves_slice_stop']] = np.load(
                        f'{save_dir}/{save_name}/{prop}.npy',
                        allow_pickle=False).astype(
                            dtype) if prop in STATIC_PROP_NAMES else np.full(
                                cortex_info['cortex_static_nerves_slice_stop'],
                                PART_PROPS[prop][1])
            self.spine_inds = self.cortex_info['spine_inds']
        elif save_name == 'save_posterior_init':
            save_posterior_inds = np.concatenate(
                (self.spine_inds,
                 np.arange(cortex_info['cortex_static_nerves_slice_stop'],
                           cortex_info['cortex_slice_stop'])))
            for prop, dtype in PART_PROPS_DTYPE:
                self.cortex[prop][save_posterior_inds] = np.load(
                    f'{save_dir}/{save_name}/{prop}.npy', allow_pickle=False
                ).astype(dtype) if prop in STATIC_PROP_NAMES else np.full(
                    len(save_posterior_inds), PART_PROPS[prop][1])
            # init_posterior_slice = slice(
            #     cortex_info['cortex_static_nerves_slice_stop'],
            #     cortex_info['cortex_slice_stop'])
            # for prop, dtype in PART_PROPS_DTYPE:
            #     self.cortex[prop][init_posterior_slice] = np.load(
            #         f'{save_dir}/{save_name}/{prop}.npy', allow_pickle=False
            #     ).astype(dtype) if prop in STATIC_PROP_NAMES else np.full(
            #         init_posterior_slice.stop -
            #         init_posterior_slice.start, PART_PROPS[prop][1])
        else:
            for prop, dtype in STATIC_PROP_DTYPE:
                self.cortex[prop][
                    cortex_info['cortex_static_nerves_slice_stop']:] = -1

                if save_name == 'save_posterior/None':
                    continue

                save_posterior_inds = np.concatenate(
                    (self.spine_inds,
                     np.arange(cortex_info['cortex_static_nerves_slice_stop'],
                               cortex_info['cortex_slice_stop'])))
                self.cortex[prop][save_posterior_inds] = np.load(
                    f'{save_dir}/{save_name}/{prop}.npy',
                    allow_pickle=False).astype(dtype)

                # self.cortex[
                #     prop][cortex_info['cortex_static_nerves_slice_stop']:
                #           cortex_info['cortex_slice_stop']] = np.load(
                #               f'{save_dir}/{save_name}/{prop}.npy',
                #               allow_pickle=False).astype(dtype)

    def get_all_history_file_name(self):
        all_history_name = list(
            set([
                os.path.splitext(file_name)[0]
                for file_name in os.listdir(self.history_dir)
                if not file_name.endswith('.json')
            ]))
        all_history_name.sort(
            key=lambda history_name: float(history_name.split(';')[0]))
        return all_history_name