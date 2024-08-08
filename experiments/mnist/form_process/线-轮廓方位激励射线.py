from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ORIENT_SIDES,
)
from ...util import REGION, get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}
prop_pack_list = [
    (orient_side, orient, receptive_field_level)
    for orient_side in ORIENT_SIDES
    for orient in ORIENTS
    for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS
]


def 方位激励各个尺度各个方向的射线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side, orient, receptive_field_level in prop_pack_list:
        add_levels = np.array(
            [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if level <= receptive_field_level
            ]
        )
        for add_level in add_levels:
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{add_level}", f"{orient}方向的{orient_side}侧方位"
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"线_射线-S{receptive_field_level}",
                    f"{orient}方向{orient_side}侧的射线",
                )
            )
            """ 加上尺度的信息 """
            axon_end_release_sums.extend(
                [65 / len(add_levels) * (0.5 + 0.1 * (receptive_field_level // 2))]
                * REGION[f"方位-S{add_level}"]["hyper_col_sum"]
            )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 各个方向的射线在各个尺度上的拮抗抑制(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side, orient, receptive_field_level in prop_pack_list:
        add_levels = np.array(
            [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if level <= receptive_field_level
            ]
        )
        for add_level in add_levels:
            mother_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"全局调控", f"对各个尺度的方位激励射线的拮抗抑制_A抑制"
                    ),
                    REGION[f"线_射线-S{receptive_field_level}"]["hyper_col_sum"],
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"线_射线-S{receptive_field_level}",
                    f"{orient}方向{orient_side}侧的射线",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "各个方向的射线在各个尺度上的拮抗抑制"
        ),
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def 消除各个方向的射线在各个尺度上的拮抗抑制(cortex_obj):
    mother_inds, father_inds = [], []
    for orient_side, orient, receptive_field_level in prop_pack_list:
        add_levels = np.array(
            [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if level <= receptive_field_level
            ]
        )
        for add_level in add_levels:
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{add_level}", f"{orient}方向的{orient_side}侧方位_A抑制"
                )
            )
    father_inds = axon_end_inds["各个方向的射线在各个尺度上的拮抗抑制"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 更小尺度的内侧方位抑制各个尺度各个方向的射线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for orient in ORIENTS:
            """抑制内轮廓向同侧偏移一个方位会导致内轮廓兴奋太小，无法达到抑制效果"""
            inhibit_orient = orient
            for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
                higher_receptive_field_level = receptive_field_level + 2
                inhibit_level = [
                    level
                    for level in RECEPTIVE_FIELD_LEVELS
                    if level <= higher_receptive_field_level
                ][-1]
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{inhibit_level}",
                        f"汇总{inhibit_orient}方向尺度内的内轮廓方位_求和_A抑制",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线",
                    )
                )
                axon_end_release_sums.extend(
                    np.tile(
                        [65 * (receptive_field_level // 2 + 1)],
                        REGION[f"方位-S{1}"]["hyper_col_sum"],
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def 更大尺度的内侧方位抑制各个尺度各个方向的射线(cortex_obj):
    """用于解决圆型内边缘的角被较大程度激活的问题"""
    mother_inds, father_inds = [], []
    for orient_side in ORIENT_SIDES:
        for orient in ORIENTS:
            for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
                if receptive_field_level < 3 or receptive_field_level == 21:
                    continue
                inhibit_level = receptive_field_level + 2
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{inhibit_level}",
                        f"{orient}方向的内轮廓方位_求和_A抑制",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 末端抑制各个尺度各个方向的射线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for orient in ORIENTS:
            for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
                # 最大尺度的射线不受末端抑制
                if receptive_field_level == LINE_RECEPTIVE_FIELD_LEVELS[-1]:
                    continue
                higher_receptive_field_level = receptive_field_level + 2
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{higher_receptive_field_level}",
                        f"{orient}方向的{orient_side}侧方位_A抑制",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线",
                    )
                )
                axon_end_release_sums.extend(
                    np.tile(
                        [65 * (receptive_field_level // 2 + 1)],
                        REGION[f"方位-S{higher_receptive_field_level}"][
                            "hyper_col_sum"
                        ],
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def form_init_nerve():
    return [
        方位激励各个尺度各个方向的射线,
        各个方向的射线在各个尺度上的拮抗抑制,
        消除各个方向的射线在各个尺度上的拮抗抑制,
        更小尺度的内侧方位抑制各个尺度各个方向的射线,
        更大尺度的内侧方位抑制各个尺度各个方向的射线,
        末端抑制各个尺度各个方向的射线,
    ]
