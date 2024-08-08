import numpy as np
from .region_and_synapse import REGION_AND_SYNAPSE_META
import itertools
import math

global_axon_end_inds = {}
global_axon_end_markers = {}

VISUAL_FIELD_WH = REGION_AND_SYNAPSE_META["visual_field_wh"]
ORIENT_SUM = 16
FACE_ORIENT_SUM = ORIENT_SUM * 2
MIN_ORIENT = 360.0 / ORIENT_SUM
MIN_ANGLE = 360.0 / ORIENT_SUM

# 角
# ANGLES = np.arange(2 * MIN_ANGLE, 9 * MIN_ANGLE, MIN_ANGLE)
ANGLES = np.arange(1 * MIN_ANGLE, 9 * MIN_ANGLE, MIN_ANGLE)
ANGLE_SUM = len(ANGLES)

ORIENTS = np.arange(1, ORIENT_SUM + 1) * 360 / ORIENT_SUM
CONTOUR_CENTER_ORIENTS = ["无", *ORIENTS]
CONTOUR_OPEN_ANGLES = ["无", *np.arange(MIN_ANGLE, MIN_ANGLE * 7 + 1, MIN_ANGLE)]
BOTH_SIDE_ORIENT_DESC = [
    f"{ORIENTS[orient_ind]}_{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}"
    for orient_ind in range(ORIENT_SUM // 2)
]
PIXEL_ORIENTS = np.array([45, 90, 135, 180, 225, 270, 315, 360], float)

# TODO 无开口的内轮廓中心会导致多个属性（朝向、相对整体的朝向、相对锚点的朝向、开口角度）的值都一定为无，如果这些属性值参与了一条预测回路的形成，它们的占比会偏大，但其实它们的值都是“无”，因此可以将这些属性值变成一个，例如只有朝向有“无”的值，其他属性没有，这样就只有一个“无”值属性在链路中，让预测链路的结构更加合理
FACE_ORIENTS = ["无", *ORIENTS]
# FACE_ORIENTS = [
#     '无',
#     *(np.arange(1, FACE_ORIENT_SUM + 1) * 360 / FACE_ORIENT_SUM),
# ]

POS_ORIENTS = ["无", *ORIENTS]

RECEPTIVE_FIELD_LEVELS = np.arange(1, 21 + 1, 2)
RECEPTIVE_FIELD_LEVEL_SUM = len(RECEPTIVE_FIELD_LEVELS)
LINE_RECEPTIVE_FIELD_LEVELS = RECEPTIVE_FIELD_LEVELS[1:]
# LINE_RECEPTIVE_FIELD_LEVELS = RECEPTIVE_FIELD_LEVELS[1:-1]
SCALE_LEVEL_RATIOS = np.around(np.arange(0.1, 1 + 0.1, 0.1), 1)
CONTOUR_CENTER_RECEPTIVE_FIELD_LEVELS = RECEPTIVE_FIELD_LEVELS[1:]
CONTOUR_OPEN_SCALES = [
    "无",
    *RECEPTIVE_FIELD_LEVELS,
]

MAX_CONTOUR_OPEN_ANGLE = 135.0

CONTOUR_OPEN_ORIENT_MAP = {}
CONTOUR_OPEN_LINE_MAP = {}
for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
    CONTOUR_OPEN_LINE_MAP[receptive_field_level] = []
    for open_scale in RECEPTIVE_FIELD_LEVELS:
        """计算开口角的时候，邻边长需要小一级，否则计算结果和人的感觉会有差距"""
        邻边长 = max(1, receptive_field_level - 2)

        if 邻边长 * 2 < open_scale:
            continue
        # 根据两条邻边长和一条对边长 求角度
        open_angle = math.degrees(
            math.acos((邻边长**2 + 邻边长**2 - open_scale**2) / (2 * 邻边长 * 邻边长))
        )
        if open_angle > MAX_CONTOUR_OPEN_ANGLE:
            continue
        中垂线长 = math.sqrt(receptive_field_level**2 - (open_scale / 2) ** 2)
        中垂线尺度 = RECEPTIVE_FIELD_LEVELS[
            np.argmin(np.abs(RECEPTIVE_FIELD_LEVELS - 中垂线长))
        ]
        CONTOUR_OPEN_LINE_MAP[receptive_field_level].append(
            (
                中垂线尺度,
                open_scale,
                open_angle,
            )
        )
        CONTOUR_OPEN_ORIENT_MAP[中垂线尺度] = CONTOUR_OPEN_ORIENT_MAP.get(
            中垂线尺度, []
        )
        CONTOUR_OPEN_ORIENT_MAP[中垂线尺度].append((open_scale, open_angle))

CONTOUR_SIDES = ["内", "外"]
ORIENT_CONTOUR_SIDES = ["内", "外"]
ORIENT_SIDES = ["左", "右"]

FEATURE_TYPES = [
    "轮廓中心",
    "角",
    # '叉',
]

COMMON_ABSTRACT_TYPES_MAP = {
    "type": {
        "names": [
            "类型",
        ],
        "values": FEATURE_TYPES,
        "value_recyclable": False,
        "is_can_popu": False,
    },
    "orient": {
        "names": [
            "相对整体的方位",
            "相对锚点的方位",
        ],
        "values": POS_ORIENTS,
        "value_recyclable": 360.0,
        "value_internal": MIN_ORIENT,
    },
    "face_orient": {
        "names": [
            "朝向",
            "相对_相对整体的方位_的朝向",
            "相对_相对锚点的方位_的朝向",
        ],
        "values": FACE_ORIENTS,
        "value_recyclable": 360.0,
        "value_internal": MIN_ORIENT,
    },
    "angle": {
        "names": [
            "角度",
        ],
        "values": ["无", *ANGLES],
        "value_recyclable": False,
        "value_internal": MIN_ANGLE,
    },
    "scale": {
        "names": [
            "尺度",
        ],
        "values": RECEPTIVE_FIELD_LEVELS,
        "value_recyclable": False,
        "value_internal": RECEPTIVE_FIELD_LEVELS[1] - RECEPTIVE_FIELD_LEVELS[0],
    },
    "distance": {
        "names": [
            "相对整体中心的距离",
            "相对锚点的距离",
        ],
        "values": RECEPTIVE_FIELD_LEVELS,
        "value_recyclable": False,
        "value_internal": RECEPTIVE_FIELD_LEVELS[1] - RECEPTIVE_FIELD_LEVELS[0],
    },
    "distance_ratio": {
        "names": [
            "相对整体中心的距离相对整体尺度的比例",
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
        (f"{abstract_type_name}{abstract_value}", abstract_type_name)
        for abstract_value in common_abstract_values
    ]
    for abstract_type_name, common_abstract_values in COMMON_ABSTRACT_TYPES
}
COMMON_ABSTRACT_NAMES = list(
    itertools.chain(*COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.values())
)

ANGLE_NAMES = [
    f"方位{orient}和{(orient+angle)%360 or 360.0}的角"
    for orient in ORIENTS
    for angle in ANGLES
]
CROSS_NAMES = [
    f"方位{orient}和{(orient+angle)%360 or 360.0}的叉"
    for orient in ORIENTS
    for angle in ANGLES
]

CONTOUR_CENTER_NAMES = [
    f"朝向{orient}的{side}轮廓中心"
    for side in ["内"]
    for orient in CONTOUR_CENTER_ORIENTS
]


def sort_region(region_names):
    region_order_map = {info[0]: ind for ind, info in enumerate(COMMON_ABSTRACT_TYPES)}
    sorted_region_name_order = np.argsort([region_order_map[t] for t in region_names])
    # region_no越大的特征类型排越前面
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
