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
        "region_name": f"线_射线",
        "region_shape": (*VISUAL_FIELD_WH, 1),
        "neurons": [
            {
                "name": f"汇总所有射线的最大值",
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
                        "name": f"$_A步长0的激励",
                        "feature": {
                            "step_length": 0,
                        },
                    },
                ],
            },
            {
                "name": f"汇总所有射线的最大值_自突触",
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
                        "name": f"$_A抑制",
                        "feature": {
                            "post_sign": -1,
                        },
                    },
                ],
            },
            *[
                {
                    "name": f"汇总{orient}方向{orient_side}侧的射线的最大值",
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
                            "name": f"$_A抑制",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                        {
                            "name": f"$_A全或无强抑制",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                        {
                            "name": f"$_A全或无弱抑制",
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
                    "name": f"汇总{orient}方向{orient_side}侧的射线的最大值_反馈",
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
                            "name": f"$_A全或无强抑制",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 2,
                            },
                        },
                        {
                            "name": f"$_A抑制",
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
            "region_name": f"线_射线-S{receptive_field_level}",
            "region_shape": (*VISUAL_FIELD_WH, 1),
            "neurons": [
                *[
                    {
                        "name": f"{orient}方向{orient_side}侧的射线",
                        "feature": {},
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "dendrites": [],
                        "axons": [
                            {
                                "name": f"$_A步长2的激励",
                                "feature": {
                                    "step_length": 2,
                                },
                            },
                            {
                                "name": f"$_A抑制",
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
                        "name": f"{orient}方向{orient_side}侧的射线_用于激励最大兴奋",
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
                        "name": f"{orient}方向{orient_side}侧的射线_反馈",
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
                                "name": f"$_A抑制",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_A步长0的激励",
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
                        "name": f"汇总所有方向{orient_side}侧的射线",
                        "feature": {},
                        "dendrites": [
                            {
                                "name": "$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                                "dendrites": [
                                    {
                                        "name": f"$_DMin_{orient}方向",
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
                                "name": f"$_A抑制",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_A全或无强抑制",
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
                        "name": f"{orient}方向兴奋最大的{orient_side}侧射线",
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
                                "name": f"$_A全或无强抑制",
                                "feature": {
                                    "post_sign": -1,
                                    "all_or_none": 2,
                                },
                            },
                            {
                                "name": f"$_A抑制",
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
