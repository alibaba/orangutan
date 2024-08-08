from consts.feature import (
    VISUAL_FIELD_WH,
)
from ...util import (
    get_soma_inds,
    save_axon_end_inds_with_new_nerves,
)
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION

axon_end_inds = {}


def excite_offset(cortex_obj):
    mother_inds, father_inds = [], []
    for center_x_or_y in range(VISUAL_FIELD_WH[0]):
        for x_or_y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            if not (center_x_or_y + x_or_y_delta) in range(VISUAL_FIELD_WH[0]):
                continue
            mother_inds.extend(get_soma_inds(f"whole_center", f"{center_x_or_y}"))
            father_inds.extend(
                get_soma_inds("offset_of_current_feature_position_relative_to_overall_center", f"{x_or_y_delta}")
            )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "excite_offset"
        ),
    )


def prohibit_excite_offset(cortex_obj):
    mother_inds, father_inds = [], []
    for center_x_or_y in range(VISUAL_FIELD_WH[0]):
        for x_or_y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            if not (center_x_or_y + x_or_y_delta) in range(VISUAL_FIELD_WH[0]):
                continue
            mother_inds.extend(
                get_soma_inds(f"whole_center", f"{center_x_or_y}_A_inhibit")
            )
    father_inds = axon_end_inds["excite_offset"]
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "prohibit_excite_offset"
        ),
    )


def unprohibited_excite_offset(cortex_obj):
    mother_inds, father_inds = [], []
    for center_x_or_y in range(VISUAL_FIELD_WH[0]):
        for x_or_y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            if not (center_x_or_y + x_or_y_delta) in range(VISUAL_FIELD_WH[0]):
                continue
            mother_inds.extend(
                get_soma_inds(f"current_feature_position", f"{center_x_or_y+x_or_y_delta}_A_inhibit")
            )
    father_inds.extend(axon_end_inds["prohibit_excite_offset"])
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        excite_offset,
        prohibit_excite_offset,
        unprohibited_excite_offset,
    ]
