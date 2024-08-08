import itertools
import numpy as np
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from ..mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS, APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs, GENERATIVE_POPU_ABSTRACT_APPEAR_INDS, GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS
from consts.feature import CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE, ABSTRACT_EXCITE, COMMON_ABSTRACT_TYPES_MAP
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from consts.nerve_props import DENDRITE_TYPE, PART_PROPS_DTYPE, PART_PROPS_MATRIX, TYPE, PART_PROPS_KEYS_MAP, RELEASE_TYPE, PART_PROPS, DYNAMIC_PROP_NAMES, STATIC_PROP_NAMES, SYNAPSE_TYPE, SPINE_EXINFO, POSTERIOR_SYNAPSE_EXINFO
from ....regions import REGION, REGION_INDEX_MAP
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP, STANDARD_PREDICT_EXCITE, SPINE_SIZE_SUM_LIMIT, POST_SYNAPSE_RESOURCE_SUM
from .abstract_mocker import Abstract_mocker
from experiments.util import get_soma_inds, get_popu_props
from ..mock_utils import get_mock_feature_names_list


class Prop_mocker(Abstract_mocker):

    def __init__(self, cortex_obj):
        super().__init__(cortex_obj, mock_data_list=self.get_mock_data_list())

        #
        self.appear_soma_inds = np.concatenate(
            (POPU_ABSTRACT_APPEAR_INDS, GENERATIVE_POPU_ABSTRACT_APPEAR_INDS))
        self.disappear_soma_inds = np.concatenate(
            (POPU_ABSTRACT_DISAPPEAR_INDS,
             GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS))
        self.appear_and_disappear_soma_inds = np.concatenate(
            (self.appear_soma_inds, self.disappear_soma_inds))
        self.appear_axon_inds = self.get_axon_inds_of_somas(
            self.appear_soma_inds)
        self.disappear_axon_inds = self.get_axon_inds_of_somas(
            self.disappear_soma_inds)
        self.appear_and_disappear_axon_inds = np.concatenate(
            (self.appear_axon_inds, self.disappear_axon_inds))
        self.appear_nerve_inds = np.concatenate(
            (self.appear_soma_inds, self.appear_axon_inds))
        self.disappear_nerve_inds = np.concatenate(
            (self.disappear_soma_inds, self.disappear_axon_inds))
        self.appear_and_disappear_nerve_inds = np.concatenate(
            (self.appear_nerve_inds, self.disappear_nerve_inds))

        self.init_popu_scale()

    def get_mock_data_list(self, get_content='all'):

        def get_common_data(mock_feature_ind, mock_feature_names):
            mock_feature_name = mock_feature_names[mock_feature_ind]
            return {
                'mnist_name': '_'.join(mock_feature_name.split('_')[:2]),
                'feature_name': mock_feature_name,
                'feature_ind': mock_feature_ind,
                'is_last_feature':
                mock_feature_ind == len(mock_feature_names) - 1,
            }

        if get_content == 'all':
            mnist_names = CORTEX_OPTS['MNIST_INPUTS_LIST']
            mock_feature_names_list = get_mock_feature_names_list(mnist_names)
        else:
            current_mock_data = self.mock_data_loader.current_data
            mnist_names = [current_mock_data['mnist_name']]
            feature_sequence_ind = int(
                current_mock_data['feature_name'].split('_')[3])
            mock_feature_names_list = get_mock_feature_names_list(mnist_names)
            mock_feature_names_list = [
                mock_feature_names_list[feature_sequence_ind]
            ]

        mock_data_list = []

        for mnist_ind, mock_feature_names in enumerate(
                mock_feature_names_list):
            mock_data_list.extend([
                *[({
                    'run_tick_sum': 1,
                    'play_direction': 'forward',
                    **get_common_data(mock_feature_ind, mock_feature_names),
                }) for mock_feature_ind, mock_feature_name in enumerate(
                    mock_feature_names)],
            ])

        return mock_data_list

    def remock_nowa_mnist(self):
        self.mock_data_loader.insert_mock_data(
            self.get_mock_data_list(get_content='get_mock_data_list'))

    def mock_input(self):
        # if not self.is_remock_input:
        self.mock_data_loader.load_next_mock_data()
        self.cortex_obj.mock_file_name = self.mock_data_loader.get_current_feature_name(
        )

        self.mock_props_appear_and_disappear()
        # if not self.is_mocking_intersection_features():
        #     self.mock_generative_popu_coding_appear_or_disappear()
        self.mock_grid_excite()
        self.cortex_obj.write_cortex('mock_input')

    def add_popu_scale(self):
        self.popu_scale += 1
        # self.is_remock_input = True

    def init_popu_scale(self):
        self.popu_scale = 5
        # self.is_remock_input = False

    def is_popu_scale_reach_end(self):
        return self.popu_scale > 7

    def is_mocking_intersection_features(self):
        return self.mock_data_loader.current_data.get('mock_file_name') != None

    def get_nowa_feature_ind(self):
        return self.mock_data_loader.current_data['feature_ind']

    def get_is_last_feature(self):
        return self.get_nowa_feature_ind() == len(
            get_mock_feature_names_list(
                [self.mock_data_loader.current_data['mnist_name']])[0]) - 1

    def get_is_first_feature(self):
        return self.get_nowa_feature_ind() == 0

    def get_mock_nerve_suffixs(self):
        return APPEAR_NERVE_SUFFIXs if self.get_is_last_feature(
        ) else DISAPPEAR_NERVE_SUFFIXs

    def load_props(self, feature_name, prop_name):
        return np.load(f'{INPUT_DIR}/{feature_name};{prop_name}.npy',
                       allow_pickle=False)

    def mock_props_appear_and_disappear(self):
        cortex_obj = self.cortex_obj
        cortex = self.cortex
        nowa_feature_data = self.mock_data_loader.current_data
        feature_name = nowa_feature_data['feature_name']
        # # 第0个序列是实际观察序列
        # feature_name += '_0'

        # # 对每个特征的抽象细胞建立或强化突触前，都要将is_new_synapse置为0
        # # 避免之前的特征的抽象细胞建立或强化突触后，将is_new_synapse变为1，导致当前特征的抽象细胞无法正常建立或强化突触
        # # cortex['is_new_synapse'][:] = 0
        # cortex['is_synapse'][cortex['is_synapse'] == 2] = 1

        # mock属性的excite
        if nowa_feature_data.get('mock_excites'):
            mock_soma_inds = nowa_feature_data.get('mock_inds')
        else:
            mock_soma_inds = self.appear_soma_inds
            single_coding_excites = self.load_props(
                feature_name,
                'excite') + 65 + self.cortex['RP'][POPU_ABSTRACT_APPEAR_INDS]
            load_popu_excites = self.get_popu_coding_from_single_coding(
                single_coding_excites, self.popu_scale)
            # load_popu_excites = self.load_props(feature_name, 'excite')
            # generative_load_popu_excites = self.get_generative_popu_coding_excites_with_popu_coding_excites(
            #     load_popu_excites, 'appear')
            generative_load_popu_excites = self.get_popu_coding_from_single_coding(
                single_coding_excites, self.popu_scale + 2)
            mock_soma_excites = np.concatenate(
                (load_popu_excites, generative_load_popu_excites))

            is_not_first_feature = nowa_feature_data['feature_ind'] > 0
            if is_not_first_feature:
                prev_feature_name = self.mock_data_loader.prev_data[
                    'feature_name']
                mock_soma_inds = np.concatenate(
                    (mock_soma_inds, self.disappear_soma_inds))

                prev_single_coding_excites = self.load_props(
                    prev_feature_name, 'excite'
                ) + 65 + self.cortex['RP'][POPU_ABSTRACT_DISAPPEAR_INDS]
                prev_load_popu_excites = self.get_popu_coding_from_single_coding(
                    prev_single_coding_excites, self.popu_scale)
                prev_generative_load_popu_excites = self.get_popu_coding_from_single_coding(
                    prev_single_coding_excites, self.popu_scale + 2)
                # prev_generative_load_popu_excites = self.get_generative_popu_coding_excites_with_popu_coding_excites(
                #     prev_load_popu_excites, 'disappear')
                mock_soma_excites = np.concatenate(
                    (mock_soma_excites, prev_load_popu_excites,
                     prev_generative_load_popu_excites))

        mock_axon_inds = self.get_axon_inds_of_somas(mock_soma_inds)

        # mock兴奋
        cortex['excite'][self.appear_and_disappear_nerve_inds] = cortex['RP'][[
            self.appear_and_disappear_nerve_inds
        ]]
        self.cortex['excite'][mock_soma_inds] = mock_soma_excites
        self.cortex['excite'][self.appear_and_disappear_axon_inds] = cortex[
            'excite'][cortex['pre_ind'][self.appear_and_disappear_axon_inds]]
        self.cortex_obj.vary_soma_inds = set(
            self.appear_and_disappear_soma_inds)

        # mock属性的tick_spike_times
        mock_nerve_inds = [*mock_soma_inds, *mock_axon_inds]
        self.cortex_obj.set_spike_times_with_excite(mock_nerve_inds)

        # 直接用tick_spike_times来计算marker_remain
        cortex['marker_remain'][self.appear_and_disappear_nerve_inds] = 0
        cortex_obj.add_marker_remain(mock_nerve_inds)

    def get_popu_coding_from_single_coding(self,
                                           single_coding_excites,
                                           popu_scale=5):
        popu_coding_from_single_coding = self.cortex['float_util']
        popu_coding_from_single_coding[
            POPU_ABSTRACT_APPEAR_INDS] = self.cortex['RP'][
                POPU_ABSTRACT_APPEAR_INDS]

        for prop_type in COMMON_ABSTRACT_TYPES_MAP:
            prop_values = COMMON_ABSTRACT_TYPES_MAP[prop_type]['values']
            prop_names = COMMON_ABSTRACT_TYPES_MAP[prop_type]['names']
            for prop_name in prop_names:
                prop_inds = np.asarray([
                    get_soma_inds(
                        f'属性-{prop_name}',
                        f'{prop_name}{prop_value}-个体编码出现',
                    )[0] for prop_value in prop_values
                ])
                excites = single_coding_excites[:len(prop_inds)]
                single_coding_excites = single_coding_excites[len(prop_inds):]
                max_excite_prop_argind = np.argmax(excites)

                max_prop_value = prop_values[max_excite_prop_argind]

                popu_props = get_popu_props(prop_type, max_prop_value,
                                            popu_scale)

                popu_coding_inds = np.asarray([
                    get_soma_inds(
                        f'属性-{prop_name}',
                        f'{prop_name}{popu_coding_value}-群体编码出现',
                    )[0] for _, popu_coding_value, _ in popu_props
                ])
                popu_coding_from_single_coding[popu_coding_inds] += np.asarray(
                    [(np.max(excites) - self.cortex['RP'][popu_coding_ind]) *
                     axon_end_release_sum_ratio
                     for popu_coding_ind, (_, _, axon_end_release_sum_ratio) in
                     zip(popu_coding_inds, popu_props)])

        return popu_coding_from_single_coding[POPU_ABSTRACT_APPEAR_INDS]

    def get_generative_popu_coding_excites_with_popu_coding_excites(
            self, popu_coding_excites, appear_or_disappear):
        cortex = self.cortex
        popu_coding_inds, generative_popu_coding_inds = {
            'appear':
            (POPU_ABSTRACT_APPEAR_INDS, GENERATIVE_POPU_ABSTRACT_APPEAR_INDS),
            'disappear': (POPU_ABSTRACT_DISAPPEAR_INDS,
                          GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS),
        }[appear_or_disappear]

        max_excite_popu_coding_inds = popu_coding_inds[
            popu_coding_excites == ABSTRACT_EXCITE +
            cortex['RP'][popu_coding_inds]]
        single_coding_inds = [
            get_soma_inds(
                REGION_INDEX_MAP[cortex['region_no']
                                 [popu_coding_ind]]['region_name'],
                REGION_INDEX_MAP[cortex['region_no'][popu_coding_ind]]
                ['neurons'][cortex['neuron_no']
                            [popu_coding_ind]]['name'].replace('群体编码', '个体编码'),
            )[0] for popu_coding_ind in max_excite_popu_coding_inds
        ]
        mock_post_excite = cortex['float_util']
        mock_post_excite[:] = SRP
        mock_post_excite[single_coding_inds] += ABSTRACT_EXCITE
        spike_axon_end_inds = cortex['ind'][
            (mock_post_excite[cortex['pre_ind']] > 0) *
            (cortex['type'] == TYPE['axon_end'])]
        mock_post_excite[cortex['post_ind'][cortex['post_ind'][
            spike_axon_end_inds]]] += ABSTRACT_EXCITE * cortex[
                'transmitter_release_sum'][
                    spike_axon_end_inds] / -cortex['RP'][spike_axon_end_inds]

        return mock_post_excite[generative_popu_coding_inds]

    def get_axon_inds_of_somas(self, soma_ind):
        cortex = self.cortex
        soma_mask = cortex['bool_util']
        soma_mask[:] = False
        soma_mask[soma_ind] = True
        return cortex['ind'][(cortex['type'] == TYPE['axon']) *
                             soma_mask[cortex['pre_ind']]]

    def mock_grid_excite(self):
        cortex = self.cortex
        feature_name = self.mock_data_loader.current_data['feature_name']

        # mock网格位置
        cortex['excite'][NOWA_FEATURE_GRID_INDS] = self.load_props(
            feature_name, 'grid')
        cortex['excite'][WHOLE_CENTER_GRID_INDS] = self.load_props(
            feature_name, 'whole_center_grid')