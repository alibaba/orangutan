import os
import numpy as np
from ....regions import REGION
from consts.feature import CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE
from consts.nerve_props import TYPE
from consts.base import IMG_PATH
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
from ..mock_features import mock_features
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP
from experiments.util import get_soma_inds
from ..mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS
from .abstract_controller import Abstract_controller
from ..input_mocker.feature_mocker import Feature_mocker


class Controller(Abstract_controller):

    def __init__(self, cortex_obj):
        super().__init__(cortex_obj)

    def get_input_mocker(self):
        return Feature_mocker(self.cortex_obj)

    def mock_input(self):
        self.input_mocker.mock_input()

    def on_cortex_cycle_end(self):
        if self.input_mocker.mock_data_loader.is_next_data_new_feature:
            self.record_props()

    def record_props(self):
        ''' 写入input会自动覆盖，但如果老的序列比新序列长，那么多出来的节点就不会被清除，在mock的时候依然会被读取，导致结果有偏差
            所以写入前需要清理这个mnist相关的全部的文件，保证所有文件都是这次写入的
        '''
        current_data = self.input_mocker.mock_data_loader.current_data
        nowa_mnist = current_data['mnist_name']
        nowa_feature_ind = current_data['feature_ind']
        save_input_path = f'{INPUT_DIR}/{nowa_mnist}_{nowa_feature_ind}'
        feature_sequence_ind = current_data.get('feature_sequence_ind')
        if feature_sequence_ind != None:
            save_input_path += f'_{feature_sequence_ind}'
        cortex = self.cortex

        if nowa_feature_ind == 0:
            self.clear_record_data_files(nowa_mnist, feature_sequence_ind)

        # 记录抽象细胞兴奋
        np.save(
            f'{save_input_path};excite',
            cortex['excite'][SINGLE_ABSTRACT_APPEAR_INDS],
            # cortex['excite'][POPU_ABSTRACT_APPEAR_INDS],
            allow_pickle=False)

        # 记录抽象细胞tick_spike_times
        np.save(
            f'{save_input_path};tick_spike_times',
            cortex['tick_spike_times'][SINGLE_ABSTRACT_APPEAR_INDS],
            # cortex['tick_spike_times'][POPU_ABSTRACT_APPEAR_INDS],
            allow_pickle=False)

        # 记录当前特征网格细胞兴奋
        np.save(f'{save_input_path};grid',
                cortex['excite'][NOWA_FEATURE_GRID_INDS],
                allow_pickle=False)
        # 记录整体特征网格细胞兴奋
        np.save(f'{save_input_path};whole_center_grid',
                cortex['excite'][WHOLE_CENTER_GRID_INDS],
                allow_pickle=False)

    def clear_record_data_files(self, mnist_name, feature_sequence_ind=None):
        remove_paths = [
            file_name for file_name in os.listdir(INPUT_DIR)
            if file_name.startswith(f'{mnist_name}_') and (
                feature_sequence_ind == None
                or file_name.split(';')[0].endswith(str(feature_sequence_ind)))
        ]
        for remove_path in remove_paths:
            os.remove(f'{INPUT_DIR}/{remove_path}')

    def is_can_reset_cortex_props_at_cycle_end(self):
        return self.input_mocker.mock_data_loader.is_next_data_new_feature