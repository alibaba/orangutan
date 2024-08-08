from consts.feature import (
    ANGLE_NAMES,
    FEATURE_TYPES,
)
from ...util import (
    get_soma_inds,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def induce_features_excite_positions_and_center(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type in FEATURE_TYPES:
        for feature_name in {
            "angle": ANGLE_NAMES,
            "contour_center": ["inner_contour_center", "outer_contour_center"],
        }[feature_type]:
            this_mother_inds = get_soma_inds(
                feature_type,
                f"attention_competition_result_of_{feature_name}",
            )
            mother_inds.extend(np.tile(this_mother_inds, 2))
            father_region_name = (
                "whole_center"
                if feature_name == "outer_contour_center"
                else "current_feature_position"
            )
            father_inds.extend(
                get_soma_inds(
                    father_region_name,
                    [
                        f"{y}"
                        for y in (
                            cortex_obj.cortex["region_row_no"][this_mother_inds] - 1
                        )
                    ],
                    0,
                )
            )
            father_inds.extend(
                get_soma_inds(
                    father_region_name,
                    [
                        f"{x}"
                        for x in (
                            cortex_obj.cortex["region_hyper_col_no"][this_mother_inds]
                            - 1
                        )
                    ],
                    1,
                )
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        induce_features_excite_positions_and_center,
    ]
