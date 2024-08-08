from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def summarize_contour_center_feedback_excitation_orientations(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(
                f"contour_center",
                f"attention_competition_result_of_{side}_contour_center",
            )
        )
        father_inds.extend(
            get_soma_inds(f"orientation", f"inner_contour_orientation_summary_{orient}_feedback_DMax")
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "summarize_contour_center_feedback_excitation_orientations"
        ),
    )


def prohibit_summarize_contour_center_feedback_excitation_orientations(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(
                f"contour_center",
                f"attention_competition_result_of_{side}_contour_center_A_all_or_none_strong_inhibit",
            )
        )
    father_inds = axon_end_inds["summarize_contour_center_feedback_excitation_orientations"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_summarize_contour_center_feedback_excitation_orientations"
        ),
    )


def unprohibited_summarize_contour_center_feedback_excitation_orientations(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(f"orientation", f"inner_contour_orientation_summary_{orient}_A_inhibit")
        )
    father_inds = axon_end_inds["prohibit_summarize_contour_center_feedback_excitation_orientations"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def summarize_contour_orientation_feedback_excitation_contour_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(f"orientation", f"inner_contour_orientation_summary_{orient}_feedback")
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"orientation_of_{orient}_direction_{side}_contour_feedback_DMax",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "summarize_contour_orientation_feedback_excitation_contour_orientation"
        ),
    )


def prohibit_summarize_contour_orientation_feedback_excitation_contour_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"orientation", f"inner_contour_orientation_summary_{orient}_feedback_A_all_or_none_strong_inhibit"
                )
            )
    father_inds = axon_end_inds["summarize_contour_orientation_feedback_excitation_contour_orientation"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_summarize_contour_orientation_feedback_excitation_contour_orientation"
        ),
    )


def unprohibited_summarize_contour_orientation_feedback_excitation_contour_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"orientation-S{receptive_field_level}",
                    f"orientation_of_{orient}_direction_{side}_contour_A_inhibit",
                )
            )
    father_inds = axon_end_inds["prohibit_summarize_contour_orientation_feedback_excitation_contour_orientation"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        summarize_contour_center_feedback_excitation_orientations,
        prohibit_summarize_contour_center_feedback_excitation_orientations,
        unprohibited_summarize_contour_center_feedback_excitation_orientations,
        summarize_contour_orientation_feedback_excitation_contour_orientation,
        prohibit_summarize_contour_orientation_feedback_excitation_contour_orientation,
        unprohibited_summarize_contour_orientation_feedback_excitation_contour_orientation,
    ]
