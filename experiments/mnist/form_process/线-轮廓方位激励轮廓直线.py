from consts.feature import (
    ORIENT_SUM,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    BOTH_SIDE_ORIENT_DESC,
    ORIENT_CONTOUR_SIDES,
)
from ...util import (
    REGION,
    get_soma_inds,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def 轮廓方位激励轮廓直线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        receptive_field_levels = RECEPTIVE_FIELD_LEVELS
        for receptive_field_level in receptive_field_levels:
            level = receptive_field_level
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{level}",
                    [
                        f"{ORIENTS[orient_ind]}方向的{side}轮廓方位",
                        f"{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向的{side}轮廓方位",
                        #
                        f"{ORIENTS[orient_ind]}方向的{side}轮廓方位_复杂细胞",
                        f"{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向的{side}轮廓方位_复杂细胞",
                    ],
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"线_轮廓直线-S{receptive_field_level}",
                    [
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}方向_{side}轮廓直线_DMax{ORIENTS[orient_ind]}方向",
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}方向_{side}轮廓直线_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向",
                        #
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}方向_{side}轮廓直线_复杂细胞_DMax{ORIENTS[orient_ind]}方向",
                        f"{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}方向_{side}轮廓直线_复杂细胞_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向",
                    ],
                )
            )

            assert len(mother_inds) == len(father_inds)
            # # 如果在传递兴奋时，就让尺度削弱兴奋传递，那么兴奋的部分后续会被抑制逻辑进一步抑制，最终得到比实际更少的兴奋。
            # # 所以需要先计算兴奋和抑制，再将最终结果加上尺度的限制。所以改为把计算axon_end_release_sum的逻辑放到脑区配置里
            # axon_end_release_sums.extend([
            #     # 因为直线是两个对向方位的组合，所以尺度上要乘以2，不然内轮廓直线将很难竞争过角
            #     min(
            #         65, 65 *
            #         ((receptive_field_level * 2) / RECEPTIVE_FIELD_LEVELS[-1]))
            # ] * 2 * REGION[f'方位-S{level}']['hyper_col_sum'])
            # ''' 尝试用感知到的尺度来参与注意力竞争，而不是在激励直线时加上尺度相关的兴奋放大效果
            # '''
            axon_end_release_sums.extend(
                [65 * 2 * (0.6 + 0.15 * (receptive_field_level // 2))]
                * REGION[f"方位-S{level}"]["hyper_col_sum"]
                * 4
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def is_orient_in_range(line_orient, left_open_orient, right_open_orient):
    if left_open_orient < right_open_orient:
        return left_open_orient < line_orient < right_open_orient
    else:
        return left_open_orient < line_orient or line_orient < right_open_orient


def get_opposite_orient_ind(orient_ind):
    return (orient_ind + ORIENT_SUM // 2) % ORIENT_SUM


def get_opposite_orient(orient):
    return (orient + 180.0) % 360.0 or 360.0


def 汇总各个方向各个尺度的轮廓直线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind in range(ORIENT_SUM // 2):
        for side in ORIENT_CONTOUR_SIDES:
            if side == "内":
                receptive_field_levels = RECEPTIVE_FIELD_LEVELS
            else:  # side == '外':
                receptive_field_levels = RECEPTIVE_FIELD_LEVELS[3:]
            for receptive_field_level in receptive_field_levels:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_轮廓直线-S{receptive_field_level}",
                        [
                            f"{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线",
                            f"{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞",
                        ],
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        "线_轮廓直线",
                        [
                            f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_DMax",
                            f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞_DMax",
                        ],
                    )
                )
                """ 因为最大值会在传递反馈兴奋时，用于抑制对不是最大值的直线的兴奋传递突触
                    所以这里在计算最大值时，不能额外放大兴奋，否则它大于实际的最大直线兴奋
                    导致抑制向所有直线传递兴奋的突触，无法顺利传递反馈信号
                """
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        轮廓方位激励轮廓直线,
        汇总各个方向各个尺度的轮廓直线,
    ]
