from consts.feature import COMMON_ABSTRACT_TYPES, ABSTRACT_EXCITE
from consts.nerve_props import TYPE, RELEASE_TYPE
from consts.nerve_params import PIXEL_MAX_EXCITE

ACTION_NAMES = ["扫视到下个特征", "得出结论"]
region_info = {
    "region_name": "全局调控",
    "region_shape": (1, 1, 1),
    "neurons": [
        *[
            {
                "name": f"注意力竞争兴奋汇总{suffix}",
                "feature": {},
                "dendrites": [
                    {
                        "name": "$_DMin",
                        "feature": {
                            "type": TYPE["dendrite_min"],
                        },
                        "dendrites": [
                            {
                                "name": "$_DMax",
                                "feature": {
                                    "type": TYPE["dendrite_max"],
                                },
                            },
                        ],
                    },
                ],
                "axons": [
                    {
                        "name": "$_A全或无弱抑制",
                        "feature": {
                            "post_sign": -1,
                            "all_or_none": 1,
                        },
                    },
                    {
                        "name": "$_A易化全或无自禁止激励结束特征归纳",
                        "feature": {
                            "release_type": RELEASE_TYPE["Fa"],
                        },
                    },
                ],
            }
            for suffix in ["", "-外轮廓中心"]
        ],
        {
            "name": "onehot数字预测",
            "feature": {},
            "dendrites": [
                {
                    "name": "onehot数字预测_DMax",
                    "feature": {
                        "type": TYPE["dendrite_max"],
                    },
                },
            ],
            "axons": [
                {
                    "name": "onehot数字预测_A全或无弱抑制",
                    "feature": {
                        "post_sign": -1,
                        "all_or_none": 1,
                    },
                },
                {
                    "name": "onehot数字预测_A禁止激励前馈预测偏差",
                    "feature": {
                        "post_sign": -1,
                    },
                },
                {
                    "name": "onehot数字预测_A禁止抑制激励前馈预测意外",
                    "feature": {
                        "post_sign": -1,
                    },
                },
            ],
        },
        {
            "name": "公用调控兴奋",
            "feature": {
                "excite": 0,
                "self_synapse": 2,
            },
            "axons": [
                {
                    "name": "公用调控兴奋_A自维持",
                    "feature": {},
                },
                {
                    "name": "$_A抑制",
                    "feature": {
                        "post_sign": -1,
                    },
                },
                {
                    "name": "公用调控兴奋_A数字前馈预测偏差",
                    "feature": {
                        "transmitter_release_sum": 65 * 11,
                    },
                },
                {
                    "name": "公用调控兴奋_A全或无禁止解禁激励有向轮廓中心",
                    "feature": {
                        "transmitter_release_sum": 65 * 10,
                        "post_sign": -1,
                        "all_or_none": 1,
                    },
                },
                {
                    "name": "公用调控兴奋_A激励属性群体编码缺失",
                    "feature": {
                        "transmitter_release_sum": 65 * 10,
                    },
                },
                {
                    "name": "公用调控兴奋_A限制激励数字预测onehot的最大值",
                    "feature": {
                        "transmitter_release_sum": 500,
                        "step_length": 21,
                    },
                },
                {
                    "name": "公用调控兴奋_A解禁前馈预测",
                    "feature": {
                        "post_sign": -1,
                    },
                },
                {
                    "name": "公用调控兴奋_A限制激励注意力竞争结果最大值",
                    "feature": {
                        "transmitter_release_sum": 10065,  # 最低兴奋
                    },
                },
                {
                    "name": "公用调控兴奋_A限制抽象个体编码最大兴奋",
                    "feature": {
                        "transmitter_release_sum": ABSTRACT_EXCITE,  # 最低兴奋
                    },
                },
                {
                    "name": "公用调控兴奋_A解禁用轮廓直线强化激励内轮廓中心",
                    "feature": {
                        "transmitter_release_sum": 65,  # 最低兴奋
                        "post_sign": -1,
                    },
                },
                {
                    "name": "公用调控兴奋_A激励群体编码未消失",
                    "feature": {},
                },
                {
                    "name": "公用调控兴奋_A限制属性出现时机",
                    "feature": {
                        "transmitter_release_sum": 10000,  # 最低兴奋
                        # 'step_length': 15,
                        # debug
                        "step_length": 1,
                    },
                },
                {
                    "name": "公用调控兴奋_A全或无抑制对缺口方位的抑制",
                    "feature": {
                        # 避免全或无抑制兴奋过大，导致在6_2下17，18点上朝67.5的缺口因为相关的内轮廓方位兴奋偏小，无法被抑制
                        # 'transmitter_release_sum': 225 * 100 / 2,
                        "transmitter_release_sum": 70 * 100,
                        "post_sign": -1,
                        "all_or_none": 1,
                    },
                },
                {
                    "name": "公用调控兴奋_A理论极值",
                    "feature": {
                        "transmitter_release_sum": 225 * 100,
                    },
                },
                {
                    "name": "$_A控制注意力竞争开始时机",
                    "feature": {
                        # 'step_length': 9,
                        "step_length": 8,
                        "transmitter_release_sum": 100000000,
                    },
                },
            ],
        },
        {
            "name": "激励属性",
            "feature": {
                "excite": 65 * 100,
                "self_synapse": 2,
            },
            "axons": [
                {
                    "name": "$_A激励朝向无",
                    "feature": {},
                },
                {
                    "name": "$_A禁止激励朝向无",
                    "feature": {
                        "all_or_none": 1,
                        "post_sign": -1,
                    },
                },
                {
                    "name": "$_A激励角度无",
                    "feature": {},
                },
                {
                    "name": "$_A禁止激励角度无",
                    "feature": {
                        "all_or_none": 1,
                        "post_sign": -1,
                    },
                },
            ],
        },
        {
            "name": "汇总所有位置位于弧线边缘且有反馈的内轮廓方位",
            "feature": {},
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
                    "name": "$_A抑制",
                    "feature": {
                        "post_sign": -1,
                    },
                },
            ],
        },
        {
            "name": "方位激励射线的最小兴奋",
            "feature": {
                "excite": 255 * 10 * 2,
                "self_synapse": 2,
            },
            "axons": [
                {
                    "name": "方位激励射线的最小兴奋_A抑制射线",
                    "feature": {
                        "transmitter_release_sum": 65 * 10 / 2,
                        "post_sign": -1,
                    },
                },
            ],
        },
        {
            "name": "开启反馈预测",
            "feature": {},
            "axons": [
                # 最终得分
                {
                    "name": "开启反馈预测_A易化抑制激励最终得分",
                    "feature": {
                        "transmitter_release_sum": 1,
                        "release_type": RELEASE_TYPE["Fa"],
                    },
                },
                {
                    "name": "开启反馈预测_A抑制激励累积兴奋",
                    "feature": {
                        "transmitter_release_sum": 65 * 10000000000,
                        "post_sign": -1,
                    },
                },
            ],
        },
        # 行动
        *[
            {
                "name": action_name,
                "feature": {},
                "dendrites": {
                    "得出结论": [
                        {
                            "name": f"{action_name}_DMax",
                            "feature": {
                                "type": TYPE["dendrite_max"],
                            },
                        },
                        {
                            "name": f"{action_name}_DAdd全或无抑制",
                            "feature": {
                                "post_sign": -1,
                                "all_or_none": 1,
                            },
                            "dendrites": [
                                {
                                    "name": f"{action_name}_DMax全或无抑制",
                                    "feature": {
                                        "type": TYPE["dendrite_max"],
                                    },
                                },
                            ],
                        },
                    ],
                    "扫视到下个特征": [
                        {
                            "name": f"{action_name}_DMin",
                            "feature": {
                                "type": TYPE["dendrite_min"],
                            },
                            "dendrites": [
                                {
                                    "name": f"{action_name}_DMax",
                                    "feature": {
                                        "type": TYPE["dendrite_max"],
                                    },
                                },
                                {
                                    "name": f"{action_name}_DMax数字onehot",
                                    "feature": {
                                        "type": TYPE["dendrite_max"],
                                    },
                                },
                            ],
                        },
                    ],
                }[action_name],
                "axons": [
                    {
                        "name": f"{action_name}_A激励onehot",
                        "feature": {
                            "step_length": 2,
                        },
                    },
                    {
                        "name": f"{action_name}_A全或无解禁onehot行动调控禁止行为",
                        "feature": {
                            "post_sign": -1,
                            "all_or_none": 2,
                        },
                    },
                ],
            }
            for action_name in ACTION_NAMES
        ],
        *[
            {"name": f"{action_name}onehot", "feature": {}, "axons": []}
            for action_name in ACTION_NAMES
        ],
        {
            "name": "onehot行动调控",
            "feature": {},
            "dendrites": [
                {
                    "name": "onehot行动调控_DMax",
                    "feature": {
                        "type": TYPE["dendrite_max"],
                    },
                },
            ],
            "axons": [
                {
                    "name": "onehot行动调控_A全或无弱抑制",
                    "feature": {
                        "post_sign": -1,
                        "all_or_none": 1,
                    },
                },
            ],
        },
        {
            "name": "注意力竞争结果特征存在",
            "feature": {},
            "dendrites": [
                {
                    "name": "注意力竞争结果特征存在_DMax",
                    "feature": {
                        "type": TYPE["dendrite_max"],
                    },
                },
            ],
            "axons": [],
        },
        {
            "name": "对各个尺度的方位激励射线的拮抗抑制",
            "feature": {
                "excite": PIXEL_MAX_EXCITE / 3,
                "self_synapse": 2,
            },
            "dendrites": [],
            "axons": [
                {
                    "name": "$_A抑制",
                    "feature": {
                        "post_sign": -1,
                        # 'transmitter_release_sum': 65 * 3,
                    },
                },
            ],
        },
    ],
}
