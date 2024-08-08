from consts.feature import VISUAL_FIELD_WH, ORIENTS
from consts.nerve_props import TYPE, RELEASE_TYPE

region_info = {
    "region_name": "point",
    "region_shape": (*VISUAL_FIELD_WH, 1),
    "neurons": [
        {
            "name": "input",
            "axons": [
                {
                    "name": "$_A_inhibit",
                    "feature": {
                        "post_sign": -1,
                    },
                },
            ],
        },
        *[
            {
                "name": f"edge_points_in_{orient}_direction",
            }
            for orient in ORIENTS
        ],
        *[
            {
                "name": f"edge_points_in_{orient}_direction_feedback",
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
                        "name": f"$_ASTD",
                        "feature": {
                            "release_type": RELEASE_TYPE["STD"],
                        },
                    },
                ],
            }
            for orient in ORIENTS
        ],
    ],
}
