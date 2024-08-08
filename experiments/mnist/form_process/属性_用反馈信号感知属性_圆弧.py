from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    MIN_ANGLE,
    ORIENT_SIDES,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION
from .属性_用反馈信号感知属性_角 import (
    找到两个朝向分别可以激励的中间朝向,
)

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 激励所在位置兴奋最大且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind, orient in enumerate(ORIENTS):
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向所在位置兴奋最大的内轮廓方位",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向所在位置兴奋最大且有反馈的内轮廓方位",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "激励所在位置兴奋最大且有反馈的内轮廓方位"
        ),
    )


def 禁止激励所在位置兴奋最大且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind, orient in enumerate(ORIENTS):
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向所在位置兴奋最大的内轮廓方位_A全或无强抑制",
                )
            )
    father_inds = axon_end_inds["激励所在位置兴奋最大且有反馈的内轮廓方位"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止激励所在位置兴奋最大且有反馈的内轮廓方位"
        ),
    )


def 解禁激励所在位置兴奋最大且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind, orient in enumerate(ORIENTS):
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向的内轮廓方位_反馈_A抑制",
                )
            )
    father_inds = axon_end_inds["禁止激励所在位置兴奋最大且有反馈的内轮廓方位"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励位于弧线边缘且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    f"汇总{orient}方向的内轮廓方位_自突触",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"方位",
                    f"汇总{orient}方向{orient_side}侧位于弧线边缘且有反馈的内轮廓方位",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "汇总所有尺度侧向内轮廓方位"
        ),
    )


def 禁止激励位于弧线边缘且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    f"汇总{orient}方向的内轮廓方位_自突触_A全或无强抑制",
                )
            )
    father_inds = axon_end_inds["汇总所有尺度侧向内轮廓方位"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止激励位于弧线边缘且有反馈的内轮廓方位"
        ),
    )


def 解禁激励位于弧线边缘且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    f"汇总{orient}方向的内轮廓方位_反馈_A抑制",
                )
            )
    father_inds = axon_end_inds["禁止激励位于弧线边缘且有反馈的内轮廓方位"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "解禁激励位于弧线边缘且有反馈的内轮廓方位"
        ),
    )


def 禁止解禁激励位于弧线边缘且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_orient = (
                orient
                + MIN_ANGLE
                * (
                    {
                        "左": -1,
                        "右": 1,
                    }[orient_side]
                )
                + 360.0
            ) % 360.0 or 360.0
            mother_inds.extend(
                get_soma_inds(
                    f"方位", f"汇总{mother_orient}方向的内轮廓方位_反馈_A抑制"
                )
            )
    father_inds = axon_end_inds["解禁激励位于弧线边缘且有反馈的内轮廓方位"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总位于弧线边缘且有反馈的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for orient_side in ORIENT_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    f"方位",
                    f"汇总{orient}方向{orient_side}侧位于弧线边缘且有反馈的内轮廓方位",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"全局调控",
                        f"汇总所有位置位于弧线边缘且有反馈的内轮廓方位_DMax",
                    ),
                    REGION["方位"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总所在位置的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        mother_inds.extend(get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_自突触"))
        father_inds.extend(get_soma_inds(f"方位", f"汇总所在位置的内轮廓方位_DMax"))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励所在位置兴奋最大的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient in ORIENTS:
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向的内轮廓方位_自突触",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向所在位置兴奋最大的内轮廓方位",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "激励所在位置兴奋最大的内轮廓方位"
        ),
    )


def 禁止激励激励所在位置兴奋最大的内轮廓方位(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient in ORIENTS:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    f"汇总所在位置的内轮廓方位_A全或无弱抑制",
                )
            )
    father_inds = axon_end_inds["激励所在位置兴奋最大的内轮廓方位"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 内轮廓方位激励朝向(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            left_orient, right_orient = 找到两个朝向分别可以激励的中间朝向(
                orient, angle
            )
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    [
                        f"汇总{orient}方向右侧位于弧线边缘且有反馈的内轮廓方位",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧位于弧线边缘且有反馈的内轮廓方位",
                    ],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"属性-朝向",
                        [
                            f"朝向{left_orient}-个体编码_DMax",
                            f"朝向{right_orient}-个体编码_DMax",
                        ],
                    ),
                    REGION["线_轮廓直线"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "内轮廓方位激励朝向"
        ),
    )


def 禁止内轮廓方位激励朝向(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    [
                        f"汇总{orient}方向右侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                    ],
                )
            )
    father_inds = axon_end_inds["内轮廓方位激励朝向"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止内轮廓方位激励朝向"
        ),
    )


def 解禁内轮廓方位激励朝向(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    [
                        f"汇总{(orient+angle)%360. or 360.}方向左侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                        f"汇总{orient}方向右侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                    ],
                )
            )
    father_inds = axon_end_inds["禁止内轮廓方位激励朝向"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "解禁内轮廓方位激励朝向"
        ),
    )


