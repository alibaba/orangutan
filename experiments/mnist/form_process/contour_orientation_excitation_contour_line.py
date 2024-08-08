from consts.feature import (
    ORIENT_SUM,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    BOTH_SIDE_ORIENT_DESC,
    ORIENT_CONTOUR_SIDES,
)
from ...util import (
    REGION,
    get_soma_inds,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def excite_contour_line_with_contour_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        receptive_field_levels = RECEPTIVE_FIELD_LEVELS
        for receptive_field_level in receptive_field_levels:
            level = receptive_field_level
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{level}",
                    [
                        f"orientation_of_{ORIENTS[orient_ind]}_direction_{side}_contour",
                        f"orientation_of_{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}_direction_{side}_contour",
                        #
                        f"orientation_of_{ORIENTS[orient_ind]}_direction_{side}_contour_complex_cell",
                        f"orientation_of_{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}_direction_{side}_contour_complex_cell",
                    ],
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"antipodal_points-S{receptive_field_level}",
                    [
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}_direction_{side}_contour_straight_line_DMax{ORIENTS[orient_ind]}_direction",
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}_direction_{side}_contour_straight_line_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}_direction",
                        #
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}_direction_{side}_contour_straight_line_complex_cell_DMax{ORIENTS[orient_ind]}_direction",
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}_direction_{side}_contour_straight_line_complex_cell_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}_direction",
                    ],
                )
            )

            axon_end_release_sums.extend(
                [65 * 2 * (0.6 + 0.15 * (receptive_field_level // 2))]
                * REGION[f"orientation-S{level}"]["hyper_col_sum"]
                * 4
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def is_orient_in_range(line_orient, left_open_orient, right_open_orient):
    if left_open_orient < right_open_orient:
        return left_open_orient < line_orient < right_open_orient
    else:
        return left_open_orient < line_orient or line_orient < right_open_orient


def get_opposite_orient_ind(orient_ind):
    return (orient_ind + ORIENT_SUM // 2) % ORIENT_SUM


def get_opposite_orient(orient):
    return (orient + 180.0) % 360.0 or 360.0


def summarize_contour_lines_across_orientations_and_scales(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind in range(ORIENT_SUM // 2):
        for side in ORIENT_CONTOUR_SIDES:
            if side == "inner":
                receptive_field_levels = RECEPTIVE_FIELD_LEVELS
            else:
                receptive_field_levels = RECEPTIVE_FIELD_LEVELS[3:]
            for receptive_field_level in receptive_field_levels:
                mother_inds.extend(
                    get_soma_inds(
                        f"antipodal_points-S{receptive_field_level}",
                        [
                            f"{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line",
                            f"{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell",
                        ],
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        "antipodal_points",
                        [
                            f"summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_DMax",
                            f"summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell_DMax",
                        ],
                    )
                )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        excite_contour_line_with_contour_orientation,
        summarize_contour_lines_across_orientations_and_scales,
    ]
