from consts.feature import ORIENTS, RECEPTIVE_FIELD_LEVELS, ORIENT_SIDES
from ...util import get_soma_inds
from ...form_nerve.form_nerve import form_nerve
from .方位_各种点激励各种方位 import get_receptive_field_infos


def get_matrix_params(level):
    return {
        3: [225, 3],
        5: [135, 2],
        7: [90, 2],
        9: [45, 2],
        11: [45, 2],
    }.get(level, [None, None])


def 轮廓方位反馈激励边缘点(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        [orient_range, receptive_field_level_range] = get_matrix_params(
            receptive_field_level
        )
        for orient_ind, orient in enumerate(ORIENTS):
            (
                around_pos_inds,
                center_pos_inds,
                gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
                sum_gray_axon_end_release_sum,
            ) = get_receptive_field_infos(
                orient,
                receptive_field_level,
                orient_range=orient_range,
                receptive_field_level_range=receptive_field_level_range,
            )
            for father_orient in ORIENTS:
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的内轮廓方位_反馈",
                        center_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        "点", f"{father_orient}方向的边缘点_反馈_DMax", around_pos_inds
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 垂直方位反馈激励边缘点(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        [orient_range, receptive_field_level_range] = get_matrix_params(
            receptive_field_level
        )
        for orient_ind, orient in enumerate(ORIENTS):
            (
                around_pos_inds,
                center_pos_inds,
                gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
                sum_gray_axon_end_release_sum,
            ) = get_receptive_field_infos(
                orient,
                receptive_field_level,
                orient_range=orient_range,
                receptive_field_level_range=receptive_field_level_range,
            )
            for orient_side in ORIENT_SIDES:
                for father_orient in ORIENTS:
                    mother_inds.extend(
                        get_soma_inds(
                            f"方位-S{receptive_field_level}",
                            f"{orient}方向的{orient_side}侧方位_反馈",
                            center_pos_inds,
                        )
                    )
                    father_inds.extend(
                        get_soma_inds(
                            "点",
                            f"{father_orient}方向的边缘点_反馈_DMax",
                            around_pos_inds,
                        )
                    )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        轮廓方位反馈激励边缘点,
        垂直方位反馈激励边缘点,
    ]