def 激励朝向_无(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(f"属性-类型", f"类型轮廓中心-个体编码"),
    )
    father_inds.extend(
        get_soma_inds(f"属性-朝向", f"朝向无-个体编码_DMax"),
    )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "激励朝向_无"
        ),
    )


def 禁止激励朝向_无(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(f"属性-类型", f"类型轮廓中心-个体编码_A全或无弱抑制"),
    )
    father_inds = axon_end_inds["激励朝向_无"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止激励朝向_无"
        ),
    )


def 增强禁止激励朝向_无(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(
            "全局调控",
            "汇总所有位置位于弧线边缘且有反馈的内轮廓方位",
        )
    )
    father_inds = axon_end_inds["禁止激励朝向_无"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 内轮廓方位激励角度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    [
                        f"汇总{orient}方向右侧位于弧线边缘且有反馈的内轮廓方位",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧位于弧线边缘且有反馈的内轮廓方位",
                    ],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"属性-角度",
                        f"角度{angle}-个体编码_DMax",
                    ),
                    REGION["线_轮廓直线"]["hyper_col_sum"] * 2,
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "内轮廓方位激励角度"
        ),
    )


def 禁止内轮廓方位激励角度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    [
                        f"汇总{orient}方向右侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                    ],
                )
            )
    father_inds = axon_end_inds["内轮廓方位激励角度"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止内轮廓方位激励角度"
        ),
    )


def 解禁内轮廓方位激励角度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "方位",
                    [
                        f"汇总{(orient+angle)%360. or 360.}方向左侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                        f"汇总{orient}方向右侧位于弧线边缘且有反馈的内轮廓方位_A抑制",
                    ],
                )
            )
    father_inds = axon_end_inds["禁止内轮廓方位激励角度"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "解禁内轮廓方位激励角度"
        ),
    )


def 激励角度_无(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(f"属性-类型", f"类型轮廓中心-个体编码"),
    )
    father_inds.extend(
        get_soma_inds(f"属性-角度", f"角度无-个体编码_DMax"),
    )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "激励角度_无"
        ),
    )


def 禁止激励角度_无(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(f"属性-类型", f"类型轮廓中心-个体编码_A全或无弱抑制"),
    )
    father_inds = axon_end_inds["激励角度_无"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止激励角度_无"
        ),
    )


def 增强禁止激励角度_无(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    mother_inds.extend(
        get_soma_inds(
            "全局调控",
            "汇总所有位置位于弧线边缘且有反馈的内轮廓方位",
        )
    )
    father_inds = axon_end_inds["禁止激励角度_无"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 内轮廓方位激励尺度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方向所在位置兴奋最大且有反馈的内轮廓方位",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"属性-尺度", f"尺度{receptive_field_level}-个体编码_DMax"
                    ),
                    REGION[f"方位-S{receptive_field_level}"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "内轮廓方位激励尺度"
        ),
    )


def 激励圆弧类型(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    mother_inds.extend(
        get_soma_inds(
            f"轮廓中心",
            f"内轮廓中心的注意力竞争结果",
        )
    )
    father_inds.extend(
        np.tile(
            get_soma_inds(
                f"属性-类型",
                f"类型轮廓中心-个体编码_DMax",
            ),
            REGION["轮廓中心"]["hyper_col_sum"],
        )
    )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # 类型
        激励圆弧类型,
        # 位于开口边缘的有反馈兴奋的汇总方位，用于激励朝向和角度
        激励位于弧线边缘且有反馈的内轮廓方位,
        禁止激励位于弧线边缘且有反馈的内轮廓方位,
        解禁激励位于弧线边缘且有反馈的内轮廓方位,
        禁止解禁激励位于弧线边缘且有反馈的内轮廓方位,
        汇总位于弧线边缘且有反馈的内轮廓方位,
        # 朝向
        内轮廓方位激励朝向,
        禁止内轮廓方位激励朝向,
        解禁内轮廓方位激励朝向,
        激励朝向_无,
        禁止激励朝向_无,
        增强禁止激励朝向_无,
        # 角度
        内轮廓方位激励角度,
        禁止内轮廓方位激励角度,
        解禁内轮廓方位激励角度,
        激励角度_无,
        禁止激励角度_无,
        增强禁止激励角度_无,
        # 有反馈兴奋的最活跃的方位，用于激励尺度
        汇总所在位置的内轮廓方位,
        激励所在位置兴奋最大的内轮廓方位,
        禁止激励激励所在位置兴奋最大的内轮廓方位,
        激励所在位置兴奋最大且有反馈的内轮廓方位,
        禁止激励所在位置兴奋最大且有反馈的内轮廓方位,
        解禁激励所在位置兴奋最大且有反馈的内轮廓方位,
        # 尺度
        内轮廓方位激励尺度,
    ]
