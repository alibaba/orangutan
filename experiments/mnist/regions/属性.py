from consts.feature import COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from consts.nerve_props import TYPE, RELEASE_TYPE, SYNAPSE_TYPE
from consts.nerve_params import ABSTRACT_TRANSMITTER_RELEASE_SUM, ABSTRACT_SYNAPSE_RP
import numpy as np
import itertools


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(np.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def get_primes(prime_sum):
    primes = []
    num = 2
    while len(primes) != prime_sum:
        if is_prime(num):
            primes.append(num)
        num += 1
    else:
        return primes


primes = get_primes(len(COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES))

PRODUCE_MARKER_PER_SPIKE = 1
CHILD_PRODUCE_MARKER_PER_SPIKE = 0.001

region_info = [
    {
        "region_name": f"属性-{prop_type}",
        "region_shape": (1, 1, 1),
        "neurons": list(
            itertools.chain(
                *[
                    [
                        *[
                            {
                                "name": f"{prop_name}{suffix}-个体编码",
                                "feature": {},
                                "dendrites": [
                                    {
                                        "name": f"$_DMin",
                                        "feature": {
                                            "type": TYPE["dendrite_min"],
                                        },
                                    },
                                    {
                                        "name": f"$_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [
                                    {
                                        "name": f"$_A激励出现和持续",
                                        "feature": {},
                                    },
                                    {
                                        "name": f"$_A禁止激励消失",
                                        "feature": {
                                            "post_sign": -1,
                                        },
                                    },
                                    {
                                        "name": f"$_A激励相对特征",
                                        "feature": {},
                                    },
                                    {
                                        "name": f"$_A禁止激励相对特征",
                                        "feature": {
                                            "post_sign": -1,
                                        },
                                    },
                                    {
                                        "name": f"$_A解禁激励相对特征",
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
                                ],
                            }
                            for prop_name, _ in prop_values
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}-个体编码出现",
                                "feature": {
                                    "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                    "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                },
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}-个体编码出现_DMin",
                                        "feature": {
                                            "type": TYPE["dendrite_min"],
                                        },
                                    },
                                ],
                                "axons": [],
                            }
                            for prop_name, _ in prop_values
                        ],
                        {
                            "name": f"个体编码出现汇总{suffix}",
                            "feature": {},
                            "axons": [],
                            "dendrites": [
                                {
                                    "name": f"个体编码出现汇总{suffix}_DMax",
                                    "feature": {
                                        "type": TYPE["dendrite_max"],
                                    },
                                },
                            ],
                        },
                        *[
                            {
                                "name": f"{prop_name}{suffix}-个体编码持续",
                                "feature": {},
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}-个体编码持续_DMin",
                                        "feature": {
                                            "type": TYPE["dendrite_min"],
                                        },
                                    },
                                ],
                                "axons": [
                                    {
                                        "name": f"{prop_name}{suffix}-个体编码持续A禁止激励出现",
                                        "feature": {
                                            "post_sign": -1,
                                        },
                                    },
                                ],
                            }
                            for prop_name, _ in prop_values
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}-个体编码消失",
                                "feature": {},
                                "axons": [],
                            }
                            for prop_name, _ in prop_values
                        ],
                        {
                            "name": f"个体编码消失汇总{suffix}",
                            "feature": {},
                            "axons": [],
                            "dendrites": [
                                {
                                    "name": f"个体编码消失汇总{suffix}_DMax",
                                    "feature": {
                                        "type": TYPE["dendrite_max"],
                                    },
                                },
                            ],
                        },
                        *[
                            {
                                "name": f"{prop_name}{suffix}-群体编码",
                                "feature": {},
                                "dendrites": [
                                    {
                                        "name": f"$_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [],
                            }
                            for prop_name, _ in prop_values
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}-群体编码出现",
                                "feature": {
                                    "RP": ABSTRACT_SYNAPSE_RP,
                                    "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                    "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                    "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                    "exinfo_0": primes[
                                        abstract_type_ind
                                    ],  # 用一个质数作为这一类属性的数字标识，用于建立突触回路时的防重逻辑
                                },
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码出现_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码出现_A前馈预测",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": ABSTRACT_TRANSMITTER_RELEASE_SUM,
                                            "exinfo_0": 0,  # 建立突触时是否考虑质数冲突，0不是，1是
                                            "exinfo_1": SYNAPSE_TYPE["excite"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码出现_A易化前馈预测",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                            # 'release_type':
                                            # RELEASE_TYPE['Fa'],
                                            # ABSTRACT_TRANSMITTER_RELEASE_SUM,
                                            "exinfo_0": 1,  # 建立突触时是否考虑质数冲突，0不是，1是
                                            "exinfo_1": SYNAPSE_TYPE["Fa"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码出现_A转运标记物",
                                        "feature": {
                                            "release_type": RELEASE_TYPE["marker"],
                                            "transmitter_release_sum": 0.1,
                                        },
                                    },
                                ],
                            }
                            for abstract_ind, [prop_name, _] in enumerate(prop_values)
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}-群体编码持续",
                                "feature": {},
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码持续_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [],
                            }
                            for prop_name, _ in prop_values
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}-群体编码消失",
                                "feature": {
                                    "RP": ABSTRACT_SYNAPSE_RP,
                                    "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                    "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                    "exinfo_0": primes[abstract_type_ind],
                                },
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码消失_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码消失_Astp预测",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": ABSTRACT_TRANSMITTER_RELEASE_SUM,
                                            "release_type": RELEASE_TYPE["STP"],
                                            "exinfo_0": 0,  # 建立突触时是否考虑质数冲突，0不是，1是
                                            "exinfo_1": SYNAPSE_TYPE["STP"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                    {
                                        "name": f"{prop_name}{suffix}-群体编码消失_A易化stp预测",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                            # 'release_type':
                                            # RELEASE_TYPE['Fa'],
                                            # ABSTRACT_TRANSMITTER_RELEASE_SUM,
                                            "exinfo_0": 1,  # 建立突触时是否考虑质数冲突，0不是，1是
                                            "exinfo_1": SYNAPSE_TYPE["Fa_STP"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                ],
                            }
                            for abstract_ind, [prop_name, _] in enumerate(prop_values)
                        ],
                    ]
                    for suffix in ["", "-泛化"]
                ]
            )
        ),
    }
    for abstract_type_ind, (prop_type, prop_values) in enumerate(
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
    )
]
