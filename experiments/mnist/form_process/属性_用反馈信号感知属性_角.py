from consts.feature import (
    ORIENTS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    ORIENT_SIDES,
)
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION
from .角_射线激励角 import 汇总射线最大值的axon_end_release_sums

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 找到两个朝向分别可以激励的中间朝向(orient, angle):
    left_orient = orient
    right_orient = (orient + angle) % 360.0 or 360.0
    center_orient = (orient + angle / 2) % 360.0 or 360.0
    orient_deltas = 所有朝向和特定朝向的夹角(center_orient)
    close_center_orients = ORIENTS[orient_deltas == min(orient_deltas)]
    left_center_orient = close_center_orients[
        np.argmin(所有朝向和特定朝向的夹角(left_orient, close_center_orients))
    ]
    right_center_orient = close_center_orients[
        np.argmin(所有朝向和特定朝向的夹角(right_orient, close_center_orients))
    ]
    return left_center_orient, right_center_orient


def 所有朝向和特定朝向的夹角(orient, all_orient=ORIENTS):
    return np.minimum(
        np.abs(orient - all_orient),
        np.abs(orient + 360 - all_orient),
    )


def 找到两个尺度分别可以激励的中间尺度(left_scale, right_scale):
    center_scale = (left_scale + right_scale) / 2
    scale_deltas = 所有尺度和特定尺度的距离(center_scale)
    close_center_scales = RECEPTIVE_FIELD_LEVELS[scale_deltas == min(scale_deltas)]
    left_center_scale = close_center_scales[
        np.argmin(所有尺度和特定尺度的距离(left_scale, close_center_scales))
    ]
    right_center_scale = close_center_scales[
        np.argmin(所有尺度和特定尺度的距离(right_scale, close_center_scales))
    ]
    return left_center_scale, right_center_scale


def 所有尺度和特定尺度的距离(scale, all_scale=RECEPTIVE_FIELD_LEVELS):
    return np.abs(scale - all_scale)


def 激励类型(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    f"角",
                    f"方位{orient}和{(orient+angle)%360 or 360.0}的角的注意力竞争结果",
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(f"属性-类型", f"类型角-个体编码_DMax"),
                    REGION["角"]["hyper_col_sum"],
                )
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 射线激励朝向(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            left_orient, right_orient = 找到两个朝向分别可以激励的中间朝向(
                orient, angle
            )
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值",
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
                    REGION["线_射线"]["hyper_col_sum"],
                )
            )
            assert len(mother_inds) == len(father_inds)
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "射线激励朝向"
        ),
    )


def 禁止射线激励朝向(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值_A全或无强抑制",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值_A全或无强抑制",
                    ],
                )
            )
    mother_inds = mother_inds * 2
    father_inds = np.tile(axon_end_inds["射线激励朝向"], 2)
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止射线激励朝向"
        ),
    )


def 解禁射线激励朝向(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    # 用对方的反馈兴奋解禁
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值_反馈_A抑制",
                        f"汇总{orient}方向右侧的射线的最大值_反馈_A抑制",
                    ],
                )
            )
    # 用自己的反馈兴奋解禁
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值_反馈_A抑制",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值_反馈_A抑制",
                    ],
                )
            )
    father_inds = axon_end_inds["禁止射线激励朝向"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
    )


def 射线激励角度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值",
                    ],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"属性-角度",
                        [
                            f"角度{angle}-个体编码_DMax",
                        ]
                        * 2,
                    ),
                    REGION["线_射线"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "射线激励角度"
        ),
    )


def 禁止射线激励角度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值_A全或无强抑制",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值_A全或无强抑制",
                    ],
                )
            )
    mother_inds = mother_inds * 2
    father_inds = np.tile(axon_end_inds["射线激励角度"], 2)
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止射线激励角度"
        ),
    )


def 解禁射线激励角度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值_反馈_A抑制",
                        f"汇总{orient}方向右侧的射线的最大值_反馈_A抑制",
                    ],
                )
            )
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    "线_射线",
                    [
                        f"汇总{orient}方向右侧的射线的最大值_反馈_A抑制",
                        f"汇总{(orient+angle)%360. or 360.}方向左侧的射线的最大值_反馈_A抑制",
                    ],
                )
            )
    father_inds = axon_end_inds["禁止射线激励角度"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
    )


