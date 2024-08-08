from consts.feature import (
    ORIENTS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    ORIENT_SIDES,
)
from ...util import (
    get_soma_inds,
    save_axon_end_inds_with_new_nerves,
)
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def angle_feedback_excitation_summary_rays(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    f"angle",
                    [
                        f"attention_competition_result_of_angle_of_orientation{orient}_and_{(orient+angle)%360 or 360.0}"
                    ]
                    * 2,
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side_feedback_DMax",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360 or 360.0}_direction_left_side_feedback_DMax",
                    ],
                )
            )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "angle_feedback_excitation_summary_rays"
        ),
    )


def summarize_ray_feedback_excitation_rays(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray",
                        f"summarize_max_values_of_rays_in_{orient}_direction_{orient_side}_side_feedback",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side_feedback_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "summarize_ray_feedback_excitation_rays"
        ),
    )


def prohibit_summarize_ray_feedback_excitation_rays(cortex_obj):
    mother_inds = []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray",
                        f"summarize_max_values_of_rays_in_{orient}_direction_{orient_side}_side_feedback_A_all_or_none_strong_inhibit",
                    )
                )
    father_inds = axon_end_inds["summarize_ray_feedback_excitation_rays"]
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_summarize_ray_feedback_excitation_rays"
        ),
    )


def unprohibited_summarize_ray_feedback_excitation_rays(cortex_obj):
    mother_inds = []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side_A_inhibit",
                    )
                )
    father_inds = axon_end_inds["prohibit_summarize_ray_feedback_excitation_rays"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        angle_feedback_excitation_summary_rays,
        summarize_ray_feedback_excitation_rays,
        prohibit_summarize_ray_feedback_excitation_rays,
        unprohibited_summarize_ray_feedback_excitation_rays,
    ]
