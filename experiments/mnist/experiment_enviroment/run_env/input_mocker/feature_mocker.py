import numpy as np
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from ..mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS, APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs, GENERATIVE_POPU_ABSTRACT_APPEAR_INDS, GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS
from consts.base import IMG_PATH
from consts.feature import CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE, ABSTRACT_EXCITE
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from consts.nerve_props import DENDRITE_TYPE, PART_PROPS_DTYPE, PART_PROPS_MATRIX, TYPE, PART_PROPS_KEYS_MAP, RELEASE_TYPE, PART_PROPS, DYNAMIC_PROP_NAMES, STATIC_PROP_NAMES, SYNAPSE_TYPE, SPINE_EXINFO, POSTERIOR_SYNAPSE_EXINFO
from ....regions import REGION, REGION_INDEX_MAP
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP, STANDARD_PREDICT_EXCITE, SPINE_SIZE_SUM_LIMIT, POST_SYNAPSE_RESOURCE_SUM
from experiments.util import get_soma_inds
import itertools
from ..mock_features1 import mock_features
from .abstract_mocker import Abstract_mocker


class Feature_mocker(Abstract_mocker):

    def __init__(self, cortex_obj):
        super().__init__(cortex_obj, mock_data_list=self.get_mock_data_list())

    def get_mock_data_list(self):
        return [
            {
                'mnist_name': mnist_name,
                'feature_ind': feature_ind,
                'whole_center_data': feature_datas[0],
                'run_tick_sum': 7,
                'feature_data': feature_data,
                'is_last_feature': feature_ind == len(feature_sequence) - 1,
                'feature_sequence_ind': feature_sequence_ind,
            }
            for mnist_ind, (mnist_name,
                            feature_datas) in enumerate(mock_features.items())
            for feature_sequence_ind, feature_sequence in enumerate(
                itertools.permutations(feature_datas[1:],
                                       len(feature_datas) - 1))
            for feature_ind, feature_data in enumerate(feature_sequence)
        ]

    def mock_input(self):
        ''' mock_data:
        {
            'mnist_name': '0_27',
            'feature_ind': 0,
            'whole_center_data': 整体轮廓的信息
            'run_tick_sum': 7,
            'feature_data': {},
            'is_last_feature': False,
            'row_ind': 15,
            'col_ind': 14,
            'region_name': '轮廓中心',
            'neuron_name': '整体轮廓中心',
            'scale': 19,
            'contour_center_open_angle': 0,
        },
        '''
        self.mock_data_loader.load_next_mock_data()

        self.update_mock_file_name()

        self.mock_feature_input()

        self.record_anchor_feature_pos_excites()

    def update_mock_file_name(self):
        current_data = self.mock_data_loader.current_data
        self.cortex_obj.mock_file_name = f"{current_data['mnist_name']}_{current_data['feature_ind']}"

    def record_anchor_feature_pos_excites(self):
        if not self.mock_data_loader.is_next_data_new_feature or self.mock_data_loader.is_next_data_new_mnist:
            return

        cortex = self.cortex

        # 记录当前特征位置，用于mock锚点特征位置
        self.anchor_feature_pos_excites = cortex['excite'][
            NOWA_FEATURE_GRID_INDS]

    def mock_feature_input(self):
        # 整体中心
        self.mock_whole_center_input()

        # 当前特征
        self.mock_current_feature_input()

        self.mock_anchor_pos()

    def mock_anchor_pos(self):
        current_data = self.mock_data_loader.current_data
        cortex = self.cortex
        cortex_obj = self.cortex_obj

        if current_data['feature_ind'] == 0: return

        anchor_pos_inds = get_soma_inds(
            '位置_锚点特征', [f'{x_or_y}' for x_or_y in range(VISUAL_FIELD_WH[0])])
        cortex['excite'][anchor_pos_inds] = self.anchor_feature_pos_excites
        cortex_obj.vary_soma_inds.update(anchor_pos_inds)

    def mock_whole_center_input(self):
        current_data = self.mock_data_loader.current_data
        cortex = self.cortex
        cortex_obj = self.cortex_obj

        # 整体中心
        row_ind, col_ind, region_name, neuron_name, scale = current_data[
            'whole_center_data'].values()
        excite = 10000
        whole_center_soma_inds = get_soma_inds(
            region_name, f'{neuron_name}-注意力竞争结果出现',
            row_ind * REGION[region_name]['region_shape'][1] + col_ind)
        outer_contour_soma_inds = get_soma_inds(
            f'外轮廓边界', [f'{orient}方位{scale}尺度的外轮廓边界' for orient in ORIENTS])
        cortex['excite'][whole_center_soma_inds] = excite
        cortex['excite'][outer_contour_soma_inds] = excite
        cortex_obj.vary_soma_inds.update([
            *whole_center_soma_inds,
            *outer_contour_soma_inds,
        ])

    def mock_current_feature_input(self):
        cortex = self.cortex
        cortex_obj = self.cortex_obj
        current_data = self.mock_data_loader.current_data
        row_ind, col_ind, region_name, neuron_name, scale, *contour_center_open_angle = current_data[
            'feature_data'].values()
        excite = 10000
        feature_soma_inds = get_soma_inds(
            region_name, f'{neuron_name}-注意力竞争结果出现',
            row_ind * REGION[region_name]['region_shape'][1] + col_ind)
        scale_prop_soma_inds = get_soma_inds('属性-尺度', f'尺度{scale}-个体编码出现')
        angle_prop_soma_inds = []
        if len(contour_center_open_angle) == 1:
            angle_prop_soma_inds = get_soma_inds(
                '属性-角度',
                f'角度{float(contour_center_open_angle[0]) if contour_center_open_angle[0]!="无" else "无"}-个体编码出现'
            )
        get_soma_inds('属性-尺度', f'尺度{scale}-个体编码出现')
        cortex['excite'][feature_soma_inds] = 585
        cortex['excite'][scale_prop_soma_inds] = 585
        if len(angle_prop_soma_inds) > 0:
            cortex['excite'][angle_prop_soma_inds] = 585
        cortex_obj.vary_soma_inds.update([
            *feature_soma_inds,
            *scale_prop_soma_inds,
            *angle_prop_soma_inds,
        ])