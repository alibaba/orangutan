import numpy as np
from .default_config import DEFAULT_CONFIG

common_cortex_opts = {
    **DEFAULT_CONFIG,
    "CORTEX_W": 60000000,
    "controller": "mock_input_and_percept_feature",
    "region_names": [
        "全局调控",
        "点",
        "方位",
        "线_轮廓直线",
        "线_射线",
        "角",
        "轮廓中心",
        "位置_整体中心",
        "位置_当前特征",
        "位置_锚点特征",
        "位置_当前特征相对整体中心的偏移",
        "位置_当前特征相对锚点特征的偏移",
        "属性",
    ],
}

INIT_CORTEX_OPTS = {
    **common_cortex_opts,
    "IS_MOCK_RECORD_PROPS": 0,
    "WRITE_STAGES_lambda": lambda cortex_obj: ["init"],
    "write_slice_lambda": lambda cortex_obj, cortex, get_soma_inds, REGION, TYPE: [],
    "WRITE_NERVE_PROPS": ["excite"],
    "form_synapse_rules": [
        # 感知
        "点-激励边缘点",
        "方位_各种点激励各种方位",
        "线-轮廓方位激励射线",
        "线-轮廓方位激励轮廓直线",
        "角_射线激励角",
        "轮廓中心-轮廓直线激励轮廓中心",
        # 注意力竞争
        "注意力-注意力竞争",
        # 反馈STD
        "方位-轮廓中心反馈激励轮廓方位",
        "线-轮廓中心反馈激励轮廓直线",
        "线-角反馈激励射线",
        "方位-射线反馈激励垂直方位",
        "点-轮廓方位反馈激励边缘点",
        # 位置
        "位置-激励特征位置和整体中心位置",
        "位置-激励当前特征相对整体中心的偏移",
        "位置-激励当前特征相对锚点特征的偏移",
        # 属性
        "属性_用反馈信号感知属性_角",
        "属性_用反馈信号感知属性_圆弧",
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
            get_soma_inds("点", "input"),
            *[
                [
                    cortex["ind"][
                        (cortex["region_no"] == REGION["角"]["region_no"])
                        * (cortex["type"] == TYPE["soma"])
                    ],
                    cortex["ind"][
                        (cortex["region_no"] == REGION["轮廓中心"]["region_no"])
                        * (cortex["type"] == TYPE["soma"])
                    ],
                ],
                [
                    cortex["ind"][(cortex["type"] == TYPE["soma"])],
                    cortex["ind"][(cortex["type"] == TYPE["axon"])],
                ],
                [
                    cortex["ind"],
                    # cortex['ind'][(cortex['region_no'] <= REGION['轮廓中心']['region_no'])],
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
