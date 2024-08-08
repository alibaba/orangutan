from consts.feature import ABSTRACT_EXCITE
from consts.nerve_props import TYPE, RELEASE_TYPE
from consts.nerve_params import PIXEL_MAX_EXCITE

region_info = {
    "region_name": "global_control",
    "region_shape": (1, 1, 1),
    "neurons": [
        *[
            {
                "name": f"attention_competition_excitation_summary{suffix}",
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
                        "name": "$_A_all_or_none_weak_inhibition",
                        "feature": {
                            "post_sign": -1,
                            "all_or_none": 1,
                        },
                    },
                ],
            }
            for suffix in ["", "_outer_contour_center"]
        ],
        {
            "name": "shared_regulation_excitation",
            "feature": {
                "excite": 0,
                "self_synapse": 2,
            },
            "axons": [
                {
                    "name": "$_A_self_sustaining",
                    "feature": {},
                },
                {
                    "name": "$_A_control_attention_competition_start_timing",
                    "feature": {
                        "step_length": 8,
                        "transmitter_release_sum": 100000000,
                    },
                },
            ],
        },
        {
            "name": "summarize_inner_contour_orientations_with_feedback_at_curve_edges",
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
                    "name": "$_A_inhibit",
                    "feature": {
                        "post_sign": -1,
                    },
                },
            ],
        },
        {
            "name": "apply_antagonistic_inhibition_to_orientation_excitation_rays",
            "feature": {
                "excite": PIXEL_MAX_EXCITE / 3,
                "self_synapse": 2,
            },
            "dendrites": [],
            "axons": [
                {
                    "name": "$_A_inhibit",
                    "feature": {
                        "post_sign": -1,
                    },
                },
            ],
        },
    ],
}
