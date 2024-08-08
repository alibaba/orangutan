from consts.feature import ORIENT_SUM, ORIENTS, RECEPTIVE_FIELD_LEVELS, CONTOUR_SIDES, CONTOUR_CENTER_RECEPTIVE_FIELD_LEVELS, BOTH_SIDE_ORIENT_DESC
from ...util import get_soma_inds, REGION, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def 轮廓直线反馈激励轮廓方位复杂细胞(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    side = '内'
    for orient_ind in range(ORIENT_SUM // 2):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(f'线_轮廓直线-S{receptive_field_level}', [
                    f'{BOTH_SIDE_ORIENT_DESC[orient_ind%(ORIENT_SUM//2)]}方向_{side}轮廓直线_复杂细胞_反馈',
                ] * 2))
            father_inds.extend(
                get_soma_inds(f'方位-S{receptive_field_level}', [
                    f'{ORIENTS[orient_ind]}方向的{side}轮廓方位_复杂细胞_反馈_DMax',
                    f'{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向的{side}轮廓方位_复杂细胞_反馈_DMax',
                ]))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 轮廓方位复杂细胞反馈激励轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            for sub_receptive_field_level in [
                    level for level in RECEPTIVE_FIELD_LEVELS
                    if abs(level - receptive_field_level) <= 2
            ]:
                mother_inds.extend(
                    get_soma_inds(f'方位-S{receptive_field_level}',
                                  f'{orient}方向的内轮廓方位_复杂细胞_反馈'))
                father_inds.extend(
                    get_soma_inds(f'方位-S{sub_receptive_field_level}',
                                  f'{orient}方向的内轮廓方位_反馈_DMax'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '轮廓方位复杂细胞反馈激励轮廓方位'))


def 禁止轮廓方位复杂细胞反馈激励轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            for sub_receptive_field_level in [
                    level for level in RECEPTIVE_FIELD_LEVELS
                    if abs(level - receptive_field_level) <= 2
            ]:
                mother_inds.extend(
                    get_soma_inds(f'方位-S{receptive_field_level}',
                                  f'{orient}方向的内轮廓方位_复杂细胞_反馈_A全或无强抑制'))
    father_inds = axon_end_inds['轮廓方位复杂细胞反馈激励轮廓方位']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止轮廓方位复杂细胞反馈激励轮廓方位'))


def 解禁轮廓方位复杂细胞反馈激励轮廓方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            for sub_receptive_field_level in [
                    level for level in RECEPTIVE_FIELD_LEVELS
                    if abs(level - receptive_field_level) <= 2
            ]:
                mother_inds.extend(
                    get_soma_inds(f'方位-S{sub_receptive_field_level}',
                                  f'{orient}方向的内轮廓方位_A抑制'))
    father_inds = axon_end_inds['禁止轮廓方位复杂细胞反馈激励轮廓方位']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


# def 内轮廓直线反馈激励外轮廓方位(cortex_obj):
#     mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
#     for orient_ind in range(ORIENT_SUM // 2):
#         for receptive_field_level in RECEPTIVE_FIELD_LEVELS[1:]:
#             for lower_level in [
#                     level for level in RECEPTIVE_FIELD_LEVELS
#                     if level < receptive_field_level
#             ]:
#                 mother_inds.extend(
#                     get_soma_inds(f'线_轮廓直线-S{receptive_field_level}', [
#                         f'内轮廓中心对{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_轮廓直线的反馈'
#                     ] * 2))
#                 father_inds.extend(
#                     get_soma_inds(f'方位-S{lower_level}', [
#                         f'对{ORIENTS[orient_ind]}方向外轮廓方位的反馈_DMax',
#                         f'对{ORIENTS[orient_ind%(ORIENT_SUM//2)]}方向外轮廓方位的反馈_DMax',
#                     ]))
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 缺口直线反馈激励对向的轮廓方位(cortex_obj):
#     mother_inds, father_inds = [], []
#     side = '内'
#     for orient_ind, orient in enumerate(ORIENTS):
#         for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#             for level in [receptive_field_level]:
#                 mother_inds.extend(
#                     get_soma_inds(f'线_轮廓直线-S{receptive_field_level}',

#                                   f'内轮廓中心对{orient}方向的缺口{side}轮廓直线的反馈'))
#                 father_inds.extend(
#                     get_soma_inds(
#                         f'方位-S{receptive_field_level}',

#                         f'对{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向{side}轮廓方位的反馈_DMax'
#                     ))
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 缺口直线反馈激励同向的轮廓方位(cortex_obj):
#     mother_inds, father_inds = [], []
#     side = '内'
#     for orient_ind, orient in enumerate(ORIENTS):
#         for level_ind, receptive_field_level in enumerate(
#                 RECEPTIVE_FIELD_LEVELS):
#             levels = RECEPTIVE_FIELD_LEVELS[max(0, level_ind - 1):level_ind +
#                                             3]
#             for level in levels:
#                 mother_inds.extend(
#                     get_soma_inds(f'线_轮廓直线-S{receptive_field_level}',

#                                   f'内轮廓中心对{orient}方向的缺口{side}轮廓直线的反馈'))
#                 father_inds.extend(
#                     get_soma_inds(f'方位-S{level}',

#                                   f'对{orient}方向{side}轮廓方位的反馈_DMax'))
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        轮廓直线反馈激励轮廓方位复杂细胞,
        轮廓方位复杂细胞反馈激励轮廓方位,
        禁止轮廓方位复杂细胞反馈激励轮廓方位,
        解禁轮廓方位复杂细胞反馈激励轮廓方位,
        # 内轮廓直线反馈激励外轮廓方位,
        # 缺口直线反馈激励对向的轮廓方位,
        # 缺口直线反馈激励同向的轮廓方位,
    ]