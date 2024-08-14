from .abstract_controller import Abstract_controller
import itertools
from ..input_mocker.mnist_mocker import Mnist_mocker
from ..mock_globals import NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS
from consts.feature import CONTOUR_SIDES, ANGLE_NAMES
from .....util import get_soma_inds
import numpy as np


attention_result_inds = np.array(
    list(
        itertools.chain(*[
            get_soma_inds(feature_type, f'attention_competition_result_of_{feature_name}')
            for feature_type in ['angle', 'contour_center'] for feature_name in {
                'angle': ANGLE_NAMES,
                'contour_center': [f'{side}_contour_center' for side in CONTOUR_SIDES],
            }[feature_type]
        ])))


class Controller(Abstract_controller):

    def __init__(self, cortex_obj):
        super().__init__(cortex_obj)
        self.attention_feature_count = 0
        self.back_propagation_tick_count = 0

    def get_input_mocker(self):
        return Mnist_mocker(self.cortex_obj)

    def mock_input(self):
        self.mock_anchor()
        self.input_mocker.mock_input()

    def mock_anchor(self):
        if self.attention_feature_count > 1:
            self.cortex['excite'][
                ANCHOR_FEATURE_GRID_INDS] = self.anchor_feature_pos_excites
            self.cortex_obj.vary_soma_inds.update(ANCHOR_FEATURE_GRID_INDS)

    def is_can_reset_cortex_props_at_cycle_end(self):
        return self.input_mocker.mock_data_loader.is_next_data_new_feature

    def on_cortex_start(self):
        global attention_result_ind_on_cortex_start
        attention_result_ind_on_cortex_start = attention_result_inds[np.argmax(
            self.cortex_obj.cortex['excite'][attention_result_inds])]

    def on_cortex_cycle_end(self):
        global attention_result_ind_on_cortex_start

        # If there are two identical excited winner cells after attention competition, only one of them is forcibly retained.
        if sum(self.cortex_obj.cortex['excite'][attention_result_inds] > 0
               ) > 1:
            max_excite_ind = attention_result_inds[np.argmax(
                self.cortex_obj.cortex['excite'][attention_result_inds])]
            self.cortex_obj.cortex['excite'][attention_result_inds[
                attention_result_inds !=
                max_excite_ind]] = self.cortex_obj.cortex['RP'][
                    attention_result_inds[
                        attention_result_inds != max_excite_ind]]

        attention_result_ind = attention_result_inds[np.argmax(
            self.cortex_obj.cortex['excite'][attention_result_inds])]

        if sum(
                self.cortex_obj.cortex['excite'][attention_result_inds] > 0
        ) > 0 and attention_result_ind != attention_result_ind_on_cortex_start:

            # Before moving on to the next feature, record the position of the current feature.
            if self.attention_feature_count > 0:
                # Record the current feature position for mocking anchor point feature position.
                self.anchor_feature_pos_excites = self.record_anchor_feature_pos_excites

            self.cortex_obj.write_cortex('attention_result')
            self.attention_feature_count += 1
            self.back_propagation_tick_count = 0
        else:
            self.back_propagation_tick_count += 1

        if self.back_propagation_tick_count == 4:
            self.cortex_obj.write_cortex('percept_properties')

        if self.back_propagation_tick_count == 5:
            self.cortex_obj.write_cortex('back_propagation_to_dot')

        if self.back_propagation_tick_count == 1 and self.attention_feature_count > 0:
            self.record_anchor_feature_pos_excites = self.cortex['excite'][
                NOWA_FEATURE_GRID_INDS]

        if self.back_propagation_tick_count == 2:
            self.cortex_obj.write_cortex('pos_offset')
