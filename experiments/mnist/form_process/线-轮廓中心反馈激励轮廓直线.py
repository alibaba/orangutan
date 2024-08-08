from consts.feature import (
    ORIENT_SUM,
    RECEPTIVE_FIELD_LEVELS,
    BOTH_SIDE_ORIENT_DESC,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 轮廓中心反馈激励汇总轮廓直线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                f"轮廓中心",
                f"{side}轮廓中心的注意力竞争结果",
            )
        )
        father_inds.extend(
            get_soma_inds(
                "线_轮廓直线",
                f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞_反馈_DMax",
            )
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "轮廓中心反馈激励汇总轮廓直线"
        ),
    )


def 禁止轮廓中心反馈激励汇总轮廓直线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                f"轮廓中心",
                f"{side}轮廓中心的注意力竞争结果_A全或无强抑制",
            )
        )
    father_inds = axon_end_inds["轮廓中心反馈激励汇总轮廓直线"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止轮廓中心反馈激励汇总轮廓直线"
        ),
    )


def 解禁轮廓中心反馈激励汇总轮廓直线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "线_轮廓直线",
                f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞_A抑制",
            )
        )
    father_inds = axon_end_inds["禁止轮廓中心反馈激励汇总轮廓直线"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        轮廓中心反馈激励汇总轮廓直线,
        禁止轮廓中心反馈激励汇总轮廓直线,
        解禁轮廓中心反馈激励汇总轮廓直线,
    ]
