import numpy as np
from .nerve_params import SRP, NRP

# 神经类型
TYPE = {
    type_name: type_ind
    for type_ind, type_name in enumerate(
        [
            "soma",  # 胞体
            "axon",  # 轴突
            "axon_end",  # 轴突末端
        ]
    )
}
DENDRITE_TYPE = {
    type_name: type_ind + len(TYPE)
    for type_ind, type_name in enumerate(
        [
            "dendrite_min",  # min树突
            "dendrite_max",  # max树突
            "dendrite_add",  # add树突
            "dendrite_weight",  # 加权求和树突
            "dendrite_multi",  # 相乘
        ]
    )
}
TYPE.update(DENDRITE_TYPE)
TYPE.update({"spine_connect": len(TYPE)})
STATIC_TYPES = [TYPE["soma"], TYPE["axon"], *DENDRITE_TYPE.values()]

# 0：不是突触 1：先验突触 2：预测突触 3：易化突触 4：stp突触 5：易化stp突触
SYNAPSE_TYPE = {
    synapse_type: synapse_type_value
    for synapse_type_value, synapse_type in enumerate(
        ["no_synapse", "static", "excite", "Fa", "STP", "Fa_STP"]
    )
}

RELEASE_TYPE = {
    type_name: type_ind
    for type_ind, type_name in enumerate(
        [
            "excite",
            "Fa",
            "Fa_multi",
            "anti_Fa",
            "STP",
            "STD",
            "marker",
            "marker_multi",
        ]
    )
}

# 神经attribute
def part_prop_tuple(dtype, value):
    if value == "RP":
        prop_tuple = (dtype, SRP, *[NRP] * (len(TYPE) - 1))
    elif value == "TYPE":
        prop_tuple = (dtype, *TYPE.values())
    else:
        prop_tuple = (dtype, *[value] * len(TYPE))
    return prop_tuple


POSTERIOR_SYNAPSE_EXINFO = {
    key_name: f"exinfo_{key_ind}"
    for key_ind, key_name in enumerate(
        [
            "prime_key",
            "spine_ind",
            "feature_no",
            "ind_in_circuit",
            "size",
        ]
    )
}

SPINE_EXINFO = {
    key_name: f"exinfo_{key_ind}"
    for key_ind, key_name in enumerate(
        [
            "size",
            "is_form_synapse",
            "parents_info",
            "posted_excite",
            "min_excite",
        ]
    )
}

