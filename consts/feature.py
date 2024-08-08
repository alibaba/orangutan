import numpy as np
import itertools
import math

global_axon_end_inds = {}
global_axon_end_markers = {}

VISUAL_FIELD_WH = [28, 28]
ORIENT_SUM = 16
FACE_ORIENT_SUM = ORIENT_SUM * 2
MIN_ORIENT = 360.0 / ORIENT_SUM
MIN_ANGLE = 360.0 / ORIENT_SUM

ANGLES = np.arange(1 * MIN_ANGLE, 9 * MIN_ANGLE, MIN_ANGLE)
ANGLE_SUM = len(ANGLES)

ORIENTS = np.arange(1, ORIENT_SUM + 1) * 360 / ORIENT_SUM
CONTOUR_CENTER_ORIENTS = ["none", *ORIENTS]
CONTOUR_OPEN_ANGLES = ["none", *np.arange(MIN_ANGLE, MIN_ANGLE * 7 + 1, MIN_ANGLE)]
BOTH_SIDE_ORIENT_DESC = [
    f"{ORIENTS[orient_ind]}_{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}"
    for orient_ind in range(ORIENT_SUM // 2)
]
PIXEL_ORIENTS = np.array([45, 90, 135, 180, 225, 270, 315, 360], float)
FACE_ORIENTS = ["none", *ORIENTS]
POS_ORIENTS = ["none", *ORIENTS]

RECEPTIVE_FIELD_LEVELS = np.arange(1, 21 + 1, 2)
RECEPTIVE_FIELD_LEVEL_SUM = len(RECEPTIVE_FIELD_LEVELS)
LINE_RECEPTIVE_FIELD_LEVELS = RECEPTIVE_FIELD_LEVELS[1:]
SCALE_LEVEL_RATIOS = np.around(np.arange(0.1, 1 + 0.1, 0.1), 1)
CONTOUR_CENTER_RECEPTIVE_FIELD_LEVELS = RECEPTIVE_FIELD_LEVELS[1:]
CONTOUR_OPEN_SCALES = [
    "none",
    *RECEPTIVE_FIELD_LEVELS,
]

MAX_CONTOUR_OPEN_ANGLE = 135.0

CONTOUR_OPEN_ORIENT_MAP = {}
CONTOUR_OPEN_LINE_MAP = {}
for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
    CONTOUR_OPEN_LINE_MAP[receptive_field_level] = []
    for open_scale in RECEPTIVE_FIELD_LEVELS:
        adjacent_side_length = max(1, receptive_field_level - 2)

        if adjacent_side_length * 2 < open_scale:
            continue
        
        open_angle = math.degrees(
            math.acos((adjacent_side_length**2 + adjacent_side_length**2 - open_scale**2) / (2 * adjacent_side_length * adjacent_side_length))
        )
        if open_angle > MAX_CONTOUR_OPEN_ANGLE:
            continue
        perpendicular_bisector_length = math.sqrt(receptive_field_level**2 - (open_scale / 2) ** 2)
        perpendicular_bisector_scale = RECEPTIVE_FIELD_LEVELS[
            np.argmin(np.abs(RECEPTIVE_FIELD_LEVELS - perpendicular_bisector_length))
        ]
        CONTOUR_OPEN_LINE_MAP[receptive_field_level].append(
            (
                perpendicular_bisector_scale,
                open_scale,
                open_angle,
            )
        )
        CONTOUR_OPEN_ORIENT_MAP[perpendicular_bisector_scale] = CONTOUR_OPEN_ORIENT_MAP.get(
            perpendicular_bisector_scale, []
        )
        CONTOUR_OPEN_ORIENT_MAP[perpendicular_bisector_scale].append((open_scale, open_angle))

CONTOUR_SIDES = ["inner", "outer"]
ORIENT_CONTOUR_SIDES = ["inner", "outer"]
ORIENT_SIDES = ["left", "right"]

FEATURE_TYPES = [
    "contour_center",
    "angle",
]

COMMON_ABSTRACT_TYPES_MAP = {
    "type": {
        "names": [
            "type",
        ],
        "values": FEATURE_TYPES,
        "value_recyclable": False,
        "is_can_popu": False,
    },
    "orient": {
        "names": [
            "relative_overall_orientation",
            "orientation_relative_to_anchor_point",
        ],
        "values": POS_ORIENTS,
        "value_recyclable": 360.0,
        "value_internal": MIN_ORIENT,
    },
    "face_orient": {
        "names": [
            "face",
            "face_relative_to_overall_orientation",
            "face_relative_to_orientation_relative_to_anchor_point",
        ],
        "values": FACE_ORIENTS,
        "value_recyclable": 360.0,
        "value_internal": MIN_ORIENT,
    },
    "angle": {
        "names": [
            "angle",
        ],
        "values": ["none", *ANGLES],
        "value_recyclable": False,
        "value_internal": MIN_ANGLE,
    },
    "scale": {
        "names": [
            "scale",
        ],
        "values": RECEPTIVE_FIELD_LEVELS,
        "value_recyclable": False,
        "value_internal": RECEPTIVE_FIELD_LEVELS[1] - RECEPTIVE_FIELD_LEVELS[0],
    },
    "distance": {
        "names": [
            "distance_relative_to_overall_center",
            "distance_relative_to_anchor_point",
        ],
        "values": RECEPTIVE_FIELD_LEVELS,
        "value_recyclable": False,
        "value_internal": RECEPTIVE_FIELD_LEVELS[1] - RECEPTIVE_FIELD_LEVELS[0],
    },
    "distance_ratio": {
        "names": [
            "proportion_of_distance_relative_to_overall_center_to_overall_scale",
        ],
        "values": SCALE_LEVEL_RATIOS,
        "value_recyclable": False,
        "value_internal": SCALE_LEVEL_RATIOS[1] - SCALE_LEVEL_RATIOS[0],
    },
}

COMMON_ABSTRACT_TYPE_NAME_MAP = {
    type_name: type_info
    for type_info in COMMON_ABSTRACT_TYPES_MAP.values()
    for type_name in type_info["names"]
}
COMMON_ABSTRACT_TYPES = []
for abstract_types_category, abstract_types_info in COMMON_ABSTRACT_TYPES_MAP.items():
    for abstract_type_name in abstract_types_info["names"]:
        COMMON_ABSTRACT_TYPES.append(
            (abstract_type_name, abstract_types_info["values"])
        )
COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES = {
    abstract_type_name: [
        (f"{abstract_type_name}_{abstract_value}", abstract_type_name)
        for abstract_value in common_abstract_values
    ]
    for abstract_type_name, common_abstract_values in COMMON_ABSTRACT_TYPES
}
COMMON_ABSTRACT_NAMES = list(
    itertools.chain(*COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.values())
)

ANGLE_NAMES = [
    f"angle_of_orientation{orient}_and_{(orient+angle)%360 or 360.0}"
    for orient in ORIENTS
    for angle in ANGLES
]
CONTOUR_CENTER_NAMES = [
    f"contour_center_of_face_oriented_{orient}_on_{side}_side"
    for side in ["inner"]
    for orient in CONTOUR_CENTER_ORIENTS
]


def sort_region(region_names):
    region_order_map = {info[0]: ind for ind, info in enumerate(COMMON_ABSTRACT_TYPES)}
    sorted_region_name_order = np.argsort([region_order_map[t] for t in region_names])
    sorted_region_names = [
        region_names[order_ind] for order_ind in sorted_region_name_order
    ]
    return sorted_region_names


ABSTRACT_EXCITE = 650
NUM_EXCITE = 100_000_000

TRANSMITTER_RELEASE_SUM_FOR_EACH_RECEPTIVE_FIELD_LEVEL = {
    receptive_field_level: 0.5 + 0.1 * (receptive_field_level // 2)
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS
}
