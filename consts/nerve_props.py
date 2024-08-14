import numpy as np
from .nerve_params import SRP, NRP

# neural type
TYPE = {
    type_name: type_ind
    for type_ind, type_name in enumerate(
        [
            "soma",  # soma
            "axon",  # axon
            "axon_end",  # axonend
        ]
    )
}
DENDRITE_TYPE = {
    type_name: type_ind + len(TYPE)
    for type_ind, type_name in enumerate(
        [
            "dendrite_min",  # min dendrite
            "dendrite_max",  # max dendrite
            "dendrite_add",  # add dendrite
            "dendrite_weight",  # weight add dendrite
            "dendrite_multi",  #  dendrite
        ]
    )
}
TYPE.update(DENDRITE_TYPE)
TYPE.update({"spine_connect": len(TYPE)})
STATIC_TYPES = [TYPE["soma"], TYPE["axon"], *DENDRITE_TYPE.values()]

# 0: Non-synaptic 1: Presynaptic 2: Postsynaptic 3: Facilitated 4: STP (Short-Term Plasticity) 5: Facilitated STP (Short-Term Plasticity)
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

# neural attribute
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

# TODO Translation: In non-learning mode, some attributes that are not needed do not need to be initialized, saving computational resources.
# At the same time, it is also possible to omit some calculation steps in the cortex calculation process to speed up the calculation speed.
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
    # ''' 0: Not all or none 1: Weak all or none, the sign of the transmitted excitation must be equal to the sign of the excitation transmitted in order to be transmitted 2: Strong all or none, the sign of the transmitted excitation is equal to the sign of the transmitted excitation, or equal to 0 if transmitted
    ("static", "all_or_none"): ("int8", 0),
    ("static", "step_length"): ("int8", 1),
    ("one_tick", "current_step"): ("int8", 1),
    ("one_tick", "refractory"): (
        "int8",
        0,
    ),  # 0: No grace period enabled, 1: Grace period enabled, 2: In grace period
    ("one_tick", "is_active"): ("int8", 0),
    ("static", "is_synapse"): (
        "int8",
        0,
    ),  # 0: Not a synapse 1: Is a synapse 2: Is a newly added or recently strengthened synapse
    ("static", "synapse_type"): (
        "int8",
        SYNAPSE_TYPE["no_synapse"],
    ),  # -1：Dendritic spine 0：Not a synapse 1：Primer synapse 2：Predictive synapse 3：Facilitated synapse 4：STP synapse 5：Facilitated STP synapse
    ("static", "self_synapse"): (
        "int8",
        0,
    ),  # 0: Non-autonomous synapse 1: Autonomus synapse, but can be forcibly cleared 2: Autonomus synapse, and cannot be forcibly cleared
    ("static", "spontaneous_firing"): ("int", 0),
    ("one_tick", "float_util"): ("float", 0),  # tool matrix
    ("one_tick", "int_util"): ("int", 0),  # tool matrix
    ("one_tick", "bool_util"): ("bool", False),  # tool matrix
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

# Structured array of attributed nerves.
PART_PROPS_KEYS_MAP = {k: i for i, k in enumerate(PART_PROPS.keys())}
PART_PROPS_DTYPE = [(k, v[0]) for k, v in PART_PROPS.items()]
PART_PROPS_MATRIX = np.array(
    [tuple(col) for col in np.array([v[1:] for k, v in PART_PROPS.items()]).T],
    PART_PROPS_DTYPE,
)
