from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    MIN_ANGLE,
    ORIENT_SIDES,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION
from .perceive_attribute_with_feedback_signal_angle import (
    find_intermediate_orientation_excited_by_two_orientations,
)

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def most_excited_with_feedback_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind, orient in enumerate(ORIENTS):
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"max_excitation_{orient}_direction_position_inner_contour_orientation",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"max_excitation_{orient}_direction_position_with_feedback_inner_contour_orientation",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "most_excited_with_feedback_inner_contour_orientation"
        ),
    )


def prohibit_most_excited_with_feedback_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind, orient in enumerate(ORIENTS):
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"max_excitation_{orient}_direction_position_inner_contour_orientation_A_all_or_none_strong_inhibit",
                )
            )
    father_inds = axon_end_inds["most_excited_with_feedback_inner_contour_orientation"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds,
            "prohibit_most_excited_with_feedback_inner_contour_orientation",
        ),
    )


def unprohibited_most_excited_with_feedback_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind, orient in enumerate(ORIENTS):
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"orientation_of_{orient}_direction_inner_contour_feedback_A_inhibit",
                )
            )
    father_inds = axon_end_inds[
        "prohibit_most_excited_with_feedback_inner_contour_orientation"
    ]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def excitation_on_arc_edge_with_feedback_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    f"inner_contour_orientation_summary_{orient}_autapse",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation",
                    f"inner_contour_orientation_summary_{orient}_{orient_side}_with_feedback_on_curve_edge",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "summarize_all_lateral_scales_inner_contour_orientation"
        ),
    )


def prohibit_excitation_on_arc_edge_with_feedback_inner_contour_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    f"inner_contour_orientation_summary_{orient}_autapse_A_all_or_none_strong_inhibit",
                )
            )
    father_inds = axon_end_inds[
        "summarize_all_lateral_scales_inner_contour_orientation"
    ]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds,
            "prohibit_excitation_on_arc_edge_with_feedback_inner_contour_orientation",
        ),
    )


def unprohibited_excitation_on_arc_edge_with_feedback_inner_contour_orientation(
    cortex_obj,
):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    f"inner_contour_orientation_summary_{orient}_feedback_A_inhibit",
                )
            )
    father_inds = axon_end_inds[
        "prohibit_excitation_on_arc_edge_with_feedback_inner_contour_orientation"
    ]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds,
            "unprohibited_excitation_on_arc_edge_with_feedback_inner_contour_orientation",
        ),
    )


def prohibit_unprohibited_excitation_on_arc_edge_with_feedback_inner_contour_orientation(
    cortex_obj,
):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_orient = (
                orient
                + MIN_ANGLE
                * (
                    {
                        "left": -1,
                        "right": 1,
                    }[orient_side]
                )
                + 360.0
            ) % 360.0 or 360.0
            mother_inds.extend(
                get_soma_inds(
                    f"orientation",
                    f"inner_contour_orientation_summary_{mother_orient}_feedback_A_inhibit",
                )
            )
    father_inds = axon_end_inds[
        "unprohibited_excitation_on_arc_edge_with_feedback_inner_contour_orientation"
    ]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def summarize_inner_contour_orientations_on_arc_edge_with_feedback(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    f"orientation",
                    f"inner_contour_orientation_summary_{orient}_{orient_side}_with_feedback_on_curve_edge",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"global_control",
                        f"summarize_inner_contour_orientations_with_feedback_at_curve_edges_DMax",
                    ),
                    REGION["orientation"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inner_contour_orientation_summary_at_position(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(
                f"orientation", f"inner_contour_orientation_summary_{orient}_autapse"
            )
        )
        father_inds.extend(
            get_soma_inds(
                f"orientation", f"inner_contour_orientation_summary_at_position_DMax"
            )
        )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def most_excited_inner_contour_orientation_at_excitation_location(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient in ORIENTS:
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"orientation_of_{orient}_direction_inner_contour_autapse",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"max_excitation_{orient}_direction_position_inner_contour_orientation",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds,
            "most_excited_inner_contour_orientation_at_excitation_location",
        ),
    )


def prohibit_most_excited_inner_contour_orientation_at_excitation_location(
    cortex_obj,
):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient in ORIENTS:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    f"inner_contour_orientation_summary_at_position_A_all_or_none_weak_inhibition",
                )
            )
    father_inds = axon_end_inds[
        "most_excited_inner_contour_orientation_at_excitation_location"
    ]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inner_contour_orientation_excitation_direction(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            left_orient, right_orient = (
                find_intermediate_orientation_excited_by_two_orientations(orient, angle)
            )
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    [
                        f"inner_contour_orientation_summary_{orient}_right_with_feedback_on_curve_edge",
                        f"inner_contour_orientation_summary_{(orient+angle)%360. or 360.}_left_with_feedback_on_curve_edge",
                    ],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-face",
                        [
                            f"face_{left_orient}_single_coding_DMax",
                            f"face_{right_orient}_single_coding_DMax",
                        ],
                    ),
                    REGION["antipodal_points"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "inner_contour_orientation_excitation_direction"
        ),
    )


def prohibit_inner_contour_orientation_excitation_direction(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    [
                        f"inner_contour_orientation_summary_{orient}_right_with_feedback_on_curve_edge_A_inhibit",
                        f"inner_contour_orientation_summary_{(orient+angle)%360. or 360.}_left_with_feedback_on_curve_edge_A_inhibit",
                    ],
                )
            )
    father_inds = axon_end_inds["inner_contour_orientation_excitation_direction"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_inner_contour_orientation_excitation_direction"
        ),
    )


