from consts.feature import (
    VISUAL_FIELD_WH,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    ORIENT_SIDES,
    ORIENT_CONTOUR_SIDES,
    ORIENT_SUM,
    BOTH_SIDE_ORIENT_DESC,
)
from consts.nerve_props import TYPE, RELEASE_TYPE
from util import is_can_init_orient_mask_map

region_info = [
    {
        "region_name": f"orientation",
        "region_shape": (*VISUAL_FIELD_WH, 1),
        "neurons": [
            *[
                {
                    "name": f"inner_contour_orientation_summary_{orient}",
                    "feature": {
                        "exinfo_0": orient,
                    },
                    "dendrites": [
                        {
                            "name": f"$_DMax",
                            "feature": {
                                "type": TYPE["dendrite_max"],
                            },
                        },
                    ],
                    "axons": [
                        {
                            "name": f"$_A_inhibit",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                        {
                            "name": f"$_A_all_or_none_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 1,
                            },
                        },
                        {
                            "name": f"$_A_all_or_none_strong_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                    ],
                }
                for orient in ORIENTS
            ],
            *[
                {
                    "name": f"inner_contour_orientation_summary_{orient}_autapse",
                    "feature": {
                        "exinfo_0": orient,
                    },
                    "dendrites": [
                        {
                            "name": f"$_DMax",
                            "feature": {
                                "type": TYPE["dendrite_max"],
                            },
                        },
                    ],
                    "axons": [
                        {
                            "name": f"$_A_inhibit",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                        {
                            "name": f"$_A_all_or_none_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 1,
                            },
                        },
                        {
                            "name": f"$_A_all_or_none_strong_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                    ],
                }
                for orient in ORIENTS
            ],
            *[
                {
                    "name": f"inner_contour_orientation_summary_{orient}_feedback",
                    "feature": {
                        "exinfo_0": orient,
                    },
                    "dendrites": [
                        {
                            "name": f"$_DMax",
                            "feature": {
                                "type": TYPE["dendrite_max"],
                            },
                        },
                    ],
                    "axons": [
                        {
                            "name": f"$_A_all_or_none_strong_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                        {
                            "name": f"$_A_inhibit",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                    ],
                }
                for orient in ORIENTS
            ],
            *[
                {
                    "name": f"inner_contour_orientation_summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}",
                    "dendrites": [
                        {
                            "name": f"$_DMax",
                            "feature": {
                                "type": TYPE["dendrite_max"],
                            },
                        },
                    ],
                    "axons": [
                        {
                            "name": f"$_A_all_or_none_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 1,
                            },
                        },
                    ],
                }
                for orient_ind in range(ORIENT_SUM // 2)
            ],
            *[
                {
                    "name": f"inner_contour_orientation_summary_{orient}_{orient_side}_with_feedback_on_curve_edge",
                    "dendrites": [
                        {
                            "name": f"$_DMin",
                            "feature": {
                                "type": TYPE["dendrite_min"],
                            },
                        },
                    ],
                    "axons": [
                        {
                            "name": f"$_A_inhibit",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                        {
                            "name": f"$_A_all_or_none_strong_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                        {
                            "name": f"$_A_excitation_of_step0",
                            "feature": {
                                "step_length": 0,
                            },
                        },
                    ],
                }
                for orient in ORIENTS
                for orient_side in ORIENT_SIDES
            ],
            {
                "name": f"inner_contour_orientation_summary_at_position",
                "dendrites": [
                    {
                        "name": f"$_DMax",
                        "feature": {
                            "type": TYPE["dendrite_max"],
                        },
                    },
                ],
                "axons": [
                    {
                        "name": f"$_A_all_or_none_weak_inhibition",
                        "feature": {
                            "post_sign": -1,
                            "all_or_none": 1,
                        },
                    },
                ],
            },
        ],
    },
    *[
        {
            "region_name": f"orientation-S{receptive_field_level}",
            "region_shape": (*VISUAL_FIELD_WH, 1),
            "neurons": [
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{side}_contour",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                            {
                                "name": f"$_DMax_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_DMax_inner_contour_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_A_excitation_of_step0",
                                "feature": {
                                    "step_length": 0,
                                },
                            },
                        ],
                    }
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{side}_contour_autapse",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                        ],
                    }
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{side}_contour_sum_value",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                            {
                                "name": f"$_DMax_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_DMax_inner_contour_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                        ],
                    }
                    for side in ["inner"]
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{side}_contour_complex_cell",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                        ],
                    }
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{side}_contour_feedback",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                        ],
                    }
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{side}_contour_complex_cell_feedback",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_all_or_none_strong_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                    "all_or_none": 2,
                                },
                            },
                        ],
                    }
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{orient_side}_side",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                            {
                                "name": f"$_DMax_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_A_all_or_none_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                    "all_or_none": 1,
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"orientation_of_{orient}_direction_{orient_side}_side_feedback",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"summary_of_{orient}_direction_inner_scale_inner_contour_orientation",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"summary_of_{orient}_direction_inner_scale_inner_contour_orientation_sum_value",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"max_excitation_{orient}_direction_{side}_contour_orientation",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": f"$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                            {
                                "name": f"$_DMax_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_DMax_inner_contour_inhibit",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                        ],
                        "axons": [
                            {
                                "name": f"$_A_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_A_excitation_of_step0",
                                "feature": {
                                    "step_length": 0,
                                },
                            },
                        ],
                    }
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"max_excitation_{orient}_direction_position_inner_contour_orientation",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "axons": [
                            {
                                "name": f"$_A_all_or_none_strong_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                    "all_or_none": 2,
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"max_excitation_{orient}_direction_position_with_feedback_inner_contour_orientation",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "axons": [
                            {
                                "name": f"$_A_all_or_none_strong_inhibit",
                                "feature": {
                                    "post_sign": -1,
                                    "all_or_none": 2,
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                ],
            ],
        }
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS
    ],
]
