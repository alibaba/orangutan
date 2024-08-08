import numpy as np
from .default_config import DEFAULT_CONFIG

common_cortex_opts = {
    **DEFAULT_CONFIG,
    "CORTEX_W": 60000000,
    "controller": "mock_input_and_percept_feature",
    "region_names": [
        "global_control",
        "point",
        "orientation",
        "antipodal_points",
        "ray",
        "angle",
        "contour_center",
        "whole_center",
        "current_feature_position",
        "anchor_point_feature_position",
        "offset_of_current_feature_position_relative_to_overall_center",
        "offset_of_current_feature_position_relative_to_anchor_feature",
        "attribute",
    ],
}

INIT_CORTEX_OPTS = {
    **common_cortex_opts,
    "IS_MOCK_RECORD_PROPS": 0,
    "WRITE_STAGES_lambda": lambda cortex_obj: ["init"],
    "write_slice_lambda": lambda cortex_obj, cortex, get_soma_inds, REGION, TYPE: [],
    "WRITE_NERVE_PROPS": ["excite"],
    "form_synapse_rules": [
        "excite_edge_points",
        "various_points_excite_various_orientations",
        "contour_orientation_excitation_ray",
        "contour_orientation_excitation_contour_line",
        "ray_excitation_angle",
        "contour_line_excite_contour_center",
        "attention_competition",
        "contour_center_feedback_excite_contour_orientation",
        "contour_center_feedback_excitation_contour_line",
        "angular_feedback_excitation_ray",
        "ray_feedback_excite_vertical_orientation",
        "contour_orientation_feedback_excite_edge_points",
        "excite_feature_position_and_global_center_position",
        "excite_current_feature_relative_to_global_center_offset",
        "excite_current_feature_relative_to_anchor_feature_offset",
        "perceive_attribute_with_feedback_signal_angle",
        "perceive_attribute_with_feedback_signal_arc",
    ],
}

WRITE_PRESET_IND = 1
RUN_CORTEX_OPTS = {
    **common_cortex_opts,
    "MODE": "run",
    "IS_MOCK_RECORD_PROPS": 1,
    "WRITE_STAGES_lambda": lambda cortex_obj: [
        "init",
        # 'cycle_start',
        # 'cycle_end',
        # 'pos_offset',
        # 'back_propagation_to_dot',
        # 'reset_cortex_props_to_initial_state',
        *[
            [
                # 'back_propagation_to_dot',
                "attention_result",
            ],
            [
                # "cycle_end",
                "attention_result",
                "percept_properties",
            ],
            (
                [
                    "spike_soma",
                    "spike_axon",
                    "spike_axon_end",
                    "spike_dendrite",
                    "cycle_end",
                    "attention_result",
                    "percept_properties",
                ]
                if cortex_obj.tick == 51
                else [
                    # ] if cortex_obj.tick == 9 else [
                    # "cycle_end",
                    "attention_result",
                    "percept_properties",
                ]
            ),
        ][WRITE_PRESET_IND],
    ],
    "write_slice_lambda": lambda cortex_obj, cortex, get_soma_inds, REGION, TYPE: np.concatenate(
        (
            get_soma_inds("point", "input"),
            *[
                [
                    cortex["ind"][
                        (cortex["region_no"] == REGION["angle"]["region_no"])
                        * (cortex["type"] == TYPE["soma"])
                    ],
                    cortex["ind"][
                        (cortex["region_no"] == REGION["contour_center"]["region_no"])
                        * (cortex["type"] == TYPE["soma"])
                    ],
                ],
                [
                    cortex["ind"][(cortex["type"] == TYPE["soma"])],
                    cortex["ind"][(cortex["type"] == TYPE["axon"])],
                ],
                [
                    cortex["ind"],
                    # cortex['ind'][(cortex['region_no'] <= REGION['contour_center']['region_no'])],
                ],
            ][WRITE_PRESET_IND],
        )
    ),
    "WRITE_NERVE_PROPS": [
        "excite",
        # 'current_step',
    ],
    "MNIST_INPUTS_LIST": [
        "4_0",
        # "8_0",
        # "0_0",
        # "8_11",
        # '3_2',
        # *([f'{i}_{j}' for i in range(10) for j in range(10)][::-1]),
        # *([f'{i}_{j}' for i in range(10) for j in range(2)][::-1]),
        # *[f'{i}_{j}' for i in range(10) for j in range(100)],
        # *[f'{i}_{j}' for j in range(100) for i in range(10)],
        # 'perception_test/contour',
    ],
    "form_posterior_synapse_rules": [],
}
