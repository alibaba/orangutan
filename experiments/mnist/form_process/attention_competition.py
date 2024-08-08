from consts.feature import (
    ANGLE_NAMES,
    CONTOUR_SIDES,
)
from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs
LOOP_PROPS = [
    (feature_type, feature_name)
    for feature_type in ["angle", "contour_center"]
    for feature_name in {
        "angle": ANGLE_NAMES,
        "contour_center": [f"{side}_contour_center" for side in CONTOUR_SIDES],
    }[feature_type]
]


def excite_attention_competition(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(
            get_soma_inds(
                feature_type,
                f"{feature_name}",
            )
        )
        father_inds.extend(get_soma_inds(feature_type, f"attention_competition_of_{feature_name}"))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def attention_competition_excitation_summary(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(get_soma_inds(feature_type, f"attention_competition_of_{feature_name}"))
        father_inds.extend(
            np.tile(
                get_soma_inds(
                    "global_control",
                    f"attention_competition_excitation_summary{'_outer_contour_center' if feature_name == 'outer_contour_center' else ''}_DMax",
                ),
                REGION[feature_type]["hyper_col_sum"],
            )
        )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def control_attention_competition_start_timing(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(
        get_soma_inds(f"global_control", f"shared_regulation_excitation_A_control_attention_competition_start_timing")
    )
    father_inds.extend(get_soma_inds("global_control", f"attention_competition_excitation_summary_DMin"))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def excite_attention_competition_result(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(
            get_soma_inds(
                feature_type,
                f'{feature_name}_A_excitation_with_step_length_{({ "contour_center":2, "angle":3, }[feature_type])+2}',
            )
        )
        father_inds.extend(
            get_soma_inds(feature_type, f"attention_competition_result_of_{feature_name}")
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "excite_attention_competition_result"
        ),
    )


def prohibit_excite_attention_competition_result(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(
            np.tile(
                get_soma_inds(
                    "global_control",
                    f"attention_competition_excitation_summary{'_outer_contour_center' if feature_name == 'outer_contour_center' else ''}_A_all_or_none_weak_inhibition",
                ),
                REGION[feature_type]["hyper_col_sum"],
            )
        )
        father_inds.extend(
            get_soma_inds(
                feature_type,
                f'{feature_name}_A_excitation_with_step_length_{({ "contour_center":2, "angle":3, }[feature_type])+2}',
            )
        )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        excite_attention_competition,
        attention_competition_excitation_summary,
        control_attention_competition_start_timing,
        excite_attention_competition_result,
        prohibit_excite_attention_competition_result,
    ]
