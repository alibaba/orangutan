import numpy as np
from consts.feature import VISUAL_FIELD_WH, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE
from experiments.util import get_soma_inds

APPEAR_NERVE_SUFFIXs = [
    "popu_coding_appear",
    "popu_coding_appear_A_feedforward_prediction",
    "popu_coding_appear_A_facilitate_feedforward_prediction",
]
DISAPPEAR_NERVE_SUFFIXs = [
    "popu_coding_disappear",
    "popu_coding_disappear_Astp_prediction",
    "popu_coding_disappear_A_facilitate_stp_prediction",
]

POPU_ABSTRACT_APPEAR_INDS = np.concatenate(
    tuple(
        [
            get_soma_inds(
                f"attribute-{abstract_type}",
                [
                    f"{abstract_name}_popu_coding_appear",
                ],
            )
            for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]
    )
)

POPU_ABSTRACT_DISAPPEAR_INDS = np.concatenate(
    tuple(
        [
            get_soma_inds(
                f"attribute-{abstract_type}",
                [
                    f"{abstract_name}_popu_coding_disappear",
                ],
            )
            for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]
    )
)

GENERATIVE_POPU_ABSTRACT_APPEAR_INDS = np.concatenate(
    tuple(
        [
            get_soma_inds(
                f"attribute-{abstract_type}",
                [
                    f"{abstract_name}_generalization_popu_coding_appear",
                ],
            )
            for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]
    )
)

GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS = np.concatenate(
    tuple(
        [
            get_soma_inds(
                f"attribute-{abstract_type}",
                [
                    f"{abstract_name}_generalization_popu_coding_disappear",
                ],
            )
            for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]
    )
)

POPU_ABSTRACT_DISAPPEAR_STP_INDS = np.concatenate(
    tuple(
        [
            get_soma_inds(
                f"attribute-{abstract_type}",
                [
                    f"{abstract_name}_popu_coding_disappear_Astp_prediction",
                ],
            )
            for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]
    )
)

NOWA_FEATURE_GRID_INDS = get_soma_inds(
    "current_feature_position", [f"{y_or_x}" for y_or_x in range(VISUAL_FIELD_WH[0])]
)

ANCHOR_FEATURE_GRID_INDS = get_soma_inds(
    "anchor_point_feature_position",
    [f"{y_or_x}" for y_or_x in range(VISUAL_FIELD_WH[0])],
)

WHOLE_CENTER_GRID_INDS = get_soma_inds(
    "whole_center", [f"{y_or_x}" for y_or_x in range(VISUAL_FIELD_WH[0])]
)

SINGLE_ABSTRACT_APPEAR_INDS = np.concatenate(
    tuple(
        [
            get_soma_inds(
                f"attribute-{abstract_type}", f"{abstract_name}_single_coding_appear"
            )
            for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]
    )
)

PREDICT_INDS = get_soma_inds(
    "number", [f"fore_predict_DMax_spine{i}" for i in range(SPINE_SUM_ON_A_DENDRITE)]
)
PREDICT_INDS.sort()
PREDICT_SUPRISE_INDS = get_soma_inds("number", "fore_predict_unexpected")
PREDICT_BIAS_INDS = get_soma_inds("number", "fore_predict_bias")
ACCUMULATE_PREDICT_INDS = get_soma_inds("number", "accumulate_fore_predict")
