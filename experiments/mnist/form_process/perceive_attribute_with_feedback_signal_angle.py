from consts.feature import (
    ORIENTS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    ORIENT_SIDES,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION
from .ray_excitation_angle import summarize_ray_max_values_axon_end_release_sums

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def find_intermediate_orientation_excited_by_two_orientations(orient, angle):
    left_orient = orient
    right_orient = (orient + angle) % 360.0 or 360.0
    center_orient = (orient + angle / 2) % 360.0 or 360.0
    orient_deltas = calculate_angles_between_all_and_specific_orientations(
        center_orient
    )
    close_center_orients = ORIENTS[orient_deltas == min(orient_deltas)]
    left_center_orient = close_center_orients[
        np.argmin(
            calculate_angles_between_all_and_specific_orientations(
                left_orient, close_center_orients
            )
        )
    ]
    right_center_orient = close_center_orients[
        np.argmin(
            calculate_angles_between_all_and_specific_orientations(
                right_orient, close_center_orients
            )
        )
    ]
    return left_center_orient, right_center_orient


def calculate_angles_between_all_and_specific_orientations(orient, all_orient=ORIENTS):
    return np.minimum(
        np.abs(orient - all_orient),
        np.abs(orient + 360 - all_orient),
    )


def find_intermediate_scale_excited_by_two_scales(left_scale, right_scale):
    center_scale = (left_scale + right_scale) / 2
    scale_deltas = calculate_distances_between_all_scales_and_specific_scale(
        center_scale
    )
    close_center_scales = RECEPTIVE_FIELD_LEVELS[scale_deltas == min(scale_deltas)]
    left_center_scale = close_center_scales[
        np.argmin(
            calculate_distances_between_all_scales_and_specific_scale(
                left_scale, close_center_scales
            )
        )
    ]
    right_center_scale = close_center_scales[
        np.argmin(
            calculate_distances_between_all_scales_and_specific_scale(
                right_scale, close_center_scales
            )
        )
    ]
    return left_center_scale, right_center_scale


def calculate_distances_between_all_scales_and_specific_scale(
    scale, all_scale=RECEPTIVE_FIELD_LEVELS
):
    return np.abs(scale - all_scale)


def excite_type(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    f"angle",
                    f"attention_competition_result_of_angle_of_orientation{orient}_and_{(orient+angle)%360 or 360.0}",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-type",
                        f"type_angle_single_coding_DMax",
                    ),
                    REGION["angle"]["hyper_col_sum"],
                )
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def ray_excite_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            left_orient, right_orient = (
                find_intermediate_orientation_excited_by_two_orientations(orient, angle)
            )
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side",
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
                    REGION["ray"]["hyper_col_sum"],
                )
            )
            assert len(mother_inds) == len(father_inds)
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "ray_excite_orientation"
        ),
    )


def prohibit_ray_excite_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_A_all_or_none_strong_inhibit",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side_A_all_or_none_strong_inhibit",
                    ],
                )
            )
    mother_inds = mother_inds * 2
    father_inds = np.tile(axon_end_inds["ray_excite_orientation"], 2)
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_ray_excite_orientation"
        ),
    )


def unprohibited_ray_excite_orientation(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side_feedback_A_inhibit",
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_feedback_A_inhibit",
                    ],
                )
            )
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_feedback_A_inhibit",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side_feedback_A_inhibit",
                    ],
                )
            )
    father_inds = axon_end_inds["prohibit_ray_excite_orientation"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
    )


def ray_excite_angle(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side",
                    ],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-angle",
                        [
                            f"angle_{angle}_single_coding_DMax",
                        ]
                        * 2,
                    ),
                    REGION["ray"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "ray_excite_angle"
        ),
    )


def prohibit_ray_excite_angle(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_A_all_or_none_strong_inhibit",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side_A_all_or_none_strong_inhibit",
                    ],
                )
            )
    mother_inds = mother_inds * 2
    father_inds = np.tile(axon_end_inds["ray_excite_angle"], 2)
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_ray_excite_angle"
        ),
    )


def unprohibited_ray_excite_angle(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side_feedback_A_inhibit",
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_feedback_A_inhibit",
                    ],
                )
            )
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_feedback_A_inhibit",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360. or 360.}_direction_left_side_feedback_A_inhibit",
                    ],
                )
            )
    father_inds = axon_end_inds["prohibit_ray_excite_angle"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
    )


