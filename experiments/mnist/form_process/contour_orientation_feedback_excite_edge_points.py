from consts.feature import ORIENTS, RECEPTIVE_FIELD_LEVELS, ORIENT_SIDES
from ...util import get_soma_inds
from ...form_nerve.form_nerve import form_nerve
from .various_points_excite_various_orientations import get_receptive_field_infos


def get_matrix_params(level):
    return {
        3: [225, 3],
        5: [135, 2],
        7: [90, 2],
        9: [45, 2],
        11: [45, 2],
    }.get(level, [None, None])


def feedback_excite_edge_points_by_contour_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        [orient_range, receptive_field_level_range] = get_matrix_params(
            receptive_field_level
        )
        for orient_ind, orient in enumerate(ORIENTS):
            (
                around_pos_inds,
                center_pos_inds,
                gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
                sum_gray_axon_end_release_sum,
            ) = get_receptive_field_infos(
                orient,
                receptive_field_level,
                orient_range=orient_range,
                receptive_field_level_range=receptive_field_level_range,
            )
            for father_orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_inner_contour_feedback",
                        center_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        "point",
                        f"edge_points_in_{father_orient}_direction_feedback_DMax",
                        around_pos_inds,
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def feedback_excite_edge_points_by_vertical_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        [orient_range, receptive_field_level_range] = get_matrix_params(
            receptive_field_level
        )
        for orient_ind, orient in enumerate(ORIENTS):
            (
                around_pos_inds,
                center_pos_inds,
                gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
                sum_gray_axon_end_release_sum,
            ) = get_receptive_field_infos(
                orient,
                receptive_field_level,
                orient_range=orient_range,
                receptive_field_level_range=receptive_field_level_range,
            )
            for orient_side in ORIENT_SIDES:
                for father_orient in ORIENTS:
                    mother_inds.extend(
                        get_soma_inds(
                            f"orientation-S{receptive_field_level}",
                            f"orientation_of_{orient}_direction_{orient_side}_side_feedback",
                            center_pos_inds,
                        )
                    )
                    father_inds.extend(
                        get_soma_inds(
                            "point",
                            f"edge_points_in_{father_orient}_direction_feedback_DMax",
                            around_pos_inds,
                        )
                    )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        feedback_excite_edge_points_by_contour_orientation,
        feedback_excite_edge_points_by_vertical_orientation,
    ]
