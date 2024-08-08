from consts.feature import ORIENT_SUM, BOTH_SIDE_ORIENT_DESC
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves, REGION
from ...form_nerve.form_nerve import form_nerve
import numpy as np

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def is_orient_in_range(line_orient, left_open_orient, right_open_orient):
    if left_open_orient < right_open_orient:
        return left_open_orient < line_orient < right_open_orient
    else:
        return left_open_orient < line_orient or line_orient < right_open_orient


def get_opposite_orient_ind(orient_ind):
    return (orient_ind + ORIENT_SUM // 2) % ORIENT_SUM


def get_opposite_orient(orient):
    return (orient + 180.0) % 360.0 or 360.0


def 直线激励轮廓中心(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "线_轮廓直线",
                f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞",
            )
        )
        father_inds.extend(
            get_soma_inds(
                f"轮廓中心",
                f"{side}轮廓中心_DAdd",
            )
        )
        axon_end_release_sums.extend(
            [65 / (ORIENT_SUM // 2)] * REGION[f"轮廓中心"]["hyper_col_sum"]
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "直线激励轮廓中心"
        ),
    )


def 直线抑制激励轮廓中心(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "线_轮廓直线",
                f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞_A抑制",
            )
        )
    father_inds = axon_end_inds["直线激励轮廓中心"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "直线抑制激励轮廓中心"
        ),
    )


def 内轮廓方位拮抗抑制轮廓中心(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                "方位",
                f"汇总{BOTH_SIDE_ORIENT_DESC[(orient_ind+4)%(ORIENT_SUM//2)]}方向的内轮廓方位_A全或无抑制",
            )
        )
        axon_end_release_sums.extend([65 * 5] * REGION[f"轮廓中心"]["hyper_col_sum"])
    father_inds = axon_end_inds["直线抑制激励轮廓中心"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def 用轮廓直线激励整体轮廓中心(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for both_orient_ind in range(ORIENT_SUM // 2):
        each_axon_end_release_sum = 65 / (ORIENT_SUM // 2)
        mother_inds.extend(
            get_soma_inds(
                "线_轮廓直线",
                f"汇总{BOTH_SIDE_ORIENT_DESC[both_orient_ind]}方向_外轮廓直线_复杂细胞",
            )
        )
        father_inds.extend(get_soma_inds("轮廓中心", "外轮廓中心"))
        axon_end_release_sums.extend(
            [each_axon_end_release_sum] * REGION["线_轮廓直线"]["hyper_col_sum"]
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def form_init_nerve():
    return [
        直线激励轮廓中心,
        直线抑制激励轮廓中心,
        内轮廓方位拮抗抑制轮廓中心,
        用轮廓直线激励整体轮廓中心,
    ]