def unprohibited_inner_contour_orientation_excitation_direction(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    [
                        f"inner_contour_orientation_summary_{(orient+angle)%360. or 360.}_left_with_feedback_on_curve_edge_A_inhibit",
                        f"inner_contour_orientation_summary_{orient}_right_with_feedback_on_curve_edge_A_inhibit",
                    ],
                )
            )
    father_inds = axon_end_inds[
        "prohibit_inner_contour_orientation_excitation_direction"
    ]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "unprohibited_inner_contour_orientation_excitation_direction"
        ),
    )


def excitation_direction_none(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(f"attribute-type", f"type_contour_center_single_coding"),
    )
    father_inds.extend(
        get_soma_inds(f"attribute-face", f"face_none_single_coding_DMax"),
    )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "excitation_direction_none"
        ),
    )


def prohibit_excitation_direction_none(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(
            f"attribute-type",
            f"type_contour_center_single_coding_A_all_or_none_weak_inhibition",
        ),
    )
    father_inds = axon_end_inds["excitation_direction_none"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_excitation_direction_none"
        ),
    )


def enhance_prohibit_excitation_direction_none(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(
            "global_control",
            "summarize_inner_contour_orientations_with_feedback_at_curve_edges",
        )
    )
    father_inds = axon_end_inds["prohibit_excitation_direction_none"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inner_contour_orientation_excitation_angle(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    [
                        f"inner_contour_orientation_summary_{orient}_right_with_feedback_on_curve_edge",
                        f"inner_contour_orientation_summary_{(orient+angle)%360. or 360.}_left_with_feedback_on_curve_edge",
                    ],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-angle",
                        f"angle_{angle}_single_coding_DMax",
                    ),
                    REGION["antipodal_points"]["hyper_col_sum"] * 2,
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "inner_contour_orientation_excitation_angle"
        ),
    )


def prohibit_inner_contour_orientation_excitation_angle(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    [
                        f"inner_contour_orientation_summary_{orient}_right_with_feedback_on_curve_edge_A_inhibit",
                        f"inner_contour_orientation_summary_{(orient+angle)%360. or 360.}_left_with_feedback_on_curve_edge_A_inhibit",
                    ],
                )
            )
    father_inds = axon_end_inds["inner_contour_orientation_excitation_angle"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_inner_contour_orientation_excitation_angle"
        ),
    )


def unprohibited_inner_contour_orientation_excitation_angle(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "orientation",
                    [
                        f"inner_contour_orientation_summary_{(orient+angle)%360. or 360.}_left_with_feedback_on_curve_edge_A_inhibit",
                        f"inner_contour_orientation_summary_{orient}_right_with_feedback_on_curve_edge_A_inhibit",
                    ],
                )
            )
    father_inds = axon_end_inds["prohibit_inner_contour_orientation_excitation_angle"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "unprohibited_inner_contour_orientation_excitation_angle"
        ),
    )


def excitation_angle_none(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(f"attribute-type", f"type_contour_center_single_coding"),
    )
    father_inds.extend(
        get_soma_inds(f"attribute-angle", f"angle_none_single_coding_DMax"),
    )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "excitation_angle_none"
        ),
    )


def prohibit_excitation_angle_none(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(
            f"attribute-type",
            f"type_contour_center_single_coding_A_all_or_none_weak_inhibition",
        ),
    )
    father_inds = axon_end_inds["excitation_angle_none"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_excitation_angle_none"
        ),
    )


def enhance_prohibit_excitation_angle_none(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(
            "global_control",
            "summarize_inner_contour_orientations_with_feedback_at_curve_edges",
        )
    )
    father_inds = axon_end_inds["prohibit_excitation_angle_none"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inner_contour_orientation_excitation_scale(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"max_excitation_{orient}_direction_position_with_feedback_inner_contour_orientation",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-scale",
                        f"scale_{receptive_field_level}_single_coding_DMax",
                    ),
                    REGION[f"orientation-S{receptive_field_level}"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "inner_contour_orientation_excitation_scale"
        ),
    )


def excitation_arc_type(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    mother_inds.extend(
        get_soma_inds(
            f"contour_center",
            f"attention_competition_result_of_inner_contour_center",
        )
    )
    father_inds.extend(
        np.tile(
            get_soma_inds(
                f"attribute-type",
                f"type_contour_center_single_coding_DMax",
            ),
            REGION["contour_center"]["hyper_col_sum"],
        )
    )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # type
        excitation_arc_type,
        #
        excitation_on_arc_edge_with_feedback_inner_contour_orientation,
        prohibit_excitation_on_arc_edge_with_feedback_inner_contour_orientation,
        unprohibited_excitation_on_arc_edge_with_feedback_inner_contour_orientation,
        prohibit_unprohibited_excitation_on_arc_edge_with_feedback_inner_contour_orientation,
        summarize_inner_contour_orientations_on_arc_edge_with_feedback,
        # face
        inner_contour_orientation_excitation_direction,
        prohibit_inner_contour_orientation_excitation_direction,
        unprohibited_inner_contour_orientation_excitation_direction,
        excitation_direction_none,
        prohibit_excitation_direction_none,
        enhance_prohibit_excitation_direction_none,
        # angle
        inner_contour_orientation_excitation_angle,
        prohibit_inner_contour_orientation_excitation_angle,
        unprohibited_inner_contour_orientation_excitation_angle,
        excitation_angle_none,
        prohibit_excitation_angle_none,
        enhance_prohibit_excitation_angle_none,
        #
        inner_contour_orientation_summary_at_position,
        most_excited_inner_contour_orientation_at_excitation_location,
        prohibit_most_excited_inner_contour_orientation_at_excitation_location,
        most_excited_with_feedback_inner_contour_orientation,
        prohibit_most_excited_with_feedback_inner_contour_orientation,
        unprohibited_most_excited_with_feedback_inner_contour_orientation,
        # scale
        inner_contour_orientation_excitation_scale,
    ]
