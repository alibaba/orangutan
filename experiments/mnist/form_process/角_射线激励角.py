from consts.feature import (
    ORIENTS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    ORIENT_SIDES,
    MIN_ANGLE,
)
from ...util import REGION, get_soma_inds
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def 汇总射线最大值的axon_end_release_sums(receptive_field_level):
    return 65 * (0.85 + receptive_field_level / 60)


def 汇总各个方向的射线的最大值(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线",
                        f"汇总{orient}方向{orient_side}侧的射线的最大值_DMax",
                    )
                )
                """ 因为最大值会在传递反馈兴奋时，用于抑制对不是最大值的射线的兴奋传递突触
                    所以这里在计算最大值时，不能额外放大兴奋，否则它会大于实际的最大射线兴奋
                    导致抑制所有向射线传递兴奋的突触，无法顺利传递反馈信号
                """
                # 试一试
                """ 尺度越大，激励效果越大 """
                axon_end_release_sums.extend(
                    # np.tile([65 * (0.85 + receptive_field_level / 60)],
                    np.tile(
                        [汇总射线最大值的axon_end_release_sums(receptive_field_level)],
                        REGION[f"线_射线-S{receptive_field_level}"]["hyper_col_sum"],
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


def 激励各个角度的角(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    f"线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值",
                        f"汇总{(orient+angle)%360 or 360.0}方向左侧的射线的最大值",
                    ],
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"角",
                    [
                        f"方位{orient}和{(orient+angle)%360 or 360.0}的角_DMin",
                        f"方位{orient}和{(orient+angle)%360 or 360.0}的角_DMin",
                    ],
                )
            )
            """ 角度越大，激励效果越小 """
            axon_end_release_sums.extend(
                np.tile(
                    [65 * (1 - angle / MIN_ANGLE / 2 * 0.16)],
                    2 * REGION["线_射线"]["hyper_col_sum"],
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
        汇总各个方向的射线的最大值,
        激励各个角度的角,
    ]
