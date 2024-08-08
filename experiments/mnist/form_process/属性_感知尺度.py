from consts.feature import VISUAL_FIELD_WH, ORIENT_SUM, ORIENTS, RECEPTIVE_FIELD_LEVELS, LINE_RECEPTIVE_FIELD_LEVELS, RECEPTIVE_FIELD_LEVEL_SUM, global_axon_end_inds, CONTOUR_SIDES, BOTH_SIDE_ORIENT_DESC, ANGLE_SUM, ANGLES, ANGLE_NAMES, CONTOUR_CENTER_NAMES, FEATURE_TYPES, CROSS_NAMES, ORIENT_CONTOUR_SIDES, ORIENT_SIDES
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
import itertools
import math
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 激励轮廓尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient_ind in range(ORIENT_SUM // 2):
            mother_inds.extend(
                get_soma_inds(
                    f'线_轮廓直线-S{receptive_field_level}',
                    f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_内轮廓直线_复杂细胞',
                ))
            father_inds.extend(
                get_soma_inds(f'轮廓中心', f'尺度{receptive_field_level}'))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励角的尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(f'线_射线-S{receptive_field_level}',
                                  f'{orient}方向{orient_side}侧的射线'))
                father_inds.extend(
                    get_soma_inds(f'角', f'尺度{receptive_field_level}_DMax射线'))
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 汇总角(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for angle_name in ANGLE_NAMES:
        mother_inds.extend(get_soma_inds('角', f'{angle_name}'))
        father_inds.extend(get_soma_inds('角', f'汇总角_DMax'))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 约束激励角的尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
        mother_inds.extend(get_soma_inds('角', '汇总角'))
        father_inds.extend(
            get_soma_inds('角', f'尺度{receptive_field_level}_DMin'))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


# def 注意力竞争结果激励尺度(cortex_obj):
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     for
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#         mother_inds.extend(
#             get_soma_inds(f'线_射线-S{receptive_field_level}',
#                             f'{orient}方向{orient_side}侧的射线'))
#         father_inds.extend(
#             get_soma_inds(f'角', f'尺度{receptive_field_level}'))
#     return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
#                                            cortex_obj)


def form_init_nerve():
    return [
        激励轮廓尺度,
        激励角的尺度,
        汇总角,
        约束激励角的尺度,
        # 注意力竞争结果激励尺度,
    ]