def 射线准备激励所在方向上兴奋最大的射线(cortex_obj):
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
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线_用于激励最大兴奋",
                    )
                )
                """ 汇总最大射线兴奋时用了增强，所以这里也需要对应加上增强作用，以保证后面的全或无抑制逻辑的正常工作 """
                axon_end_release_sums.extend(
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


def 射线激励所在方向上兴奋最大的射线(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线_用于激励最大兴奋",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向兴奋最大的{orient_side}侧射线_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "射线激励所在方向上兴奋最大的射线"
        ),
    )


def 所在方向上兴奋最大的射线_自突触(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向兴奋最大的{orient_side}侧射线",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向兴奋最大的{orient_side}侧射线_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 禁止射线激励所在方向上兴奋最大的射线(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线",
                        f"汇总{orient}方向{orient_side}侧的射线的最大值_A全或无弱抑制",
                    )
                )
                # father_inds.extend(
                #     get_soma_inds(
                #         f'线_射线-S{receptive_field_level}',
                #         f'{orient}方向兴奋最大的{orient_side}侧射线',
                #     ))
    father_inds = axon_end_inds["射线激励所在方向上兴奋最大的射线"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总射线尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向兴奋最大的{orient_side}侧射线",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"汇总所有方向{orient_side}侧的射线_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "汇总射线尺度"
        ),
    )


def 禁止汇总射线尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向兴奋最大的{orient_side}侧射线_A全或无强抑制",
                    )
                )
    father_inds = axon_end_inds["汇总射线尺度"]
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止汇总射线尺度"
        ),
    )


def 解禁汇总射线尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线_反馈_A抑制",
                    )
                )
    father_inds = axon_end_inds["禁止汇总射线尺度"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 射线激励尺度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for left_scale in LINE_RECEPTIVE_FIELD_LEVELS:
        for right_scale in LINE_RECEPTIVE_FIELD_LEVELS:
            left_center_scale, right_center_scale = 找到两个尺度分别可以激励的中间尺度(
                left_scale, right_scale
            )
            mother_inds.extend(
                get_soma_inds(f"线_射线-S{left_scale}", f"汇总所有方向左侧的射线")
            )
            mother_inds.extend(
                get_soma_inds(f"线_射线-S{right_scale}", f"汇总所有方向右侧的射线")
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"属性-尺度", f"尺度{left_center_scale}-个体编码_DMax"
                    ),
                    REGION[f"线_射线-S{left_scale}"]["hyper_col_sum"],
                )
            )
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f"属性-尺度", f"尺度{right_center_scale}-个体编码_DMax"
                    ),
                    REGION[f"线_射线-S{right_scale}"]["hyper_col_sum"],
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "射线激励尺度"
        ),
    )


def 禁止射线激励尺度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for left_scale in LINE_RECEPTIVE_FIELD_LEVELS:
        for right_scale in LINE_RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"线_射线-S{left_scale}", f"汇总所有方向左侧的射线_A全或无强抑制"
                )
            )
            mother_inds.extend(
                get_soma_inds(
                    f"线_射线-S{right_scale}", f"汇总所有方向右侧的射线_A全或无强抑制"
                )
            )
    father_inds = axon_end_inds["射线激励尺度"]
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "禁止射线激励尺度"
        ),
    )


def 解禁射线激励尺度(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for left_scale in LINE_RECEPTIVE_FIELD_LEVELS:
        for right_scale in LINE_RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    f"线_射线-S{right_scale}", f"汇总所有方向右侧的射线_A抑制"
                )
            )
            mother_inds.extend(
                get_soma_inds(f"线_射线-S{left_scale}", f"汇总所有方向左侧的射线_A抑制")
            )
    father_inds = axon_end_inds["禁止射线激励尺度"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # 类型
        激励类型,
        # 朝向
        射线激励朝向,
        禁止射线激励朝向,
        解禁射线激励朝向,
        # 角度
        射线激励角度,
        禁止射线激励角度,
        解禁射线激励角度,
        # 尺度
        射线准备激励所在方向上兴奋最大的射线,
        射线激励所在方向上兴奋最大的射线,
        所在方向上兴奋最大的射线_自突触,
        禁止射线激励所在方向上兴奋最大的射线,
        汇总射线尺度,
        禁止汇总射线尺度,
        解禁汇总射线尺度,
        射线激励尺度,
        禁止射线激励尺度,
        解禁射线激励尺度,
    ]
