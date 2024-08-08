from consts.feature import (
    ORIENT_SUM,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    global_axon_end_inds,
    ORIENT_SIDES,
    BOTH_SIDE_ORIENT_DESC,
    LINE_RECEPTIVE_FIELD_LEVELS,
)
from ...util import (
    get_soma_inds,
    save_axon_end_inds_with_new_nerves,
    REGION,
    get_around_and_center_hyper_col_inds_with_around_mask,
    get_orient_distance_matrix,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def get_gray_matrix(
    orient, receptive_field_level, orient_range=None, receptive_field_level_range=None
):

    if orient_range == None:
        orient_range = 25
    if receptive_field_level_range == None:
        receptive_field_level_range = 2

    matrix_shape = (receptive_field_level, receptive_field_level)
    half_receptive_field_level = receptive_field_level // 2 + 1
    base_axis = np.arange(-(matrix_shape[0] // 2), matrix_shape[0] // 2 + 1)

    orient_distance_ratio_matrix = get_orient_distance_matrix(
        orient, receptive_field_level, orient_range
    )

    receptive_field_level_matrix = np.array(
        [
            np.linalg.norm([x + np.sign(x), y + np.sign(y)])
            for y in base_axis[::-1]
            for x in base_axis
        ]
    ).reshape(matrix_shape)
    receptive_field_level_ratio_matrix = (
        np.maximum(
            0,
            receptive_field_level_range
            - np.abs(half_receptive_field_level - receptive_field_level_matrix),
        )
        / receptive_field_level_range
    )

    ratio_matrix = orient_distance_ratio_matrix * receptive_field_level_ratio_matrix

    if half_receptive_field_level == 1:
        ratio_matrix[matrix_shape[0] // 2, matrix_shape[0] // 2] = 1

    gray_matrix = 255 * ratio_matrix
    max_gray_matrix = 255 * gray_matrix / np.max(gray_matrix)
    sum_gray_matrix = 255 * gray_matrix / np.sum(gray_matrix)

    return gray_matrix, max_gray_matrix, sum_gray_matrix


def filter_matrix(matrix):
    matrix[matrix <= 255 / 2] = 0
    return matrix


def fix_size(matrix, targ_size):
    new_matrix = np.full((targ_size, targ_size), 0)
    matrix_size = matrix.shape[0]
    start_pos = (targ_size - matrix_size) // 2
    new_matrix[
        start_pos : start_pos + matrix_size, start_pos : start_pos + matrix_size
    ] = matrix
    return new_matrix


def get_gray_axon_end_release_sum(
    gray_matrix, max_gray_matrix, sum_gray_matrix, inrange_mother_pos_mask
):
    gray_axon_end_release_sum_matrix = (
        gray_matrix[np.newaxis, :, :] / 255 * 65 * inrange_mother_pos_mask.astype(int)
    )
    gray_axon_end_release_sum = gray_axon_end_release_sum_matrix[
        gray_axon_end_release_sum_matrix > 0
    ]

    max_gray_axon_end_release_sum_matrix = (
        max_gray_matrix[np.newaxis, :, :]
        / 255
        * 65
        * inrange_mother_pos_mask.astype(int)
    )
    max_gray_axon_end_release_sum = max_gray_axon_end_release_sum_matrix[
        max_gray_axon_end_release_sum_matrix > 0
    ]

    sum_gray_axon_end_release_sum_matrix = (
        sum_gray_matrix[np.newaxis, :, :]
        / 255
        * 65
        * inrange_mother_pos_mask.astype(int)
    )
    sum_gray_axon_end_release_sum = sum_gray_axon_end_release_sum_matrix[
        sum_gray_axon_end_release_sum_matrix > 0
    ]

    return (
        gray_axon_end_release_sum,
        max_gray_axon_end_release_sum,
        sum_gray_axon_end_release_sum,
    )


def get_receptive_field_infos(
    orient, receptive_field_level, orient_range=None, receptive_field_level_range=None
):
    gray_matrix, max_gray_matrix, sum_gray_matrix = get_gray_matrix(
        orient,
        receptive_field_level,
        orient_range=orient_range,
        receptive_field_level_range=receptive_field_level_range,
    )
    around_pos_inds, center_pos_inds, inrange_mother_pos_mask = (
        get_around_and_center_hyper_col_inds_with_around_mask(
            "point", f"orientation-S{receptive_field_level}", max_gray_matrix > 255 / 2
        )
    )
    (
        gray_axon_end_release_sum,
        max_gray_axon_end_release_sum,
        sum_gray_axon_end_release_sum,
    ) = get_gray_axon_end_release_sum(
        gray_matrix, max_gray_matrix, sum_gray_matrix, inrange_mother_pos_mask
    )
    return (
        around_pos_inds,
        center_pos_inds,
        gray_axon_end_release_sum,
        max_gray_axon_end_release_sum,
        sum_gray_axon_end_release_sum,
    )


def stimulus_contour_orientation(side):

    def stimulus_function(cortex_obj):
        mother_inds, father_inds, axon_end_release_sums = [], [], []
        for orient_ind, orient in enumerate(ORIENTS):
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
                (
                    around_pos_inds,
                    center_pos_inds,
                    gray_axon_end_release_sum,
                    _,
                    _,
                ) = get_receptive_field_infos(orient, receptive_field_level)

                mother_orient = {
                    "inner": ORIENTS[int((orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)],
                    "outer": orient,
                }[side]
                mother_inds.extend(
                    get_soma_inds(
                        "point",
                        f"edge_points_in_{mother_orient}_direction",
                        around_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_{side}_contour_DMax",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(gray_axon_end_release_sum)
        return form_nerve.make_new_nerve_packs(
            mother_inds,
            father_inds,
            cortex_obj,
            reset_nerve_props_matrix=np.array(
                axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
            ),
            new_nerve_callback=save_axon_end_inds_with_new_nerves(
                global_axon_end_inds, f"stimulus_{side}_contour_orientation"
            ),
        )

    return stimulus_function


def stimulus_contour_orientation_sum_value(side):

    def stimulus_function(cortex_obj):
        mother_inds, father_inds, axon_end_release_sums = [], [], []
        for orient_ind, orient in enumerate(ORIENTS):
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:

                (
                    around_pos_inds,
                    center_pos_inds,
                    gray_axon_end_release_sum,
                    _,
                    _,
                ) = get_receptive_field_infos(orient, receptive_field_level)

                mother_orient = {
                    "inner": ORIENTS[int((orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)],
                    "outer": orient,
                }[side]
                mother_inds.extend(
                    get_soma_inds(
                        "point",
                        f"edge_points_in_{mother_orient}_direction",
                        around_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_{side}_contour_sum_value",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(gray_axon_end_release_sum)
        return form_nerve.make_new_nerve_packs(
            mother_inds,
            father_inds,
            cortex_obj,
            reset_nerve_props_matrix=np.array(
                axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
            ),
        )

    return stimulus_function


def summarize_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            if receptive_field_level == 1:
                continue
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"orientation_of_{orient}_direction_inner_contour",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation", f"inner_contour_orientation_summary_{orient}_DMax"
                )
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def summarize_inner_contour_orientation_with_scale_1(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(
                f"orientation-S1",
                f"orientation_of_{orient}_direction_inner_contour",
            )
        )
        father_inds.extend(
            get_soma_inds(
                f"orientation",
                f"inner_contour_orientation_summary_{orient}_DMax",
            )
        )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            global_axon_end_inds, "summarize_inner_contour_orientation_with_scale_1"
        ),
    )


def summarize_max_of_rays_in_all_directions(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side_A_excitation_with_step_length_2",
                    )
                )
                father_inds.extend(
                    get_soma_inds(f"ray", f"summarize_max_values_of_all_rays_DMax")
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def excite_and_maintain_all_rays_synapses(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(
        get_soma_inds(
            f"ray",
            [
                f"summarize_max_values_of_all_rays_A_excitation_of_step0",
                f"summarize_max_values_of_all_rays_autapse",
            ],
        )
    )
    father_inds.extend(
        get_soma_inds(f"ray", [f"summarize_max_values_of_all_rays_autapse_DMax"] * 2)
    )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inhibit_all_rays_summarize_inner_contour_orientation_with_scale_1_autapse(
    cortex_obj,
):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(f"ray", f"summarize_max_values_of_all_rays_autapse_A_inhibit")
        )
    father_inds = global_axon_end_inds[
        "summarize_inner_contour_orientation_with_scale_1"
    ]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def summarize_contralateral_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds = [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                f"orientation",
                [
                    f"inner_contour_orientation_summary_{ORIENTS[orient_ind]}",
                    f"inner_contour_orientation_summary_{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}",
                ],
            )
        )
        father_inds.extend(
            get_soma_inds(
                f"orientation",
                [
                    f"inner_contour_orientation_summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_DMax",
                ]
                * 2,
            )
        )

    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
    )


def excite_inner_contour_orientation_complex_cells(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            for sub_receptive_field_level in [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if abs(level - receptive_field_level) <= 2
            ]:
                receptive_field_level_ratio = (
                    max(
                        0,
                        receptive_field_level
                        - abs(receptive_field_level - sub_receptive_field_level),
                    )
                    / receptive_field_level
                )
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{sub_receptive_field_level}",
                        f"orientation_of_{orient}_direction_inner_contour",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_inner_contour_complex_cell_DMax",
                    )
                )
                axon_end_release_sums.extend(
                    [65 * receptive_field_level_ratio]
                    * REGION[f"orientation-S{receptive_field_level}"]["hyper_col_sum"]
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def stimulate_vertical_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            (
                around_pos_inds,
                center_pos_inds,
                gray_axon_end_release_sum,
                _,
                _,
            ) = get_receptive_field_infos(orient, receptive_field_level)

            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        "point",
                        f'edge_points_in_{ORIENTS[int((orient_ind + {"left":-1,"right":1}[orient_side]*ORIENT_SUM  / 4) % ORIENT_SUM)]}_direction',
                        around_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_{orient_side}_side_DMax",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(gray_axon_end_release_sum)
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            global_axon_end_inds, "stimulate_vertical_orientation"
        ),
    )


def inhibit_inner_contour_orientation_with_smaller_scale_outer_contour_orientation(
    cortex_obj,
):
    mother_inds, father_inds = [], []
    inhibit_side = "outer"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            lower_levels = [
                lower_level
                for lower_level in RECEPTIVE_FIELD_LEVELS
                if lower_level <= receptive_field_level and lower_level > 1
            ]
            for lower_level in lower_levels:
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{lower_level}",
                        f"orientation_of_{orient}_direction_{inhibit_side}_contour_autapse",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_inner_contour_DMax_inhibit",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inhibit_inner_contour_orientation_with_smaller_scale_inner_contour_orientation(
    cortex_obj,
):
    mother_inds, father_inds = [], []
    inhibit_side = "inner"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            lower_levels = [
                lower_level
                for lower_level in RECEPTIVE_FIELD_LEVELS
                if lower_level < (receptive_field_level - 2)
            ]
            for lower_level in lower_levels:
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{lower_level}",
                        f"orientation_of_{orient}_direction_{inhibit_side}_contour_autapse",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"orientation_of_{orient}_direction_inner_contour_DMax_inner_contour_inhibit",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def summarize_inner_contour_orientation_by_scale(cortex_obj):
    mother_inds, father_inds = [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient in ORIENTS:
            for level in [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if level <= receptive_field_level
            ]:
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{level}",
                        f"orientation_of_{orient}_direction_inner_contour",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"summary_of_{orient}_direction_inner_scale_inner_contour_orientation_DMax",

                    )
                )
                #
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{level}",
                        f"orientation_of_{orient}_direction_inner_contour_sum_value",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        f"summary_of_{orient}_direction_inner_scale_inner_contour_orientation_sum_value_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def stimulate_inner_contour_orientation_with_std(cortex_obj):
    mother_inds, father_inds = [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, _, _, _, _ = get_receptive_field_infos(
                orient, receptive_field_level
            )
            mother_orient = ORIENTS[int((orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)]
            mother_inds.extend(
                get_soma_inds(
                    "point",
                    f"edge_points_in_{mother_orient}_direction_feedback_ASTD",
                    around_pos_inds,
                )
            )
    father_inds = global_axon_end_inds["stimulus_inner_contour_orientation"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def STD_stimulate_vertical_orientation(cortex_obj):
    mother_inds, father_inds = [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, _, _, _, _ = get_receptive_field_infos(
                orient, receptive_field_level
            )
            for orient_side in ORIENT_SIDES:
                mother_orient = ORIENTS[
                    int(
                        (
                            orient_ind
                            + {"left": -1, "right": 1}[orient_side] * ORIENT_SUM / 4
                        )
                        % ORIENT_SUM
                    )
                ]
                mother_inds.extend(
                    get_soma_inds(
                        "point",
                        f"edge_points_in_{mother_orient}_direction_feedback_ASTD",
                        around_pos_inds,
                    )
                )
    father_inds = global_axon_end_inds[f"stimulate_vertical_orientation"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def excite_and_maintain_autapse_contour_orientation(side):

    def stimulus_function(cortex_obj):
        mother_inds, father_inds = [], []
        for orient in ORIENTS:
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        [
                            f"orientation_of_{orient}_direction_{side}_contour_A_excitation_of_step0",
                            f"orientation_of_{orient}_direction_{side}_contour_autapse",
                        ],
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"orientation-S{receptive_field_level}",
                        [
                            f"orientation_of_{orient}_direction_{side}_contour_autapse_DMax"
                        ]
                        * 2,
                    )
                )
        return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

    return stimulus_function


def excite_and_maintain_autapse_summarize_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            if receptive_field_level == 1:
                continue
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"orientation_of_{orient}_direction_inner_contour_autapse",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation",
                    f"inner_contour_orientation_summary_{orient}_autapse_DMax",
                )
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        stimulus_contour_orientation("inner"),
        stimulus_contour_orientation("outer"),
        stimulus_contour_orientation_sum_value("inner"),
        excite_inner_contour_orientation_complex_cells,
        summarize_inner_contour_orientation,
        summarize_contralateral_inner_contour_orientation,
        summarize_inner_contour_orientation_by_scale,
        summarize_inner_contour_orientation_with_scale_1,
        summarize_max_of_rays_in_all_directions,
        excite_and_maintain_all_rays_synapses,
        inhibit_all_rays_summarize_inner_contour_orientation_with_scale_1_autapse,
        inhibit_inner_contour_orientation_with_smaller_scale_outer_contour_orientation,
        inhibit_inner_contour_orientation_with_smaller_scale_inner_contour_orientation,
        excite_and_maintain_autapse_contour_orientation("inner"),
        excite_and_maintain_autapse_contour_orientation("outer"),
        excite_and_maintain_autapse_summarize_inner_contour_orientation,
        stimulate_inner_contour_orientation_with_std,
        stimulate_vertical_orientation,
        STD_stimulate_vertical_orientation,
    ]
