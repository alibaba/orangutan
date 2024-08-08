import numpy as np
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from ..mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS, APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs, GENERATIVE_POPU_ABSTRACT_APPEAR_INDS, GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS
from consts.base import IMG_PATH
from consts.feature import CONTOUR_SIDES, CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE, ABSTRACT_EXCITE
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from consts.nerve_props import DENDRITE_TYPE, PART_PROPS_DTYPE, PART_PROPS_MATRIX, TYPE, PART_PROPS_KEYS_MAP, RELEASE_TYPE, PART_PROPS, DYNAMIC_PROP_NAMES, STATIC_PROP_NAMES, SYNAPSE_TYPE, SPINE_EXINFO, POSTERIOR_SYNAPSE_EXINFO
from ....regions import REGION, REGION_INDEX_MAP
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP, STANDARD_PREDICT_EXCITE, SPINE_SIZE_SUM_LIMIT, POST_SYNAPSE_RESOURCE_SUM, PIXEL_MAX_EXCITE
from PIL import Image
from experiments.util import get_soma_inds
# from ..feature_name_loader import Load_feature
import itertools
from .abstract_mocker import Abstract_mocker

attention_result_inds = np.array(
    list(
        itertools.chain(*[
            get_soma_inds(feature_type, f'{feature_name}的注意力竞争结果')
            for feature_type in ['angle', 'contour_center'] for feature_name in {
                'angle': ANGLE_NAMES,
                'contour_center': [f'{side}contour_center' for side in CONTOUR_SIDES],
            }[feature_type]
        ])))


class Mnist_mocker(Abstract_mocker):

    def __init__(self, cortex_obj):
        super().__init__(cortex_obj, mock_data_list=self.get_mock_data_list())
        self.attention_feature_count = 0

    def get_mock_data_list(self):

        def get_run_tick_sum_with_num(num):
            # feature_sum = {
            #     0: 1,
            #     1: 1,
            #     2: 2,
            #     3: 3,
            #     4: 4,
            #     5: 2,
            #     6: 2,
            #     7: 1,
            #     8: 4,
            #     9: 2,
            # }[num]
            feature_sum = 5
            # 注意力结果出现的帧数的间隔：结果1：9，后面都统一17
            return 9 + 17 * (feature_sum - 1)

        return [{
            'mnist_name':
            mnist_name,
            'run_tick_sum':
            get_run_tick_sum_with_num(int(mnist_name.split('_')[0])),
        } for mnist_name in CORTEX_OPTS['MNIST_INPUTS_LIST']]

    def mock_input(self):

        self.mock_data_loader.load_next_mock_data()
        mock_mnist_name = self.mock_data_loader.current_data['mnist_name']
        self.cortex_obj.mock_file_name = mock_mnist_name

        input_soma_inds = get_soma_inds('point', 'input')
        self.cortex['excite'][input_soma_inds] = self.get_mnist_input_matrix(
            mock_mnist_name).ravel() + self.cortex['RP'][input_soma_inds]

        self.cortex_obj.write_cortex('mock_input')

        self.cortex_obj.vary_soma_inds.update(
            input_soma_inds[self.cortex['excite'][input_soma_inds] >= ATP])

    def get_mnist_input_matrix(self, mnist_name):
        INPUT_FOLDER_NAME = 'd28_mnist/' if '/' not in mnist_name else ''
        I = Image.open(f'{IMG_PATH}/input/{INPUT_FOLDER_NAME}{mnist_name}.bmp')
        L = I.convert('L')  # 转化为灰度图
        mnist_input_matrix = np.asarray(L, np.int32) / 255 * PIXEL_MAX_EXCITE

        return mnist_input_matrix
