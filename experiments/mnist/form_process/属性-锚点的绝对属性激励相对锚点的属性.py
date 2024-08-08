from consts.feature import VISUAL_FIELD_WH, ORIENTS, FACE_ORIENTS, POS_ORIENTS
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves, cal_closest_orient
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def 激励相对锚点特征的方位(cortex_obj):
    mother_inds, father_inds = [], []
    for y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for x_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            for orient in FACE_ORIENTS:
                closest_orient = cal_closest_orient(y_delta, x_delta, '无')
                if closest_orient != orient:
                    continue
                mother_inds.extend(
                    get_soma_inds(f'位置_当前特征相对锚点特征的偏移', f'{y_delta}', 0))
                father_inds.extend(
                    get_soma_inds(f'属性-相对锚点的方位', f'相对锚点的方位{orient}-个体编码_DAdd'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对锚点特征的方位'))


def 禁止激励相对锚点特征的方位(cortex_obj):
    mother_inds, father_inds = [], []
    for y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for x_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            for orient in FACE_ORIENTS:
                closest_orient = cal_closest_orient(y_delta, x_delta, '无')
                if closest_orient != orient:
                    continue
                mother_inds.extend(
                    get_soma_inds(f'位置_当前特征相对锚点特征的偏移', f'{y_delta}_A抑制', 0))
    father_inds = axon_end_inds['激励相对锚点特征的方位']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对锚点特征的方位'))


def 解禁激励相对锚点特征的方位(cortex_obj):
    mother_inds, father_inds = [], []
    for y_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
        for x_delta in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1):
            for orient in FACE_ORIENTS:
                closest_orient = cal_closest_orient(y_delta, x_delta, '无')
                if closest_orient != orient:
                    continue
                mother_inds.extend(
                    get_soma_inds(f'位置_当前特征相对锚点特征的偏移', f'{x_delta}_A抑制', 1))
    father_inds = axon_end_inds['禁止激励相对锚点特征的方位']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 激励相对属性_朝向(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for relative_orient in FACE_ORIENTS:
            mother_inds.extend(
                get_soma_inds(f'属性-朝向', f'朝向{orient}-个体编码_A激励相对特征'))
            father_inds.extend(
                get_soma_inds(f'属性-相对_相对锚点的方位_的朝向',
                              f'相对_相对锚点的方位_的朝向{relative_orient}-个体编码'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对属性_朝向'))


def 禁止激励相对属性_朝向(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for relative_orient in FACE_ORIENTS:
            mother_inds.extend(
                get_soma_inds(f'属性-朝向', f'朝向{orient}-个体编码_A禁止激励相对特征'))
    father_inds = axon_end_inds['激励相对属性_朝向']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对属性_朝向'))


def 解禁激励相对属性_朝向(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for relative_orient in FACE_ORIENTS:
            head_orient = orient if relative_orient == '无' else (
                orient - relative_orient + 360) % 360. or 360.
            mother_inds.extend(
                get_soma_inds(f'属性-相对锚点的方位',
                              f'相对锚点的方位{head_orient}-个体编码_A解禁激励相对特征'))
    father_inds = axon_end_inds['禁止激励相对属性_朝向']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 激励相对属性_朝向无(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(get_soma_inds(f'属性-朝向', f'朝向无-个体编码_A激励相对特征'))
    father_inds.extend(
        get_soma_inds(f'属性-相对_相对锚点的方位_的朝向', f'相对_相对锚点的方位_的朝向无-个体编码'))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励相对属性_朝向无'))


def 禁止激励相对属性_朝向无(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(get_soma_inds(f'属性-朝向', f'朝向无-个体编码_A禁止激励相对特征'))
    father_inds = axon_end_inds['激励相对属性_朝向无']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励相对属性_朝向无'))


def 解禁激励相对属性_朝向无(cortex_obj):
    mother_inds, father_inds = [], []
    for head_orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(f'属性-相对锚点的方位',
                          f'相对锚点的方位{head_orient}-个体编码_A解禁激励相对特征'))
    father_inds = np.tile(axon_end_inds['禁止激励相对属性_朝向无'], len(ORIENTS))
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def form_init_nerve():
    return [
        激励相对锚点特征的方位,
        禁止激励相对锚点特征的方位,
        解禁激励相对锚点特征的方位,
        #
        激励相对属性_朝向,
        禁止激励相对属性_朝向,
        解禁激励相对属性_朝向,
        激励相对属性_朝向无,
        禁止激励相对属性_朝向无,
        解禁激励相对属性_朝向无,
    ]
