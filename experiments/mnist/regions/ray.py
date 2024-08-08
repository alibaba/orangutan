from consts.feature import (
    VISUAL_FIELD_WH,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ORIENTS,
    ORIENT_SIDES,
)
from consts.nerve_props import TYPE
from util import is_can_init_orient_mask_map

region_info = [
    {
        "region_name": f"ray",
        "region_shape": (*VISUAL_FIELD_WH, 1),
        "neurons": [
            {
                "name": f"summarize_max_values_of_all_rays",
                "feature": {},
                "dendrites": [
                    {
                        "name": "$_DMax",
                        "feature": {
                            "type": TYPE["dendrite_max"],
                        },
                    },
                ],
                "axons": [
                    {
                        "name": f"$_A_excitation_of_step0",
                        "feature": {
                            "step_length": 0,
                        },
                    },
                ],
            },
            {
                "name": f"summarize_max_values_of_all_rays_autapse",
                "feature": {},
                "dendrites": [
                    {
                        "name": "$_DMax",
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
            },
            *[
                {
                    "name": f"summarize_max_values_of_rays_in_{orient}_direction_{orient_side}_side",
                    "feature": {},
                    "dendrites": [
                        {
                            "name": "$_DMax",
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
                            "name": f"$_A_all_or_none_strong_inhibit",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                        {
                            "name": f"$_A_all_or_none_weak_inhibition",
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
                    "name": f"summarize_max_values_of_rays_in_{orient}_direction_{orient_side}_side_feedback",
                    "feature": {},
                    "dendrites": [
                        {
                            "name": "$_DMax",
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
                for orient_side in ORIENT_SIDES
            ],
        ],
    },
    *[
        {
            "region_name": f"ray-S{receptive_field_level}",
            "region_shape": (*VISUAL_FIELD_WH, 1),
            "neurons": [
                *[
                    {
                        "name": f"rays_in_{orient}_direction_{orient_side}_side",
                        "feature": {},
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [],
                        "axons": [
                            {
                                "name": f"$_A_excitation_with_step_length_2",
                                "feature": {
                                    "step_length": 2,
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
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"rays_in_{orient}_direction_{orient_side}_side_for_maximum_excitation",
                        "feature": {},
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": "$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                        "axons": [],
                    }
                    for orient in ORIENTS
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"rays_in_{orient}_direction_{orient_side}_side_feedback",
                        "feature": {},
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": "$_DMax",
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
                *[
                    {
                        "name": f"summarize_rays_on_all_directions_{orient_side}_side",
                        "feature": {},
                        "dendrites": [
                            {
                                "name": "$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                                "dendrites": [
                                    {
                                        "name": f"$_DMin_{orient}_direction",
                                        "feature": {
                                            "type": TYPE["dendrite_min"],
                                        },
                                    }
                                    for orient in ORIENTS
                                ],
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
                        ],
                    }
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"{orient}_direction_max_excitation_{orient_side}_side_rays",
                        "feature": {},
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [
                            {
                                "name": "$_DMax",
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
                    for orient_side in ORIENT_SIDES
                ],
            ],
        }
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS
    ],
]
