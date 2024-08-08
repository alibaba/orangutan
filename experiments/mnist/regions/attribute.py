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
        "region_name": f"attribute-{prop_type}",
        "region_shape": (1, 1, 1),
        "neurons": list(
            itertools.chain(
                *[
                    [
                        *[
                            {
                                "name": f"{prop_name}{suffix}_single_coding",
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
                                        "name": f"$_A_all_or_none_weak_inhibition",
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
                                "name": f"{prop_name}{suffix}_single_coding_appear",
                                "feature": {
                                    "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                    "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                },
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}_single_coding_appear_DMin",
                                        "feature": {
                                            "type": TYPE["dendrite_min"],
                                        },
                                    },
                                ],
                                "axons": [],
                            }
                            for prop_name, _ in prop_values
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}_popu_coding",
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
                                "name": f"{prop_name}{suffix}_popu_coding_appear",
                                "feature": {
                                    "RP": ABSTRACT_SYNAPSE_RP,
                                    "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                    "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                    "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                    "exinfo_0": primes[
                                        abstract_type_ind
                                    ],
                                },
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}_popu_coding_appear_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [
                                    {
                                        "name": f"{prop_name}{suffix}_popu_coding_appear_A_feedforward_prediction",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": ABSTRACT_TRANSMITTER_RELEASE_SUM,
                                            "exinfo_0": 0,
                                            "exinfo_1": SYNAPSE_TYPE["excite"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                    {
                                        "name": f"{prop_name}{suffix}_popu_coding_appear_A_facilitate_feedforward_prediction",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                            "exinfo_0": 1,
                                            "exinfo_1": SYNAPSE_TYPE["Fa"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                ],
                            }
                            for abstract_ind, [prop_name, _] in enumerate(prop_values)
                        ],
                        *[
                            {
                                "name": f"{prop_name}{suffix}_popu_coding_disappear",
                                "feature": {
                                    "RP": ABSTRACT_SYNAPSE_RP,
                                    "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                    "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                    "exinfo_0": primes[abstract_type_ind],
                                },
                                "dendrites": [
                                    {
                                        "name": f"{prop_name}{suffix}_popu_coding_disappear_DMax",
                                        "feature": {
                                            "type": TYPE["dendrite_max"],
                                        },
                                    },
                                ],
                                "axons": [
                                    {
                                        "name": f"{prop_name}{suffix}_popu_coding_disappear_Astp_prediction",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": ABSTRACT_TRANSMITTER_RELEASE_SUM,
                                            "release_type": RELEASE_TYPE["STP"],
                                            "exinfo_0": 0,
                                            "exinfo_1": SYNAPSE_TYPE["STP"],
                                            "spontaneous_firing": 1,
                                            "produce_marker_per_spike": PRODUCE_MARKER_PER_SPIKE,
                                            "child_produce_marker_per_spike": CHILD_PRODUCE_MARKER_PER_SPIKE,
                                        },
                                    },
                                    {
                                        "name": f"{prop_name}{suffix}_popu_coding_disappear_A_facilitate_stp_prediction",
                                        "feature": {
                                            "RP": ABSTRACT_SYNAPSE_RP,
                                            "transmitter_release_sum": -ABSTRACT_SYNAPSE_RP,
                                            "exinfo_0": 1,
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
                    for suffix in ["", "_generalization"]
                ]
            )
        ),
    }
    for abstract_type_ind, (prop_type, prop_values) in enumerate(
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
    )
]
