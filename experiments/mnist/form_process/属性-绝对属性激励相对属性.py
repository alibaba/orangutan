from consts.feature import POS_ORIENTS, ORIENT_SUM, VISUAL_FIELD_WH, ORIENTS, RECEPTIVE_FIELD_LEVELS, SCALE_LEVEL_RATIOS, FACE_ORIENTS
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves, cal_closest_orient
import numpy as np
import math
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def 激励相对属性_相对整体的方位(cortex_obj):
    mother_inds, father_inds = [], []
    for y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for x_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            for orient in POS_ORIENTS:
                closest_orient = cal_closest_orient(y_delta, x_delta, '无')
                if closest_orient != orient:
                    continue
                mother_inds.extend(
                    get_soma_inds(f'位置_当前特征相对整体中心的偏移', f'{y_delta}', 0))
                father_inds.extend(
                    get_soma_inds(f'属性-相对整体的方位', f'相对整体的方位{orient}-个体编码'))
                    # get_soma_inds(f'属性-相对整体的方位', f'相对整体的方位{orient}-个体编码_DAdd'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对属性_相对整体的方位'))


def 禁止激励相对属性_相对整体的方位(cortex_obj):
    mother_inds, father_inds = [], []
    for y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for x_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            for orient in POS_ORIENTS:
                closest_orient = cal_closest_orient(y_delta, x_delta, '无')
                if closest_orient != orient:
                    continue
                mother_inds.extend(
                    get_soma_inds(f'位置_当前特征相对整体中心的偏移', f'{y_delta}_A抑制', 0))
    father_inds = axon_end_inds['激励相对属性_相对整体的方位']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对属性_相对整体的方位'))


