from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 轮廓中心反馈激励汇总轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(
                f"轮廓中心",
                f"{side}轮廓中心的注意力竞争结果",
            )
        )
        father_inds.extend(
            get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_反馈_DMax")
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "轮廓中心反馈激励汇总轮廓方位"
        ),
    )


def 禁止轮廓中心反馈激励汇总轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(
                f"轮廓中心",
                f"{side}轮廓中心的注意力竞争结果_A全或无强抑制",
            )
        )
    father_inds = axon_end_inds["轮廓中心反馈激励汇总轮廓方位"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止轮廓中心反馈激励汇总轮廓方位"
        ),
    )


def 解禁轮廓中心反馈激励汇总轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_A抑制")
        )
    father_inds = axon_end_inds["禁止轮廓中心反馈激励汇总轮廓方位"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总轮廓方位反馈激励轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_反馈")
            )
            father_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向的{side}轮廓方位_反馈_DMax",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "汇总轮廓方位反馈激励轮廓方位"
        ),
    )


def 禁止汇总轮廓方位反馈激励轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"方位", f"汇总{orient}方向的内轮廓方位_反馈_A全或无强抑制"
                )
            )
    father_inds = axon_end_inds["汇总轮廓方位反馈激励轮廓方位"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止汇总轮廓方位反馈激励轮廓方位"
        ),
    )


def 解禁汇总轮廓方位反馈激励轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向的{side}轮廓方位_A抑制",
                )
            )
    father_inds = axon_end_inds["禁止汇总轮廓方位反馈激励轮廓方位"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        轮廓中心反馈激励汇总轮廓方位,
        禁止轮廓中心反馈激励汇总轮廓方位,
        解禁轮廓中心反馈激励汇总轮廓方位,
        汇总轮廓方位反馈激励轮廓方位,
        禁止汇总轮廓方位反馈激励轮廓方位,
        解禁汇总轮廓方位反馈激励轮廓方位,
    ]