# TODO 非学习模式下，用不到一些attribute，可以不进行初始化，节省计算资源
# 同时也可以在cortex的计算过程上省略一部分计算步骤，加速计算速度
nerve_prop_meta_info = {
    ("static", "type"): ("int8", "TYPE"),
    ("static", "mother_type"): ("int8", 0),
    ("static", "father_type"): ("int8", 0),
    ("static", "region_no"): ("int", 0),
    ("static", "father_region_no"): ("int", 0),
    ("static", "region_row_no"): ("int", 0),
    ("static", "region_hyper_col_no"): ("int", 0),
    ("static", "neuron_no"): ("int", 0),
    ("static", "mother_neuron_no"): ("int", 0),
    ("static", "RP"): ("float", "RP"),
    ("one_tick", "Fa"): ("float", 1),
    ("one_tick", "anti_Fa"): ("float", 1),
    ("one_tick", "STP"): ("float", 1),
    ("mul_tick", "STD"): ("float", 1),
    ("static", "LTP"): ("float", 1),
    ("static", "transmitter_release_sum"): ("float", 65),
    ("static", "release_type"): ("int8", RELEASE_TYPE["excite"]),
    ("one_tick", "excite"): ("float", "RP"),
    ("one_tick", "tick_spike_times"): ("int", 0),
    ("mul_tick", "history_tick_spike_times"): ("int", 0),
    ("static", "col_no"): ("int", 0),
    ("static", "hyper_col_ind"): ("int", 0),
    ("static", "mini_col_ind"): ("int", 0),
    ("static", "ind"): ("int", -1),
    ("static", "soma_ind"): ("int", -1),
    ("static", "pre_ind"): ("int", -1),
    ("static", "post_ind"): ("int", -1),
    ("static", "post_sign"): ("int8", 1),
    ("static", "marker"): ("int", -1),
    ("static", "exinfo_0"): ("float", 0),
    ("static", "exinfo_1"): ("float", 0),
    ("static", "exinfo_2"): ("float", 0),
    ("static", "exinfo_3"): ("float", 0),
    ("static", "exinfo_4"): ("float", 0),
    ("static", "produce_marker_per_spike"): ("float", 0),
    ("static", "child_produce_marker_per_spike"): ("float", 0),
    ("one_tick", "marker_remain"): ("float", 0),
    ("one_tick", "dopamine_remain"): ("float", 0),
    ("one_tick", "seretonin_remain"): ("float", 0),
    ("one_tick", "post_synapse_LTP_sum"): ("float", 0),
    ("one_tick", "will_recv_excite"): ("int8", 0),
    # ''' 0：非全或无 1：弱全或无，传递后的兴奋的正负号要等于所传递的兴奋的正负号时才传递 2：强全或无，传递后的兴奋的正负号等于所传递的兴奋的正负号，或等于0时就传递 '''
    ("static", "all_or_none"): ("int8", 0),
    ("static", "step_length"): ("int8", 1),
    ("one_tick", "current_step"): ("int8", 1),
    ("one_tick", "refractory"): (
        "int8",
        0,
    ),  # 0：不启用不应期，1：启用不应期，2：处于不应期
    ("one_tick", "is_active"): ("int8", 0),
    ("static", "is_synapse"): (
        "int8",
        0,
    ),  # 0：不是突触 1：是突触 2：是刚刚新增或刚刚被强化的突触
    ("static", "synapse_type"): (
        "int8",
        SYNAPSE_TYPE["no_synapse"],
    ),  # -1：树突棘 0：不是突触 1：先验突触 2：预测突触 3：易化突触 4：stp突触 5：易化stp突触
    ("static", "self_synapse"): (
        "int8",
        0,
    ),  # 0：非自突触 1：是自突触，但可以被强制清除 2：是自突触，且不可被强制清除
    ("static", "spontaneous_firing"): ("int", 0),
    ("one_tick", "float_util"): ("float", 0),  # 工具矩阵
    ("one_tick", "int_util"): ("int", 0),  # 工具矩阵
    ("one_tick", "bool_util"): ("bool", False),  # 工具矩阵
    ("one_tick", "spine_active"): ("float", 0),
    ("one_tick", "anti_spine_active"): ("int", 0),
    ("one_tick", "max_circuit_length"): ("int", 0),
    ("one_tick", "max_pre_synapse_LTP"): ("float", 0),
}

PART_PROPS = {
    prop_name: part_prop_tuple(dtype, value)
    for (prop_type, prop_name), (dtype, value) in nerve_prop_meta_info.items()
}

DYNAMIC_PROP_DTYPE = [
    (prop_name, v[0])
    for (prop_type, prop_name), v in nerve_prop_meta_info.items()
    if prop_type in ["one_tick", "mul_tick"]
]
DYNAMIC_PROP_NAMES = [prop_name for prop_name, prop_dtype in DYNAMIC_PROP_DTYPE]

STATIC_PROP_DTYPE = [
    (prop_name, v[0])
    for (prop_type, prop_name), v in nerve_prop_meta_info.items()
    if prop_type == "static"
]
STATIC_PROP_NAMES = [prop_name for prop_name, prop_dtype in STATIC_PROP_DTYPE]

# 神经attribute结构化数组
PART_PROPS_KEYS_MAP = {k: i for i, k in enumerate(PART_PROPS.keys())}
PART_PROPS_DTYPE = [(k, v[0]) for k, v in PART_PROPS.items()]
PART_PROPS_MATRIX = np.array(
    [tuple(col) for col in np.array([v[1:] for k, v in PART_PROPS.items()]).T],
    PART_PROPS_DTYPE,
)
