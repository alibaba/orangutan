from consts.feature import VISUAL_FIELD_WH
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}

def 激励偏移(cortex_obj):
    mother_inds, father_inds = [], []
    for x_or_y in range(VISUAL_FIELD_WH[0]):
        for x_or_y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            if not (x_or_y + x_or_y_delta) in range(VISUAL_FIELD_WH[0]):
                continue
            mother_inds.extend(get_soma_inds(f"位置_锚点特征", f"{x_or_y}"))
            father_inds.extend(
                get_soma_inds("位置_当前特征相对锚点特征的偏移", f"{x_or_y_delta}")
            )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "激励偏移"
        ),
    )


def 禁止激励偏移(cortex_obj):
    mother_inds, father_inds = [], []
    for x_or_y in range(VISUAL_FIELD_WH[0]):
        for x_or_y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            if not (x_or_y + x_or_y_delta) in range(VISUAL_FIELD_WH[0]):
                continue
            mother_inds.extend(get_soma_inds(f"位置_锚点特征", f"{x_or_y}_A抑制"))
    father_inds = axon_end_inds["激励偏移"]
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止激励偏移"
        ),
    )


def 解禁激励偏移(cortex_obj):
    mother_inds, father_inds = [], []
    for x_or_y in range(VISUAL_FIELD_WH[0]):
        for x_or_y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            if not (x_or_y + x_or_y_delta) in range(VISUAL_FIELD_WH[0]):
                continue
            mother_inds.extend(
                get_soma_inds(f"位置_当前特征", f"{x_or_y+x_or_y_delta}_A抑制")
            )
    father_inds.extend(axon_end_inds["禁止激励偏移"])
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励偏移,
        禁止激励偏移,
        解禁激励偏移,
    ]