def 解禁激励相对属性_相对整体的方位(cortex_obj):
    mother_inds, father_inds = [], []
    for y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for x_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            for orient in POS_ORIENTS:
                closest_orient = cal_closest_orient(y_delta, x_delta, '无')
                if closest_orient != orient:
                    continue
                mother_inds.extend(
                    get_soma_inds(f'位置_当前特征相对整体中心的偏移', f'{x_delta}_A抑制', 1))
    father_inds = axon_end_inds['禁止激励相对属性_相对整体的方位']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 激励_相对_相对整体的方位_的朝向(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in FACE_ORIENTS:
        for relative_orient in FACE_ORIENTS:
            mother_inds.extend(
                get_soma_inds(f'属性-朝向', f'朝向{orient}-个体编码_A激励相对特征'))
            father_inds.extend(
                get_soma_inds(f'属性-相对_相对整体的方位_的朝向',
                              f'相对_相对整体的方位_的朝向{relative_orient}-个体编码'))

    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励_相对_相对整体的方位_的朝向'))


def 激励_相对_相对整体的方位_的朝向_无(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(get_soma_inds(f'属性-朝向', f'朝向无-个体编码_A激励相对特征'))
    mother_inds.extend(get_soma_inds(f'属性-相对整体的方位', f'相对整体的方位无-个体编码_A激励相对特征'))
    father_inds.extend(
        np.tile(
            get_soma_inds(f'属性-相对_相对整体的方位_的朝向', f'相对_相对整体的方位_的朝向无-个体编码_DMax'),
            2))

    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 禁止激励_相对_相对整体的方位_的朝向(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in FACE_ORIENTS:
        for relative_orient in FACE_ORIENTS:
            mother_inds.extend(
                get_soma_inds(f'属性-朝向', f'朝向{orient}-个体编码_A禁止激励相对特征'))
    father_inds = axon_end_inds['激励_相对_相对整体的方位_的朝向']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励_相对_相对整体的方位_的朝向'))


def 解禁激励_相对_相对整体的方位_的朝向(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in FACE_ORIENTS:
        for relative_orient in FACE_ORIENTS:
            head_orient = (orient - relative_orient + 360) % 360. or 360.
            mother_inds.extend(
                get_soma_inds(f'属性-相对整体的方位',
                            f'相对整体的方位{head_orient}-个体编码_A解禁激励相对特征'))

    # # 相对整体的方位无可以解禁所有朝向
    # mother_inds.extend(
    #     list(get_soma_inds(f'属性-相对整体的方位', '相对整体的方位无-个体编码_A解禁激励相对特征')) *
    #     len(axon_end_inds['禁止激励_相对_相对整体的方位_的朝向']))

    father_inds = np.tile(axon_end_inds['禁止激励_相对_相对整体的方位_的朝向'], 1)
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


# def 激励_相对_相对整体的方位_的朝向无(cortex_obj):
#     mother_inds, father_inds = [], []
#     mother_inds.extend(get_soma_inds(f'属性-朝向', f'朝向无-个体编码_A激励相对特征'))
#     father_inds.extend(
#         get_soma_inds(f'属性-相对_相对整体的方位_的朝向', f'相对_相对整体的方位_的朝向无-个体编码'))
#     return form_nerve.make_new_nerve_packs(
#         mother_inds,
#         father_inds,
#         cortex_obj,
#         new_nerve_callback=save_axon_end_inds_with_new_nerves(
#             axon_end_inds, '激励_相对_相对整体的方位_的朝向无'))

# def 禁止激励_相对_相对整体的方位_的朝向无(cortex_obj):
#     mother_inds, father_inds = [], []
#     mother_inds.extend(get_soma_inds(f'属性-朝向', f'朝向无-个体编码_A禁止激励相对特征'))
#     father_inds = axon_end_inds['激励_相对_相对整体的方位_的朝向无']
#     return form_nerve.make_new_nerve_packs(
#         mother_inds,
#         father_inds,
#         cortex_obj,
#         new_nerve_callback=save_axon_end_inds_with_new_nerves(
#             axon_end_inds, '禁止激励_相对_相对整体的方位_的朝向无'))

# def 解禁激励_相对_相对整体的方位_的朝向无(cortex_obj):
#     mother_inds, father_inds = [], []
#     for orient in POS_ORIENTS:
#         mother_inds.extend(
#             get_soma_inds(f'属性-相对整体的方位', f'相对整体的方位{orient}-个体编码_A解禁激励相对特征'))
#     father_inds = np.tile(axon_end_inds['禁止激励_相对_相对整体的方位_的朝向无'],
#                           len(POS_ORIENTS))
#     return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
#                                            cortex_obj)


def 激励相对属性_相对锚点的距离(cortex_obj):
    mother_inds, father_inds = [], []
    for offset_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for offset_x in range(-VISUAL_FIELD_WH[1], VISUAL_FIELD_WH[1] + 1):
            distance = math.sqrt(math.pow(offset_y, 2) + math.pow(offset_x, 2))
            # distance = distance * 2 + 1
            closest_receptive_field_level = RECEPTIVE_FIELD_LEVELS[np.argmin(
                np.abs(RECEPTIVE_FIELD_LEVELS - distance))]
            if abs(closest_receptive_field_level - distance) > 1:
                continue
            mother_inds.extend(
                get_soma_inds('位置_当前特征相对锚点特征的偏移', f'{offset_y}', 0))
            father_inds.extend(
                get_soma_inds(
                    f'属性-相对锚点的距离',
                    f'相对锚点的距离{closest_receptive_field_level}-个体编码_DAdd'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对属性_相对锚点的距离'))


def 禁止激励相对属性_相对锚点的距离(cortex_obj):
    mother_inds, father_inds = [], []
    for offset_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for offset_x in range(-VISUAL_FIELD_WH[1], VISUAL_FIELD_WH[1] + 1):
            distance = math.sqrt(math.pow(offset_y, 2) + math.pow(offset_x, 2))
            # distance = distance * 2 + 1
            closest_receptive_field_level = RECEPTIVE_FIELD_LEVELS[np.argmin(
                np.abs(RECEPTIVE_FIELD_LEVELS - distance))]
            if abs(closest_receptive_field_level - distance) > 1:
                continue
            mother_inds.extend(
                get_soma_inds('位置_当前特征相对锚点特征的偏移', f'{offset_y}_A抑制', 0))
    father_inds = axon_end_inds['激励相对属性_相对锚点的距离']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对属性_相对锚点的距离'))


def 解禁激励相对属性_相对锚点的距离(cortex_obj):
    mother_inds, father_inds = [], []
    for offset_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for offset_x in range(-VISUAL_FIELD_WH[1], VISUAL_FIELD_WH[1] + 1):
            distance = math.sqrt(math.pow(offset_y, 2) + math.pow(offset_x, 2))
            # distance = distance * 2 + 1
            closest_receptive_field_level = RECEPTIVE_FIELD_LEVELS[np.argmin(
                np.abs(RECEPTIVE_FIELD_LEVELS - distance))]
            if abs(closest_receptive_field_level - distance) > 1:
                continue
            mother_inds.extend(
                get_soma_inds('位置_当前特征相对锚点特征的偏移', f'{offset_x}_A抑制', 1))
    father_inds = axon_end_inds['禁止激励相对属性_相对锚点的距离']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 激励相对属性_相对整体中心的距离(cortex_obj):
    mother_inds, father_inds = [], []
    for offset_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for offset_x in range(-VISUAL_FIELD_WH[1], VISUAL_FIELD_WH[1] + 1):
            distance = math.sqrt(math.pow(offset_y, 2) + math.pow(offset_x, 2))
            # distance = distance * 2 + 1
            closest_receptive_field_level = RECEPTIVE_FIELD_LEVELS[np.argmin(
                np.abs(RECEPTIVE_FIELD_LEVELS - distance))]
            if abs(closest_receptive_field_level - distance) > 1:
                continue
            mother_inds.extend(
                get_soma_inds('位置_当前特征相对整体中心的偏移', f'{offset_y}', 0))
            father_inds.extend(
                get_soma_inds(
                    f'属性-相对整体中心的距离',
                    f'相对整体中心的距离{closest_receptive_field_level}-个体编码_DAdd'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对属性_相对整体中心的距离'))


def 禁止激励相对属性_相对整体中心的距离(cortex_obj):
    mother_inds, father_inds = [], []
    for offset_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for offset_x in range(-VISUAL_FIELD_WH[1], VISUAL_FIELD_WH[1] + 1):
            distance = math.sqrt(math.pow(offset_y, 2) + math.pow(offset_x, 2))
            # distance = distance * 2 + 1
            closest_receptive_field_level = RECEPTIVE_FIELD_LEVELS[np.argmin(
                np.abs(RECEPTIVE_FIELD_LEVELS - distance))]
            if abs(closest_receptive_field_level - distance) > 1:
                continue
            mother_inds.extend(
                get_soma_inds('位置_当前特征相对整体中心的偏移', f'{offset_y}_A抑制', 0))
    father_inds = axon_end_inds['激励相对属性_相对整体中心的距离']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对属性_相对整体中心的距离'))


def 解禁激励相对属性_相对整体中心的距离(cortex_obj):
    mother_inds, father_inds = [], []
    for offset_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for offset_x in range(-VISUAL_FIELD_WH[1], VISUAL_FIELD_WH[1] + 1):
            distance = math.sqrt(math.pow(offset_y, 2) + math.pow(offset_x, 2))
            # distance = distance * 2 + 1
            closest_receptive_field_level = RECEPTIVE_FIELD_LEVELS[np.argmin(
                np.abs(RECEPTIVE_FIELD_LEVELS - distance))]
            if abs(closest_receptive_field_level - distance) > 1:
                continue
            mother_inds.extend(
                get_soma_inds('位置_当前特征相对整体中心的偏移', f'{offset_x}_A抑制', 1))
    father_inds = axon_end_inds['禁止激励相对属性_相对整体中心的距离']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 激励相对属性_相对整体中心的距离相对整体尺度的比例(cortex_obj):
    mother_inds, father_inds = [], []

    for whole_scale_level in RECEPTIVE_FIELD_LEVELS:
        for distance_scale_level in RECEPTIVE_FIELD_LEVELS:
            raw_ratio = distance_scale_level / whole_scale_level
            ratio = SCALE_LEVEL_RATIOS[np.argmin(
                np.abs(SCALE_LEVEL_RATIOS - raw_ratio))]
            if abs(raw_ratio - ratio) > .1:
                continue

            mother_inds.extend(
                get_soma_inds(f'属性-相对整体中心的距离',
                              f'相对整体中心的距离{distance_scale_level}-个体编码_A激励相对特征'))
            father_inds.extend(
                get_soma_inds(f'属性-相对整体中心的距离相对整体尺度的比例',
                              f'相对整体中心的距离相对整体尺度的比例{ratio}-个体编码_DAdd'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对属性_相对整体中心的距离相对整体尺度的比例'))


def 禁止激励相对属性_相对整体中心的距离相对整体尺度的比例(cortex_obj):
    mother_inds, father_inds = [], []
    for whole_scale_level in RECEPTIVE_FIELD_LEVELS:
        for distance_scale_level in RECEPTIVE_FIELD_LEVELS:
            raw_ratio = distance_scale_level / whole_scale_level
            ratio = SCALE_LEVEL_RATIOS[np.argmin(
                np.abs(SCALE_LEVEL_RATIOS - raw_ratio))]
            if abs(raw_ratio - ratio) > .1:
                continue

            mother_inds.extend(
                get_soma_inds(
                    f'属性-相对整体中心的距离',
                    f'相对整体中心的距离{distance_scale_level}-个体编码_A禁止激励相对特征'))
    father_inds = axon_end_inds['激励相对属性_相对整体中心的距离相对整体尺度的比例']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对属性_相对整体中心的距离相对整体尺度的比例'))


def 解禁激励相对属性_相对整体中心的距离相对整体尺度的比例(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for whole_scale_level in RECEPTIVE_FIELD_LEVELS:
            for distance_scale_level in RECEPTIVE_FIELD_LEVELS:
                raw_ratio = distance_scale_level / whole_scale_level
                ratio = SCALE_LEVEL_RATIOS[np.argmin(
                    np.abs(SCALE_LEVEL_RATIOS - raw_ratio))]
                if abs(raw_ratio - ratio) > .1:
                    continue

                mother_inds.extend(
                    get_soma_inds(
                        f'外轮廓边界',
                        f'{orient}方位{whole_scale_level}尺度的外轮廓边界_A解禁激励相对特征'))
    father_inds = np.tile(axon_end_inds['禁止激励相对属性_相对整体中心的距离相对整体尺度的比例'],
                          ORIENT_SUM)
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '解禁激励相对属性_相对整体中心的距离相对整体尺度的比例'))


def 禁止解禁激励相对属性_相对整体中心的距离相对整体尺度的比例(cortex_obj):
    ''' 比例是某个具体方位上的比例，因此需要加入方位上的限制 '''
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for whole_scale_level in RECEPTIVE_FIELD_LEVELS:
            for distance_scale_level in RECEPTIVE_FIELD_LEVELS:
                raw_ratio = distance_scale_level / whole_scale_level
                ratios = SCALE_LEVEL_RATIOS[np.abs(SCALE_LEVEL_RATIOS -
                                                   raw_ratio) < .1]
                if len(ratios) == 0:
                    continue

                mother_inds.extend(
                    get_soma_inds(
                        f'外轮廓边界',
                        f'{orient}方位{whole_scale_level}尺度的外轮廓边界_A禁止解禁激励相对特征'))
    father_inds = axon_end_inds['解禁激励相对属性_相对整体中心的距离相对整体尺度的比例']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止解禁激励相对属性_相对整体中心的距离相对整体尺度的比例'))


def 解禁解禁激励相对属性_相对整体中心的距离相对整体尺度的比例(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for whole_scale_level in RECEPTIVE_FIELD_LEVELS:
            for distance_scale_level in RECEPTIVE_FIELD_LEVELS:
                raw_ratio = distance_scale_level / whole_scale_level
                ratios = SCALE_LEVEL_RATIOS[np.abs(SCALE_LEVEL_RATIOS -
                                                   raw_ratio) < .1]
                if len(ratios) == 0:
                    continue

                mother_inds.extend(
                    get_soma_inds(f'属性-相对整体的方位',
                                  f'相对整体的方位{orient}-个体编码_A解禁激励相对特征'))

    # 相对整体的方位无可以解禁所有朝向
    mother_inds.extend(
        list(get_soma_inds(f'属性-相对整体的方位', '相对整体的方位无-个体编码_A解禁激励相对特征')) *
        len(axon_end_inds['禁止解禁激励相对属性_相对整体中心的距离相对整体尺度的比例']))

    father_inds = np.tile(axon_end_inds['禁止解禁激励相对属性_相对整体中心的距离相对整体尺度的比例'], 2)
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def form_init_nerve():
    return [
        激励相对属性_相对整体的方位,
        禁止激励相对属性_相对整体的方位,
        解禁激励相对属性_相对整体的方位,
        #
        激励_相对_相对整体的方位_的朝向,
        激励_相对_相对整体的方位_的朝向_无,
        禁止激励_相对_相对整体的方位_的朝向,
        解禁激励_相对_相对整体的方位_的朝向,
        # #
        # 激励_相对_相对整体的方位_的朝向无,
        # 禁止激励_相对_相对整体的方位_的朝向无,
        # 解禁激励_相对_相对整体的方位_的朝向无,
        #
        激励相对属性_相对锚点的距离,
        禁止激励相对属性_相对锚点的距离,
        解禁激励相对属性_相对锚点的距离,
        #
        激励相对属性_相对整体中心的距离,
        禁止激励相对属性_相对整体中心的距离,
        解禁激励相对属性_相对整体中心的距离,
        #
        激励相对属性_相对整体中心的距离相对整体尺度的比例,
        禁止激励相对属性_相对整体中心的距离相对整体尺度的比例,
        解禁激励相对属性_相对整体中心的距离相对整体尺度的比例,
        禁止解禁激励相对属性_相对整体中心的距离相对整体尺度的比例,
        解禁解禁激励相对属性_相对整体中心的距离相对整体尺度的比例,
    ]
