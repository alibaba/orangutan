# # from .mock_utils import get_all_mock_abstract_feature_names
# import numpy as np
# import itertools
# from .mock_props import Mock_props
# from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP
# from ..mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS, APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs, POPU_ABSTRACT_DISAPPEAR_STP_INDS
# from consts.feature import CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE


# class Controller():

#     def __init__(self, cortex_obj, get_soma_inds):
#         self.cortex_obj = cortex_obj
#         self.cortex = cortex_obj.cortex
#         self.get_soma_inds = get_soma_inds
#         self.init_mock_input()

#     def init_mock_input(self):
#         self.mock_props = Mock_props(
#             self.cortex_obj,
#             self.get_soma_inds,
#             self.make_mock_feature_list,
#         )

#     def make_mock_feature_list(self, mock_feature_names_list):
#         mock_features = []
#         for mock_feature_names in mock_feature_names_list:
#             mock_features.extend(
#                 list(
#                     itertools.chain(*[[(mock_feature_name, {
#                         'play_direction': 'forward'
#                     })] * 3 for mock_feature_name in mock_feature_names])))

#         return mock_features

#     def mock_input(self):
#         self.mock_props.mock_next_props()

#     def is_can_nerve_spike(self):
#         return self.mock_props.nowa_feature_exinfo[
#             'play_direction'] == 'forward'

#     def is_can_form_synapse(self):
#         return False

#     def is_can_weaken_synapse(self):
#         return False

#     def get_active_num(self):
#         return int(self.mock_props.nowa_feature_name.split('_')[0])

#     def mock_数字(self):
#         cortex_obj = self.cortex_obj
#         cortex = cortex_obj.cortex
#         get_soma_inds = self.get_soma_inds
#         num_input = self.get_active_num()
#         # if num_input == None or num_input < 0: return

#         inds_数字 = get_soma_inds('数字', 'input', num_input)
#         cortex['excite'][inds_数字] = NUM_EXCITE

#         # cortex_obj.vary_soma_inds.update(inds_数字)

#         return inds_数字