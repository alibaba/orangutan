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
        "region_name": f"方位",
        "region_shape": (*VISUAL_FIELD_WH, 1),
        "neurons": [
            *[
                {
                    "name": f"汇总{orient}方向的内轮廓方位",
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
                            "name": f"$_A抑制",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                        {
                            "name": f"$_A全或无弱抑制",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 1,
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
                for orient in ORIENTS
            ],
            *[
                {
                    "name": f"汇总{orient}方向的内轮廓方位_自突触",
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
                            "name": f"$_A抑制",
                            "feature": {
                                "post_sign": -1,
                            },
                        },
                        {
                            "name": f"$_A全或无弱抑制",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 1,
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
                for orient in ORIENTS
            ],
            *[
                {
                    "name": f"汇总{orient}方向的内轮廓方位_反馈",
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
            ],
            *[
                {
                    "name": f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向的内轮廓方位",
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
                            "name": f"$_A全或无抑制",
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
                    "name": f"汇总{orient}方向{orient_side}侧位于弧线边缘且有反馈的内轮廓方位",
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
            {
                "name": f"汇总所在位置位于弧线边缘且有反馈的内轮廓方位",
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
            },
            {
                "name": f"汇总所在位置的内轮廓方位",
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
                        "name": f"$_A全或无弱抑制",
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
            "region_name": f"方位-S{receptive_field_level}",
            "region_shape": (*VISUAL_FIELD_WH, 1),
            "neurons": [
                *[
                    {
                        "name": f"{orient}方向的{side}轮廓方位",
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
                                "name": f"$_DMax抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_DMax内轮廓抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
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
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"{orient}方向的{side}轮廓方位_自突触",
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
                                "name": f"$_A抑制",
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
                        "name": f"{orient}方向的{side}轮廓方位_求和",
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
                                "name": f"$_DMax抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_DMax内轮廓抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
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
                    }
                    # for side in ORIENT_CONTOUR_SIDES
                    for side in ["内"]
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"{orient}方向的{side}轮廓方位_复杂细胞",
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
                                "name": f"$_A抑制",
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
                        "name": f"{orient}方向的{side}轮廓方位_反馈",
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
                                "name": f"$_A抑制",
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
                        "name": f"{orient}方向的{side}轮廓方位_复杂细胞_反馈",
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
                                "name": f"$_A全或无强抑制",
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
                        "name": f"{orient}方向的{orient_side}侧方位",
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
                                "name": f"$_DMax抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
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
                                "name": f"$_A全或无弱抑制",
                                "feature": {
                                    "post_sign": -1,
                                    "all_or_none": 1,
                                },
                            },
                            # {
                            #     "name": f"$_A强化激励射线",
                            #     "feature": {
                            #         "transmitter_release_sum": 1.15,
                            #         "release_type": RELEASE_TYPE["Fa_multi"],
                            #     },
                            # },
                        ],
                    }
                    for orient in ORIENTS
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"{orient}方向的{orient_side}侧方位_反馈",
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
                        "name": f"汇总{orient}方向尺度内的内轮廓方位",
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
                                "name": f"$_A抑制",
                                "feature": {
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_A高RP阈值抑制",
                                "feature": {
                                    "post_sign": -1,
                                    "RP": -65 * 100,
                                    "transmitter_release_sum": 65 * 200,
                                },
                            },
                        ],
                    }
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"汇总{orient}方向尺度内的内轮廓方位_求和",
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
                                "name": f"$_A抑制",
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
                        "name": f"汇总所有方向{orient_side}侧位于弧线边缘且有反馈的内轮廓方位",
                        "dendrites": [
                            {
                                "name": f"$_DMax",
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
                        ],
                    }
                    for orient_side in ORIENT_SIDES
                ],
                *[
                    {
                        "name": f"{orient}方向兴奋最大的{side}轮廓方位",
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
                                "name": f"$_DMax抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
                                },
                            },
                            {
                                "name": f"$_DMax内轮廓抑制",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                    "post_sign": -1,
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
                    for side in ORIENT_CONTOUR_SIDES
                    for orient in ORIENTS
                ],
                *[
                    {
                        "name": f"{orient}方向所在位置兴奋最大的内轮廓方位",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "axons": [
                            {
                                "name": f"$_A全或无强抑制",
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
                        "name": f"{orient}方向所在位置兴奋最大且有反馈的内轮廓方位",
                        "feature": {
                            "exinfo_0": orient,
                        },
                        "neuron_in_pic_mask": is_can_init_orient_mask_map[
                            (orient, receptive_field_level)
                        ],
                        "axons": [
                            {
                                "name": f"$_A全或无强抑制",
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
