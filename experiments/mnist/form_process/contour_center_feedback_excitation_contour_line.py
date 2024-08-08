from consts.feature import (
    ORIENT_SUM,
    RECEPTIVE_FIELD_LEVELS,
    BOTH_SIDE_ORIENT_DESC,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def summarize_contour_center_feedback_excitation_lines(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                f"contour_center",
                f"attention_competition_result_of_{side}_contour_center",
            )
        )
        father_inds.extend(
            get_soma_inds(
                "antipodal_points",
                f"summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell_feedback_DMax",
            )
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "summarize_contour_center_feedback_excitation_lines"
        ),
    )


def prohibit_summarize_contour_center_feedback_excitation_lines(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                f"contour_center",
                f"attention_competition_result_of_{side}_contour_center_A_all_or_none_strong_inhibit",
            )
        )
    father_inds = axon_end_inds["summarize_contour_center_feedback_excitation_lines"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_summarize_contour_center_feedback_excitation_lines"
        ),
    )


def unprohibited_summarize_contour_center_feedback_excitation_lines(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "inner"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "antipodal_points",
                f"summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell_A_inhibit",
            )
        )
    father_inds = axon_end_inds["prohibit_summarize_contour_center_feedback_excitation_lines"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        summarize_contour_center_feedback_excitation_lines,
        prohibit_summarize_contour_center_feedback_excitation_lines,
        unprohibited_summarize_contour_center_feedback_excitation_lines,
    ]
