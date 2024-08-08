import os
import numpy as np
import itertools
from ..input_mocker.prop_mocker import Prop_mocker
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP, STANDARD_PREDICT_EXCITE, SPINE_SIZE_SUM_LIMIT, POST_SYNAPSE_RESOURCE_SUM
from ..mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS, APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs, POPU_ABSTRACT_DISAPPEAR_STP_INDS, GENERATIVE_POPU_ABSTRACT_APPEAR_INDS, GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS
from consts.feature import CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE, ABSTRACT_EXCITE, COMMON_ABSTRACT_TYPES_MAP, COMMON_ABSTRACT_TYPE_NAME_MAP
from consts.nerve_props import POSTERIOR_SYNAPSE_EXINFO, SPINE_EXINFO, SYNAPSE_TYPE, TYPE
from .....form_nerve.marker import Marker
from .....form_nerve.form_nerve import form_nerve
from ....regions import REGION, REGION_INDEX_MAP
from .abstract_controller import Abstract_controller
from experiments.util import get_soma_inds
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from ..mock_features1 import mock_features
from util import try_exchange_str_to_num, is_number

marker = Marker(REGION)


class Controller(Abstract_controller):

    def __init__(self, cortex_obj):
        super().__init__(cortex_obj)
        # self.form_debug_circuit_datas = {}
        # self.record_form_debug_circuit_data()
        self.predict_excite_threshold = STANDARD_PREDICT_EXCITE * .8
        self.form_intersection_citcuit_threshold = STANDARD_PREDICT_EXCITE * .6

    # def init_mock_input(self):
    #     self.prop_mocker = Prop_mocker(
    #         self.cortex_obj,
    #         self.get_soma_inds,
    #         self.get_mock_feature_list,
    #     )

    def get_input_mocker(self):
        return Prop_mocker(self.cortex_obj)

    # def get_mock_feature_list(self, mock_feature_names_list):
    #     mock_features = []
    #     for mock_feature_names in mock_feature_names_list:
    #         mock_features.extend(
    #             self.make_mock_feature_list_of_one_mnist(mock_feature_names))

    #     return mock_features

    # def make_mock_feature_list_of_one_mnist(self,
    #                                     mock_feature_names,
    #                                     mock_props_exinfo_list=[]):
    #     return [
    #         *list(
    #             itertools.chain(*[
    #                 [(
    #                     mock_feature_name,
    #                     {
    #                         **{
    #                             'play_direction': 'forward'
    #                         },
    #                         **(mock_props_exinfo_list[mock_feature_ind] if len(mock_props_exinfo_list) else {})
    #                     })] for mock_feature_ind, mock_feature_name in
    #                 enumerate(mock_feature_names)
    #             ])),
    #         *[(mock_feature_name, {
    #             **{
    #                 'play_direction': 'backward'
    #             },
    #             **(mock_props_exinfo_list[::-1][mock_feature_ind] if len(mock_props_exinfo_list) else {})
    #         }) for mock_feature_ind, mock_feature_name in enumerate(
    #             mock_feature_names[::-1])],
    #     ]

    def mock_input(self):
        self.input_mocker.mock_input()
        # if self.input_mocker.mock_data_loader.current_data.get(
        #         'play_direction') == 'forward':
        # if self.input_mocker.mock_data_loader.is_next_data_new_feature:

    # def record_form_debug_circuit_data(self):
    #     # current_data = self.input_mocker.mock_data_loader.current_data
    #     # mnist_name = current_data['mnist_name']
    #     mnist_names = list(mock_features.keys())
    #     for mnist_name in mnist_names:
    #         form_debug_circuit_data = {}
    #         self.form_debug_circuit_datas[mnist_name] = form_debug_circuit_data
    #         file_names = [
    #             file_name for file_name in os.listdir(INPUT_DIR)
    #             if file_name.startswith(mnist_name)
    #             and file_name.endswith('excite.npy')
    #         ]
    #         feature_sequence_sum = max([
    #             int(file_name.split(';')[0].split('_')[3])
    #             for file_name in file_names
    #         ]) + 1
    #         feature_sum = max([
    #             int(file_name.split(';')[0].split('_')[2])
    #             for file_name in file_names
    #         ]) + 1
    #         mnist_num = int(mnist_name.split('_')[0])
    #         for feature_sequence_ind in range(feature_sequence_sum):
    #             for feature_ind in range(feature_sum):
    #                 # for file_name in file_names:
    #                 feature_whole_name = f'{mnist_name}_{feature_ind}_{feature_sequence_ind}'
    #                 # feature_name =

    #                 if feature_sequence_ind not in form_debug_circuit_data:
    #                     form_debug_circuit_data[feature_sequence_ind] = [
    #                         mnist_num
    #                     ]

    #                 feature_infos = []
    #                 form_debug_circuit_data[feature_sequence_ind].append(
    #                     feature_infos)
    #                 excite_data = np.load(
    #                     f'{INPUT_DIR}/{feature_whole_name};excite.npy',
    #                     allow_pickle=False)
    #                 for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items(
    #                 ):
    #                     prop_inds = np.asarray([
    #                         get_soma_inds(f'属性-{abstract_type}',
    #                                       f'{abstract_name}-群体编码出现')[0]
    #                         for abstract_name, _ in abstract_values
    #                     ])
    #                     excite = excite_data[:len(prop_inds)]
    #                     excite_data = excite_data[len(prop_inds):]
    #                     max_excite_prop_argind = np.argmax(excite)
    #                     max_excite_prop_ind = prop_inds[max_excite_prop_argind]

    #                     region_info = REGION_INDEX_MAP[self.cortex['region_no']
    #                                                    [max_excite_prop_ind]]
    #                     neuron_info = region_info['neurons'][
    #                         self.cortex['neuron_no'][max_excite_prop_ind]]

    #                     feature_infos.append((
    #                         region_info['region_name'].split('-')[1],
    #                         neuron_info['name'].split('-')[0] if
    #                         ((excite[max_excite_prop_argind] >
    #                           self.cortex['RP'][max_excite_prop_ind]) and
    #                          ('无' not in neuron_info['name']
    #                           or neuron_info['name'].split('-')[0] == '朝向无'))
    #                         else None,
    #                     ))

    #                 # print(feature_infos)

    def get_generative_popu_coding_excites_with_popu_coding_excites(
            self, popu_coding_excites, is_last_feature):
        cortex = self.cortex
        popu_coding_inds = POPU_ABSTRACT_APPEAR_INDS if is_last_feature else POPU_ABSTRACT_DISAPPEAR_INDS
        generative_popu_coding_inds = GENERATIVE_POPU_ABSTRACT_APPEAR_INDS if is_last_feature else GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS

        max_excite_popu_coding_inds = popu_coding_inds[
            popu_coding_excites == ABSTRACT_EXCITE +
            cortex['RP'][popu_coding_inds]]
        single_coding_inds = [
            self.get_soma_inds(
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

    def get_popu_coding_prop_inds_list_from_mock_data(self):

        feature_names = [
            mock_data['feature_name']
            for mock_data in self.input_mocker.get_mock_data_list(
                get_content='current_mock_data')
        ]
        return [(
            np.concatenate((POPU_ABSTRACT_APPEAR_INDS,
                            GENERATIVE_POPU_ABSTRACT_APPEAR_INDS))
            if feature_ind == len(feature_names) - 1 else np.concatenate(
                (POPU_ABSTRACT_DISAPPEAR_INDS,
                 GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS))
        )[np.concatenate((
            self.input_mocker.load_props(feature_name, 'excite'),
            self.get_generative_popu_coding_excites_with_popu_coding_excites(
                self.input_mocker.load_props(feature_name, 'excite'),
                feature_ind == len(feature_names) - 1),
        )) > 0] for feature_ind, feature_name in enumerate(feature_names)]

    def get_circuit_prop_inds_list_on_a_spine(self, spine_ind):
        return list(
            self.cortex_obj.spine_circuit_map[spine_ind].values())[::-1]
        # max_LTP_link_on_spine = self.cortex_obj.get_max_LTP_link_on_spine(
        #     spine_ind)
        # max_LTP_link_on_spine = self.cortex_obj.spine_circuit_map[spine_ind]
        # if not len(max_LTP_link_on_spine):
        #     return
        # feature_sum_on_spine = int(
        #     max(self.cortex[POSTERIOR_SYNAPSE_EXINFO['feature_no']]
        #         [max_LTP_link_on_spine])) + 1
        # return [
        #     self.cortex['soma_ind'][max_LTP_link_on_spine]
        #     [self.cortex[POSTERIOR_SYNAPSE_EXINFO['feature_no']]
        #      [max_LTP_link_on_spine].astype(int) == feature_ind]
        #     for feature_ind in range(feature_sum_on_spine)
        # ]

    def get_circuit_prop_value_map_list_on_a_spine(self, spine_ind):
        circuit_prop_inds_list_on_a_spine = self.get_circuit_prop_inds_list_on_a_spine(
            spine_ind)
        return [
            self.get_prop_name_value_map_with_nerve_inds(nerve_inds)
            for nerve_inds in circuit_prop_inds_list_on_a_spine
        ]

    def get_intersection_between_two_set_list(self, set_list_0, set_list_1):
        return [
            list(set(set0).intersection(set(set1)))
            for set0, set1 in zip(set_list_0, set_list_1)
        ]

    def get_intersection_prop_value_map_list_between_nowa_feature_link_and_predict_link(
            self, predict_spine_ind):
        circuit_prop_value_map_list_on_a_spine = self.get_circuit_prop_value_map_list_on_a_spine(
            predict_spine_ind)
        input_prop_value_map_list = self.get_input_prop_name_value_map_list()

        # 初步只在长度相等的特征序列和预测回路之间求交集，后续如果有必要，再考虑长度不同的情况
        if len(input_prop_value_map_list) != len(
                circuit_prop_value_map_list_on_a_spine):
            return 'NO_SAME_LEN'

        intersection_prop_value_map_list = []
        for input_prop_value_map, circuit_prop_value_map in zip(
                input_prop_value_map_list,
                circuit_prop_value_map_list_on_a_spine):
            intersection_prop_value_map = {}
            for prop_name in circuit_prop_value_map.keys():
                intersection_value = self.get_intersection_prop_value(
                    prop_name,
                    circuit_prop_value_map[prop_name],
                    input_prop_value_map[prop_name],
                )
                if intersection_value != None:
                    intersection_prop_value_map[prop_name] = intersection_value
            intersection_prop_value_map_list.append(
                intersection_prop_value_map)

        return intersection_prop_value_map_list

    def get_intersection_prop_inds_list_between_nowa_feature_link_and_predict_link(
            self, predict_spine_ind):
        intersection_prop_value_map_list = self.get_intersection_prop_value_map_list_between_nowa_feature_link_and_predict_link(
            predict_spine_ind)
        return [[
            get_soma_inds(f'属性-{prop_name}', f'{prop_name}{prop_value}-群体编码出现')
            for prop_name, prop_value in intersection_prop_value_map.items()
        ] for intersection_prop_value_map in intersection_prop_value_map_list]

    def get_intersection_prop_value(self, prop_name, prop_value0, prop_value1):
        if not is_number(prop_value0) or not is_number(prop_value1):
            return None if prop_value0 != prop_value1 else prop_value0

        prop_info = COMMON_ABSTRACT_TYPE_NAME_MAP[prop_name]
        prop_number_values = [
            prop_value for prop_value in prop_info['values']
            if not isinstance(prop_value, str)
        ]
        prop_value_ind0 = prop_number_values.index(prop_value0)
        prop_value_ind1 = prop_number_values.index(prop_value1)
        prop_sum = len(prop_number_values)

        if not prop_info['value_recyclable']:
            intersection_prop_value_ind = int(
                (prop_value_ind0 + prop_value_ind1) / 2)
            prop_values_distance = abs(prop_value_ind0 - prop_value_ind1)
        else:
            intersection_prop_value_ind = int(
                (prop_value_ind0 + prop_value_ind1) / 2) if (
                    abs(prop_value_ind0 - prop_value_ind1) < prop_sum /
                    2) else (int(
                        (prop_value_ind0 + prop_value_ind1 + prop_sum) / 2) %
                             prop_sum)
            prop_values_distance = min(
                abs(prop_value_ind0 - prop_value_ind1),
                prop_value_ind0 + (prop_sum - prop_value_ind1),
                prop_value_ind1 + (prop_sum - prop_value_ind0),
            )

        intersection_prop_value = prop_number_values[
            intersection_prop_value_ind]

        if prop_values_distance > 4:
            intersection_prop_value = None
        elif prop_values_distance > 2:
            intersection_prop_value = f'{intersection_prop_value}-泛化'

        return intersection_prop_value

    def get_input_prop_name_value_map_list(self):
        input_excite_list = self.get_input_excite_list()
        return [
            self.get_input_prop_name_value_map(input_excites)
            for input_excites in input_excite_list
        ]

    def get_input_prop_name_value_map(self, input_excites):
        max_excite_nerve_inds = []

        def get_input_prop(prop_input_excites, prop_name, prop_values):
            if (prop_input_excites < 0).all(): return

            max_excite_nerve_inds.append(
                get_soma_inds(
                    f'属性-{prop_name}',
                    f'{prop_name}{prop_values[np.argmax(prop_input_excites)]}-个体编码出现',
                )[0])

        self.for_each_prop_input_excites(input_excites, get_input_prop)

        return self.get_prop_name_value_map_with_nerve_inds(
            max_excite_nerve_inds)

    def get_prop_name_value_map_with_nerve_inds(self, nerve_inds):
        prop_name_value_map = {}

        for nerve_ind in nerve_inds:
            prop_name = self.get_region_info_of_nerve(
                nerve_ind)['region_name'].split('-')[1]
            prop_value = self.get_neuron_info_of_nerve(
                nerve_ind)['name'].split('-')[0][len(prop_name):]
            prop_name_value_map[prop_name] = try_exchange_str_to_num(
                prop_value)

        return prop_name_value_map

    def get_region_info_of_nerve(self, nerve_ind):
        return REGION_INDEX_MAP[self.cortex['region_no'][nerve_ind]]

    def get_neuron_info_of_nerve(self, nerve_ind):
        return self.get_region_info_of_nerve(nerve_ind)['neurons'][
            self.cortex['neuron_no'][nerve_ind]]

    def for_each_prop_input_excites(self, input_excites, callback):
        excites_slice_start = 0
        for prop_type in COMMON_ABSTRACT_TYPES_MAP:
            prop_names = COMMON_ABSTRACT_TYPES_MAP[prop_type]['names']
            prop_values = COMMON_ABSTRACT_TYPES_MAP[prop_type]['values']
            for prop_name in prop_names:
                excites_slice_end = excites_slice_start + len(prop_values)
                excites = input_excites[excites_slice_start:excites_slice_end]
                excites_slice_start = excites_slice_end

                callback(excites, prop_name, prop_values)

    def get_input_excite_list(self):
        current_mock_data = self.input_mocker.mock_data_loader.current_data

        return [
            self.input_mocker.load_props(mock_data['feature_name'], 'excite')
            for mock_data in self.input_mocker.get_mock_data_list(
                get_content='current_mock_data')
            if mock_data['feature_name'].split('_')[3] ==
            current_mock_data['feature_name'].split('_')[3]
        ]

    def get_generative_popu_coding_ind(self,
                                       intersection_ind,
                                       excites,
                                       popu_coding_inds,
                                       suffix=''):
        cortex = self.cortex
        region_info = REGION_INDEX_MAP[cortex['region_no'][intersection_ind]]
        prop_name = region_info['region_name'].split('-')[1]
        prop_info = [
            info for info in COMMON_ABSTRACT_TYPES_MAP.values()
            if prop_name in info['names']
        ][0]
        prop_number_values = np.asarray([
            prop_value for prop_value in prop_info['values']
            if not isinstance(prop_value, str)
        ])
        same_prop_popu_nerve_inds = popu_coding_inds[
            cortex['region_no'][popu_coding_inds] == region_info['region_no']]
        max_excite_popu_nerve_inds = same_prop_popu_nerve_inds[np.argmax(
            excites[same_prop_popu_nerve_inds])]
        intersection_neuron_info = REGION_INDEX_MAP[
            cortex['region_no'][intersection_ind]]['neurons'][
                cortex['neuron_no'][intersection_ind]]
        max_excite_neuron_info = REGION_INDEX_MAP[
            cortex['region_no'][max_excite_popu_nerve_inds]]['neurons'][
                cortex['neuron_no'][max_excite_popu_nerve_inds]]
        prop_number_names = [
            f'{prop_name}{prop_number_value}'
            for prop_number_value in prop_number_values
        ]
        intersection_prop_name = intersection_neuron_info['name'].split('-')[0]
        max_excite_prop_name = max_excite_neuron_info['name'].split('-')[0]
        if intersection_prop_name not in prop_number_names or max_excite_prop_name not in prop_number_names:
            return None
        intersection_prop_ind = prop_number_names.index(intersection_prop_name)
        max_excite_prop_ind = prop_number_names.index(max_excite_prop_name)
        if not prop_info.get('value_recyclable', False) or abs(
            (max_excite_prop_ind -
             intersection_prop_ind)) < len(prop_number_values) / 2:
            center_prop_ind = (max_excite_prop_ind + intersection_prop_ind
                               ) // 2 % len(prop_number_names)
        else:
            center_prop_ind = (
                max_excite_prop_ind + intersection_prop_ind +
                len(prop_number_names)) // 2 % len(prop_number_names)
        center_prop_name = prop_number_names[center_prop_ind]
        center_nerve_name = f'{center_prop_name}{suffix}-{intersection_neuron_info["name"].split("-")[-1]}'

        print(
            '取泛化属性\n'
            f"[节点]{intersection_neuron_info['name']}\n",
            f'''[泛化]{center_nerve_name}\n''',
            f"[输入]{max_excite_neuron_info['name']}\n",
        )

        return get_soma_inds(region_info['region_name'], center_nerve_name)[0]

    def is_can_nerve_spike(self):
        return True
        # return self.prop.nowa_feature_exinfo[
        #     'play_direction'] == 'forward'

    # def is_can_form_synapse(self):
    #     return self.input_mocker.mock_data_loader.current_data[
    #         'play_direction'] == 'backward'

    # def is_can_weaken_synapse(self):
    #     return self.input_mocker.mock_data_loader.current_data[
    #         'play_direction'] == 'backward' and self.input_mocker.get_nowa_feature_ind(
    #         ) == 0

    def is_can_reset_cortex_props_at_cycle_end(self):
        return self.input_mocker.mock_data_loader.is_next_data_new_mnist

        # current_mock_data = self.input_mocker.mock_data_loader.current_data
        # return current_mock_data[
        #     'play_direction'] == 'backward' and current_mock_data[
        #         'feature_ind'] == 0

        # return self.input_mocker.mock_data_loader.current_data.get(
        #     'play_direction'
        # ) == 'backward' and self.input_mocker.get_nowa_feature_ind() == 0

    # def is_can_activate_dendritic_spine(self):
    #     return self.input_mocker.mock_data_loader.current_data[
    #         'play_direction'] == 'backward' and self.input_mocker.get_nowa_feature_ind(
    #         ) == 0

    def is_at_mnist_start(self):
        current_mock_data = self.input_mocker.mock_data_loader.current_data
        return current_mock_data[
            'feature_ind'] == 0 and self.input_mocker.mock_data_loader.current_data_run_tick == 0

    def is_at_mnist_end(self):
        return self.input_mocker.mock_data_loader.current_data.get(
            'play_direction'
        ) == 'backward' and self.input_mocker.get_nowa_feature_ind() == 0

    def prepare_for_form_synapse(self):
        self.cal_and_mock_predict_error()
        self.mock_number_spine_hormone_concentration()
        # self.cut_off_disappear_nerve_marker_remain()

    def cut_off_disappear_nerve_marker_remain(self):
        self.cortex_obj.write_cortex('before_cut_off')
        self.cortex['marker_remain'][POPU_ABSTRACT_DISAPPEAR_STP_INDS] /= 2
        self.cortex['dopamine_remain'][POPU_ABSTRACT_DISAPPEAR_STP_INDS] /= 2
        self.cortex_obj.write_cortex('after_cut_off')

    def cal_and_mock_predict_error(self):
        cortex_obj = self.cortex_obj
        cortex = cortex_obj.cortex

        self.mock_数字()

        # mock预测偏差兴奋
        num_input_excites = cortex['excite'][get_soma_inds('数字', 'input')]
        # cortex['excite'][PREDICT_SUPRISE_INDS] = np.maximum( SRP, num_input_excites - cortex['excite'][ACCUMULATE_PREDICT_INDS] + SRP)
        # debug 先不考虑实际预测兴奋，直接固定一个预测偏差
        cortex['excite'][PREDICT_SUPRISE_INDS] = num_input_excites

        cortex['excite'][PREDICT_BIAS_INDS] = np.maximum(
            SRP, cortex['excite'][ACCUMULATE_PREDICT_INDS] -
            num_input_excites + SRP)

        # mock预测偏差的marker_remain
        cortex_obj.set_spike_times_with_excite(PREDICT_SUPRISE_INDS)
        cortex_obj.set_spike_times_with_excite(PREDICT_BIAS_INDS)
        cortex_obj.add_marker_remain(PREDICT_SUPRISE_INDS)
        cortex_obj.add_marker_remain(PREDICT_BIAS_INDS)

        cortex_obj.write_cortex('cal_and_mock_predict_error')

    def get_active_num(self):
        return int(self.input_mocker.mock_data_loader.
                   current_data['mnist_name'].split('_')[0])

    def mock_数字(self):
        cortex_obj = self.cortex_obj
        cortex = cortex_obj.cortex
        num_input = self.get_active_num()
        # if num_input == None or num_input < 0: return

        inds_数字 = get_soma_inds('数字', 'input', num_input)
        cortex['excite'][inds_数字] = STANDARD_PREDICT_EXCITE
        # NUM_EXCITE

        # cortex_obj.vary_soma_inds.update(inds_数字)

        return inds_数字

    def mock_number_spine_hormone_concentration(self):
        cortex = self.cortex

        # mock多巴胺浓度
        # 将有预测意外的数字的树突棘上的marker_remain赋值给dopamine_remain
        cortex['dopamine_remain'][PREDICT_INDS] = cortex['marker_remain'][
            np.repeat(PREDICT_SUPRISE_INDS, SPINE_SUM_ON_A_DENDRITE)] * (
                cortex['marker_remain'][PREDICT_INDS] / 100)

        # 将dopamine_remain归一化，把树突棘的marker_remain水平拉到和预测回路上的突触一个水平
        MAX_DOPAMINE_REMAIN = 1.5
        max_dopamine_remain = np.max(cortex['dopamine_remain'][PREDICT_INDS])
        cortex['dopamine_remain'][PREDICT_INDS] *= MAX_DOPAMINE_REMAIN / (
            max_dopamine_remain or MAX_DOPAMINE_REMAIN)

        # mock血清素浓度
        cortex['seretonin_remain'][PREDICT_INDS] = cortex['marker_remain'][
            np.repeat(PREDICT_BIAS_INDS, SPINE_SUM_ON_A_DENDRITE)] * 2000

        # marker_remain不归一化，但是要把没有多巴胺的marker_remain置为0
        cortex['marker_remain'][PREDICT_INDS[cortex['dopamine_remain']
                                             [PREDICT_INDS] == 0]] = 0

    def insert_intersection_features_between_feature_link_and_circuit_on_largest_spine(
            self):

        spine_inds_of_nowa_num = self.cortex_obj.get_stable_spine_inds_of_nowa_num(
        )
        if not len(spine_inds_of_nowa_num): return

        largest_spine_ind = spine_inds_of_nowa_num[np.argmax(self.cortex[
            SPINE_EXINFO['posted_excite']][spine_inds_of_nowa_num])]

        largest_spine_circuit_length = self.cortex['max_circuit_length'][
            largest_spine_ind]

        intersection_prop_inds_list, intersection_prop_excites_list = self.get_popu_coding_intersection_between_nowa_feature_link_and_predict_link(
            largest_spine_ind)
        intersection_props_sum = len(
            list(itertools.chain(*intersection_prop_inds_list)))
        if largest_spine_circuit_length == intersection_props_sum:
            return

        print(f'{self.input_mocker.nowa_feature_name}', largest_spine_ind, [[
            self.cortex_obj.get_soma_name(intersection_prop_ind)
            for intersection_prop_ind in intersection_prop_inds
        ] for intersection_prop_inds in intersection_prop_inds_list])

        mock_exinfo_list = []
        mock_feature_names_list = get_mock_feature_names_list(
            self.input_mocker.nowa_mnist_name)[0]

        for feature_ind, [
                intersection_prop_inds,
                intersection_prop_excites,
                mock_feature_name,
        ] in enumerate(
                zip(
                    intersection_prop_inds_list,
                    intersection_prop_excites_list,
                    mock_feature_names_list,
                )):
            # popu_abstract_inds = POPU_ABSTRACT_APPEAR_INDS if feature_ind == len(
            #     intersection_prop_inds_list
            # ) - 1 else POPU_ABSTRACT_DISAPPEAR_INDS
            # self.cortex['float_util'][popu_abstract_inds] = self.cortex['RP'][
            #     popu_abstract_inds]
            # popu_abstract_mask = self.cortex['bool_util']
            # popu_abstract_mask[:] = False
            # popu_abstract_mask[intersection_prop_inds] = True
            # self.cortex['float_util'][
            #     intersection_prop_inds] = self.input_mocker.load_props(
            #         mock_feature_name,
            #         'excite')[popu_abstract_mask[popu_abstract_inds]]
            mock_exinfo_list.append({
                'mock_inds':
                intersection_prop_inds,
                'mock_excites':
                intersection_prop_excites,
                # self.cortex['float_util'][popu_abstract_inds],
                'largest_spine_ind':
                largest_spine_ind,
                'mock_file_name':
                f'{mock_feature_name}_intersection_with_spine_{largest_spine_ind}'
            })

        self.input_mocker.insert_features_into_mock_list(
            self.make_mock_feature_list_of_one_mnist(
                mock_feature_names_list,
                mock_exinfo_list,
            ))

    def on_cortex_inited(self):
        # self.reset_all_spine_size()
        pass

    def on_cortex_cycle_end(self):

        #
        self.cortex['excite'][get_soma_inds(
            '数字',
            '累积前馈预测')] = self.cortex['excite'][get_soma_inds('数字', '前馈预测')] - (
                self.cortex['excite'][get_soma_inds('数字', '前馈抑制')] -
                self.cortex['RP'][get_soma_inds('数字', '前馈抑制')])

        if self.input_mocker.mock_data_loader.is_next_data_new_mnist:
            self.cortex_obj.write_cortex('mnist_end')

            if self.is_all_num_predict_excite_below_threshold(
            ) and not self.input_mocker.is_popu_scale_reach_end():
                self.input_mocker.add_popu_scale()
                self.input_mocker.remock_nowa_mnist()
            else:
                self.input_mocker.init_popu_scale()
                self.form_new_circuit()

        # if self.is_at_mnist_end(
        # ) and not self.is_mocking_intersection_features():
        #     # self.insert_intersection_features_between_feature_link_and_its_closest_predict_link_into_mock_list()
        #     # self.insert_intersection_features_between_feature_link_and_all_no_subset_predict_link_into_mock_list()
        #     self.insert_intersection_features_between_feature_link_and_circuit_on_largest_spine(
        #     )
        #     self.resize_spine()

    def is_all_num_predict_excite_below_threshold(self):
        return (self.cortex['excite'][get_soma_inds('数字', '累积前馈预测')] <
                self.predict_excite_threshold).all()

    def form_new_circuit(self):
        if not self.is_has_fully_excite_circuit_on_nowa_num():
            self.form_full_length_circuit()
            self.form_intersection_citcuit()

    def is_has_fully_excite_circuit_on_nowa_num(self):
        current_data = self.input_mocker.mock_data_loader.current_data
        mnist_num = int(current_data['mnist_name'].split('_')[0])
        nowa_num_soma_ind = get_soma_inds('数字', '累积前馈预测', mnist_num)[0]
        return self.cortex['excite'][nowa_num_soma_ind] - self.cortex['RP'][
            nowa_num_soma_ind] == STANDARD_PREDICT_EXCITE

    def form_full_length_circuit(self):
        self.cortex_obj.form_debug_circuit()

    def form_intersection_citcuit(self):
        max_excite_spine_of_nowa_num = self.get_max_excite_spine_ind_of_nowa_num(
        )
        if not max_excite_spine_of_nowa_num: return

        max_excite = self.cortex['excite'][max_excite_spine_of_nowa_num]
        if max_excite < self.form_intersection_citcuit_threshold or max_excite == STANDARD_PREDICT_EXCITE:
            return

        intersection_prop_value_map_list = self.get_intersection_prop_value_map_list_between_nowa_feature_link_and_predict_link(
            max_excite_spine_of_nowa_num)

        if intersection_prop_value_map_list == 'NO_SAME_LEN': return

        self.cortex_obj.form_debug_circuit_with_prop_value_map_list(
            intersection_prop_value_map_list)
        print(1)

    def get_max_excite_spine_ind_of_nowa_num(self):
        current_mock_data = self.input_mocker.mock_data_loader.current_data
        mnist_num = int(current_mock_data['mnist_name'].split('_')[0])
        all_spine_inds_of_nowa_num = self.cortex_obj.get_all_spine_inds(
            [mnist_num])

        max_excite_spine_ind_of_nowa_num = all_spine_inds_of_nowa_num[
            np.argmax(self.cortex['excite'][all_spine_inds_of_nowa_num])]

        # spine的parents_info不能是当前数字
        nowa_num_parents_info = float(current_mock_data['mnist_name'].replace(
            '_', '.'))
        if self.cortex[SPINE_EXINFO['parents_info']][
                max_excite_spine_ind_of_nowa_num] != nowa_num_parents_info:
            return max_excite_spine_ind_of_nowa_num

    def on_after_form_synapse(self):
        # if self.is_can_spine_compete():
        # self.resize_spine()
        pass

    def on_after_weaken_synapse(self):
        # if not self.is_mocking_intersection_features():
        #     self.resize_spine()
        pass

    def reset_all_spine_size(self):
        self.cortex_obj.reset_cortex_single_prop_to_initial_state(
            self.cortex_obj.get_all_spine_inds(), SPINE_EXINFO['size'])

    def resize_spine(self):
        self.enlarge_spine()
        self.cortex_obj.write_cortex('enlarge_spine')
        self.shrink_spine()
        self.cortex_obj.write_cortex('shrink_spine')
        self.spine_compete()
        self.cortex_obj.write_cortex('spine_compete')

    def enlarge_spine(self):
        enlarge_spine_inds = self.cortex_obj.get_active_and_stable_spine_inds_of_nowa_num(
        )
        if not len(enlarge_spine_inds): return
        resource_limit_of_spine = self.cortex_obj.get_resource_limit_of_spine(
            enlarge_spine_inds)
        self.cortex[SPINE_EXINFO['size']][
            enlarge_spine_inds] += self.cortex['spine_active'][
                enlarge_spine_inds] / resource_limit_of_spine * POST_SYNAPSE_RESOURCE_SUM

    def shrink_spine(self):
        shrink_spine_inds = self.cortex_obj.get_active_and_stable_spine_inds_out_of_nowa_num(
        )
        if not len(shrink_spine_inds): return
        resource_limit_of_spine = self.cortex_obj.get_resource_limit_of_spine(
            shrink_spine_inds)
        self.cortex[SPINE_EXINFO['size']][
            shrink_spine_inds] -= self.cortex['spine_active'][
                shrink_spine_inds] / resource_limit_of_spine * POST_SYNAPSE_RESOURCE_SUM * 5
        np.maximum.at(self.cortex[SPINE_EXINFO['size']], shrink_spine_inds, 0)

    def spine_compete(self):
        self.cortex_obj.write_cortex('before_spine_compete')
        compete_spine_inds = self.get_compete_spine_inds()
        if len(compete_spine_inds) > 0:
            self.resize_compete_spines(compete_spine_inds)

    def get_compete_spine_inds(self):
        spine_inds_of_nowa_num = self.cortex_obj.get_spine_inds_of_nowa_num()
        return spine_inds_of_nowa_num[(
            self.cortex['excite'][spine_inds_of_nowa_num] *
            self.cortex[SPINE_EXINFO['size']][spine_inds_of_nowa_num] > 0)]

        # active_and_stable_spine_inds_of_nowa_num = self.cortex_obj.get_active_and_stable_spine_inds_of_nowa_num(
        # )

        # if len(active_and_stable_spine_inds_of_nowa_num) == 0:
        #     return []

        # compete_spine_inds = np.unique(
        #     np.concatenate(
        #         tuple([
        #             self.
        #             get_has_subset_or_super_circuit_spine_inds_compare_with_target_spine(
        #                 spine_ind)
        #             for spine_ind in active_and_stable_spine_inds_of_nowa_num
        #         ])))
        # return compete_spine_inds[
        #     self.cortex[SPINE_EXINFO['size']][compete_spine_inds] > 0]

    def get_has_subset_or_super_circuit_spine_inds_compare_with_target_spine(
            self, spine_ind):
        SPINE_IND_KEY = POSTERIOR_SYNAPSE_EXINFO['spine_ind']
        posterior_synapse_slice = self.cortex_obj.get_posterior_synapse_slice()

        single_coding_prop_inds_list_on_a_spine = self.get_circuit_prop_inds_list_on_a_spine(
            spine_ind)

        # mark_stable_spine_in_cortex
        spine_inds_of_nowa_num = self.cortex_obj.get_spine_inds_of_nowa_num()
        stable_spine_inds_of_nowa_num = spine_inds_of_nowa_num[
            self.cortex_obj.get_stable_spine_mask(spine_inds_of_nowa_num)]
        is_stable_spine_mask = self.cortex['bool_util']
        is_stable_spine_mask[:] = False
        is_stable_spine_mask[stable_spine_inds_of_nowa_num] = True

        props_count_on_spines = self.cortex['int_util']
        props_count_on_spines[:] = 0
        total_props_count = 0
        for feature_ind, prop_inds in enumerate(
                single_coding_prop_inds_list_on_a_spine):

            total_props_count += len(prop_inds)

            prop_flag = self.cortex['float_util']
            prop_flag[:] = 0
            prop_flag[prop_inds] = 1

            can_be_count_synapse_inds = self.cortex['ind'][
                posterior_synapse_slice][
                    (is_stable_spine_mask[self.cortex[SPINE_IND_KEY][
                        posterior_synapse_slice].astype(int)]) *
                    (self.cortex[POSTERIOR_SYNAPSE_EXINFO['feature_no']]
                     [posterior_synapse_slice] == feature_ind) *
                    (prop_flag[self.cortex['soma_ind']
                               [posterior_synapse_slice]] == 1) *
                    (self.cortex['LTP'][posterior_synapse_slice] > 0)]

            np.add.at(
                props_count_on_spines,
                self.cortex[SPINE_IND_KEY][can_be_count_synapse_inds].astype(
                    int),
                1,
            )

        superset_spine_inds = self.cortex['ind'][props_count_on_spines ==
                                                 total_props_count]
        subset_spine_inds = self.cortex['ind'][
            (0 < props_count_on_spines) *
            (props_count_on_spines < total_props_count)]
        subset_spine_inds = subset_spine_inds[
            self.cortex['max_circuit_length'][subset_spine_inds] ==
            props_count_on_spines[subset_spine_inds]]

        return np.concatenate((superset_spine_inds, subset_spine_inds))

    def resize_compete_spines(self, spine_inds):
        spine_excites = self.cortex['excite'][spine_inds] * self.cortex[
            SPINE_EXINFO['size']][spine_inds] / SPINE_SIZE_SUM_LIMIT
        spine_sort = np.argsort(spine_excites)
        spine_inds = spine_inds[spine_sort]
        spine_excites = spine_excites[spine_sort]
        excite_sum = np.sum(spine_excites)
        to_shrink_excite_sum = excite_sum - STANDARD_PREDICT_EXCITE
        to_shrink_size_sum = to_shrink_excite_sum / excite_sum * SPINE_SIZE_SUM_LIMIT

        if to_shrink_excite_sum <= 5:
            return

        to_shrink_ratios = spine_excites[::-1] / excite_sum
        max_shrink_sizes = spine_excites / STANDARD_PREDICT_EXCITE * SPINE_SIZE_SUM_LIMIT

        spine_sizes_to_shrink = np.zeros(len(spine_inds))
        self.make_spine_size_shrinks(to_shrink_size_sum, spine_inds,
                                     spine_sizes_to_shrink, max_shrink_sizes,
                                     to_shrink_ratios)

        self.cortex[SPINE_EXINFO['size']][spine_inds] -= spine_sizes_to_shrink

    def make_spine_size_shrinks(
        self,
        spine_size_sum_to_shrink,
        spine_inds,
        spine_sizes_to_shrink,
        max_shrink_sizes=[],
        to_shrink_ratios=[],
    ):
        max_shrink_sizes = max_shrink_sizes if len(
            max_shrink_sizes) else self.cortex[
                SPINE_EXINFO['size']][spine_inds]
        spine_sizes_to_shrink_more = spine_size_sum_to_shrink - np.sum(
            spine_sizes_to_shrink)
        if spine_sizes_to_shrink_more <= 10:
            return

        # to_shrink_ratios = to_shrink_ratios if len(
        #     to_shrink_ratios
        # ) else self.get_sorted_compete_spine_inds_and_to_shrink_ratio(
        #     spine_inds[can_shrink_spine_mask])[1]

        can_shrink_spine_mask = spine_sizes_to_shrink < max_shrink_sizes
        can_shrink_ratio_sum = sum(to_shrink_ratios[can_shrink_spine_mask])
        can_shrink_ratios = to_shrink_ratios[
            can_shrink_spine_mask] / can_shrink_ratio_sum

        spine_sizes_to_shrink[
            can_shrink_spine_mask] += spine_sizes_to_shrink_more * can_shrink_ratios
        spine_sizes_to_shrink[:] = np.minimum(spine_sizes_to_shrink,
                                              max_shrink_sizes)

        self.make_spine_size_shrinks(spine_size_sum_to_shrink, spine_inds,
                                     spine_sizes_to_shrink, max_shrink_sizes,
                                     to_shrink_ratios)

    def get_sorted_compete_spine_inds_and_to_shrink_ratio(
            self, compete_spine_inds):
        sorted_compete_spine_inds = compete_spine_inds[np.argsort(
            self.cortex[SPINE_EXINFO['size']][compete_spine_inds])]
        spine_size_sum = np.sum(
            self.cortex[SPINE_EXINFO['size']][sorted_compete_spine_inds])
        spine_size_shrink_ratios = (
            self.cortex[SPINE_EXINFO['size']][sorted_compete_spine_inds] /
            spine_size_sum)[::-1]
        return sorted_compete_spine_inds, spine_size_shrink_ratios

    def form_circuit(self):
        mother_inds = self.get_can_form_synapse_nerve_inds_sort_by_marker_remain(
        )
        father_inds = self.cortex_obj.get_has_marker_remain_spine_inds_of_nowa_num(
        ) if self.input_mocker.get_is_last_feature(
        ) else self.cortex_obj.all_marker_inds
        self.cortex_obj.all_marker_inds = []
        if len(father_inds) and len(mother_inds):
            self.form_circuit_between_nerves(mother_inds, father_inds[0])

    def form_circuit_between_nerves(self, mother_inds, father_ind):
        cortex = self.cortex
        new_nerve_inds = []

        for ind, [mother_ind, synapse_type] in enumerate(
                zip(mother_inds, cortex['exinfo_1'][mother_inds])):

            def reset_nerve_props(cortex_obj, new_nerve_slice, mother_inds,
                                  father_inds):
                # 突触后神经突的marker_exinfo1存放着预测的数字ind，需要继承下来，存在marker_exinfo1里
                cortex_obj.cortex[POSTERIOR_SYNAPSE_EXINFO['spine_ind']][
                    new_nerve_slice] = father_ind if synapse_type == SYNAPSE_TYPE[
                        'excite'] else cortex_obj.cortex[
                            POSTERIOR_SYNAPSE_EXINFO['spine_ind']][father_inds]

            new_nerve_ind = cortex['ind'][
                form_nerve.spring_nerve_packs_in_common_way(
                    self.cortex_obj,
                    [mother_ind],
                    [father_ind],
                    reset_nerve_props_lambda=reset_nerve_props,
                    is_posterior=2,
                    synapse_type=synapse_type,
                )][0]
            self.cortex['is_synapse'][new_nerve_ind] = 1
            father_ind = new_nerve_ind
            new_nerve_inds.append(new_nerve_ind)
            if ind == len(mother_inds) - 1:
                self.cortex_obj.all_marker_inds = [new_nerve_ind]

        self.cortex_obj.write_cortex('form_circuit_between_nerves')

        return new_nerve_inds

    def get_can_form_synapse_nerve_inds_sort_by_marker_remain(self):
        can_form_synapse_soma_inds = self.input_mocker.appear_and_disappear_soma_inds if self.input_mocker.mock_data_loader.current_data.get(
            'mock_inds') else np.concatenate(
                (POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS))
        can_form_synapse_soma_inds = can_form_synapse_soma_inds[
            self.cortex['marker_remain'][can_form_synapse_soma_inds] > 0]
        can_form_synapse_soma_inds = can_form_synapse_soma_inds[np.argsort(
            self.cortex['exinfo_0'][can_form_synapse_soma_inds])]
        can_form_synapse_soma_inds_group_by_prop_prime = np.split(
            can_form_synapse_soma_inds,
            np.unique(self.cortex['exinfo_0'][can_form_synapse_soma_inds],
                      return_index=True)[1][1:].astype(int))
        max_marker_remain_can_form_synapse_soma_inds_in_each_group = np.asarray(
            [
                inds_group[np.argmax(self.cortex['marker_remain'][inds_group])]
                for inds_group in
                can_form_synapse_soma_inds_group_by_prop_prime
            ])
        can_form_synapse_soma_inds_sorted_by_marker_remain = max_marker_remain_can_form_synapse_soma_inds_in_each_group[
            np.argsort(
                self.cortex['marker_remain']
                [max_marker_remain_can_form_synapse_soma_inds_in_each_group])]

        can_form_synapse_axon_inds = []
        for prop_ind, soma_ind in enumerate(
                can_form_synapse_soma_inds_sorted_by_marker_remain):
            region_name, soma_name = self.get_nerve_region_and_soma_name(
                soma_ind)
            if soma_name.endswith('出现'):
                soma_name = f'{soma_name}_A{"前馈预测" if prop_ind==0 else "易化前馈预测"}'
            elif soma_name.endswith('消失'):
                soma_name = f'{soma_name}_A{"stp预测" if prop_ind==0 else "易化stp预测"}'
            can_form_synapse_axon_inds.append(
                self.get_soma_inds(region_name, soma_name)[0])

        return can_form_synapse_axon_inds

        # can_form_synapse_nerve_inds = self.input_mocker.appear_and_disappear_axon_inds[
        #     self.cortex['marker_remain'][
        #         self.input_mocker.appear_and_disappear_axon_inds] > 0]

        def get_nerve_suffix(prop_ind, is_last_feature):
            if is_last_feature:
                if prop_ind == 0:
                    nerve_suffix = f'_A前馈预测'
                else:
                    nerve_suffix = f'_A易化前馈预测'
            else:
                if prop_ind == 0:
                    nerve_suffix = f'_Astp预测'
                else:
                    nerve_suffix = f'_A易化stp预测'

            return nerve_suffix

    def get_nerve_region_and_soma_name(self, nerve_ind):
        region_info = REGION_INDEX_MAP[self.cortex['region_no'][nerve_ind]]
        nerve_info = region_info['neurons'][self.cortex['neuron_no']
                                            [nerve_ind]]
        return region_info['region_name'], nerve_info['name']