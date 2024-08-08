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


def 角反馈激励汇总射线(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    f"角",
                    [f"方位{orient}和{(orient+angle)%360 or 360.0}的角的注意力竞争结果"]
                    * 2,
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值_反馈_DMax",
                        f"汇总{(orient+angle)%360 or 360.0}方向左侧的射线的最大值_反馈_DMax",
                    ],
                )
            )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "角反馈激励汇总射线"
        ),
    )


def 汇总射线反馈激励射线(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线",
                        f"汇总{orient}方向{orient_side}侧的射线的最大值_反馈",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线_反馈_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "汇总射线反馈激励射线"
        ),
    )


def 禁止汇总射线反馈激励射线(cortex_obj):
    mother_inds = []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线",
                        f"汇总{orient}方向{orient_side}侧的射线的最大值_反馈_A全或无强抑制",
                    )
                )
    father_inds = axon_end_inds["汇总射线反馈激励射线"]
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止汇总射线反馈激励射线"
        ),
    )


def 解禁汇总射线反馈激励射线(cortex_obj):
    mother_inds = []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线_A抑制",
                    )
                )
    father_inds = axon_end_inds["禁止汇总射线反馈激励射线"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        角反馈激励汇总射线,
        汇总射线反馈激励射线,
        禁止汇总射线反馈激励射线,
        解禁汇总射线反馈激励射线,
    ]