def prepare_ray_to_excite_max_excited_ray_in_direction(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side_for_maximum_excitation",
                    )
                )
                axon_end_release_sums.extend(
                    np.tile(
                        [
                            summarize_ray_max_values_axon_end_release_sums(
                                receptive_field_level
                            )
                        ],
                        REGION[f"ray-S{receptive_field_level}"]["hyper_col_sum"],
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def most_excited_ray_in_excitation_direction(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side_for_maximum_excitation",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"{orient}_direction_max_excitation_{orient_side}_side_rays_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "most_excited_ray_in_excitation_direction"
        ),
    )


def most_excited_ray_in_direction_autapse(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"{orient}_direction_max_excitation_{orient_side}_side_rays",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"{orient}_direction_max_excitation_{orient_side}_side_rays_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def prohibit_most_excited_ray_in_excitation_direction(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray",
                        f"summarize_max_values_of_rays_in_{orient}_direction_{orient_side}_side_A_all_or_none_weak_inhibition",
                    )
                )
    father_inds = axon_end_inds["most_excited_ray_in_excitation_direction"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def summarize_ray_scales(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"{orient}_direction_max_excitation_{orient_side}_side_rays",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"summarize_rays_on_all_directions_{orient_side}_side_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "summarize_ray_scales"
        ),
    )


def prohibit_summarize_ray_scales(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"{orient}_direction_max_excitation_{orient_side}_side_rays_A_all_or_none_strong_inhibit",
                    )
                )
    father_inds = axon_end_inds["summarize_ray_scales"]
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_summarize_ray_scales"
        ),
    )


def unprohibited_summarize_ray_scales(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side_feedback_A_inhibit",
                    )
                )
    father_inds = axon_end_inds["prohibit_summarize_ray_scales"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def ray_excite_scale(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for left_scale in LINE_RECEPTIVE_FIELD_LEVELS:
        for right_scale in LINE_RECEPTIVE_FIELD_LEVELS:
            left_center_scale, right_center_scale = (
                find_intermediate_scale_excited_by_two_scales(left_scale, right_scale)
            )
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{left_scale}",
                    f"summarize_rays_on_all_directions_left_side",
                )
            )
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{right_scale}",
                    f"summarize_rays_on_all_directions_right_side",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-scale",
                        f"scale_{left_center_scale}_single_coding_DMax",
                    ),
                    REGION[f"ray-S{left_scale}"]["hyper_col_sum"],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"attribute-scale",
                        f"scale_{right_center_scale}_single_coding_DMax",
                    ),
                    REGION[f"ray-S{right_scale}"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "ray_excite_scale"
        ),
    )


def prohibit_ray_excite_scale(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for left_scale in LINE_RECEPTIVE_FIELD_LEVELS:
        for right_scale in LINE_RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{left_scale}",
                    f"summarize_rays_on_all_directions_left_side_A_all_or_none_strong_inhibit",
                )
            )
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{right_scale}",
                    f"summarize_rays_on_all_directions_right_side_A_all_or_none_strong_inhibit",
                )
            )
    father_inds = axon_end_inds["ray_excite_scale"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_ray_excite_scale"
        ),
    )


def unprohibited_ray_excite_scale(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for left_scale in LINE_RECEPTIVE_FIELD_LEVELS:
        for right_scale in LINE_RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{right_scale}",
                    f"summarize_rays_on_all_directions_right_side_A_inhibit",
                )
            )
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{left_scale}",
                    f"summarize_rays_on_all_directions_left_side_A_inhibit",
                )
            )
    father_inds = axon_end_inds["prohibit_ray_excite_scale"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # type
        excite_type,
        # face
        ray_excite_orientation,
        prohibit_ray_excite_orientation,
        unprohibited_ray_excite_orientation,
        # angle
        ray_excite_angle,
        prohibit_ray_excite_angle,
        unprohibited_ray_excite_angle,
        # scale
        prepare_ray_to_excite_max_excited_ray_in_direction,
        most_excited_ray_in_excitation_direction,
        most_excited_ray_in_direction_autapse,
        prohibit_most_excited_ray_in_excitation_direction,
        summarize_ray_scales,
        prohibit_summarize_ray_scales,
        unprohibited_summarize_ray_scales,
        ray_excite_scale,
        prohibit_ray_excite_scale,
        unprohibited_ray_excite_scale,
    ]
