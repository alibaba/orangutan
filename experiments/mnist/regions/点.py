from consts.feature import VISUAL_FIELD_WH, ORIENTS
from consts.nerve_props import TYPE, RELEASE_TYPE

region_info = {
    "region_name": "点",
    "region_shape": (*VISUAL_FIELD_WH, 1),
    "neurons": [
        {
            "name": "input",
            "axons": [
                {
                    "name": "$_A抑制",
                    "feature": {
                        "post_sign": -1,
                    },
                },
            ],
        },
        *[
            {
                "name": f"{orient}方向的边缘点",
            }
            for orient in ORIENTS
        ],
        *[
            {
                "name": f"{orient}方向的边缘点_反馈",
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
