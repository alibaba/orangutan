from consts.feature import ORIENT_SUM, BOTH_SIDE_ORIENT_DESC
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves, REGION
from ...form_nerve.form_nerve import form_nerve
import numpy as np

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def is_orient_in_range(line_orient, left_open_orient, right_open_orient):
    if left_open_orient < right_open_orient:
        return left_open_orient < line_orient < right_open_orient
    else:
        return left_open_orient < line_orient or line_orient < right_open_orient


def get_opposite_orient_ind(orient_ind):
    return (orient_ind + ORIENT_SUM // 2) % ORIENT_SUM


def get_opposite_orient(orient):
    return (orient + 180.0) % 360.0 or 360.0


def excite_contour_center_with_line(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "antipodal_points",
                f"summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell",
            )
        )
        father_inds.extend(
            get_soma_inds(
                f"contour_center",
                f"{side}_contour_center_DAdd",
            )
        )
        axon_end_release_sums.extend(
            [65 / (ORIENT_SUM // 2)] * REGION[f"contour_center"]["hyper_col_sum"]
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "excite_contour_center_with_line"
        ),
    )


def inhibit_and_excite_contour_center_with_line(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "antipodal_points",
                f"summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell_A_inhibit",
            )
        )
    father_inds = axon_end_inds["excite_contour_center_with_line"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "inhibit_and_excite_contour_center_with_line"
        ),
    )


def antagonistic_inhibition_of_contour_center_by_inner_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "orientation",
                f"inner_contour_orientation_summary_{BOTH_SIDE_ORIENT_DESC[(orient_ind+4)%(ORIENT_SUM//2)]}_A_all_or_none_inhibit",
            )
        )
        axon_end_release_sums.extend(
            [65 * 5] * REGION[f"contour_center"]["hyper_col_sum"]
        )
    father_inds = axon_end_inds["inhibit_and_excite_contour_center_with_line"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def excite_entire_contour_center_with_contour_line(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for both_orient_ind in range(ORIENT_SUM // 2):
        each_axon_end_release_sum = 65 / (ORIENT_SUM // 2)
        mother_inds.extend(
            get_soma_inds(
                "antipodal_points",
                f"summary_{BOTH_SIDE_ORIENT_DESC[both_orient_ind]}_direction_outer_contour_straight_line_complex_cell",
            )
        )
        father_inds.extend(
            get_soma_inds(
                "contour_center",
                "outer_contour_center",
            )
        )
        axon_end_release_sums.extend(
            [each_axon_end_release_sum] * REGION["antipodal_points"]["hyper_col_sum"]
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def form_init_nerve():
    return [
        excite_contour_center_with_line,
        inhibit_and_excite_contour_center_with_line,
        antagonistic_inhibition_of_contour_center_by_inner_orientation,
        excite_entire_contour_center_with_contour_line,
    ]
