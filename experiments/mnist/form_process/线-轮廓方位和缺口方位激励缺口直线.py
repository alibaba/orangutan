from consts.feature import ORIENT_SIDES, ORIENT_SUM, ORIENTS, RECEPTIVE_FIELD_LEVELS, CONTOUR_SIDES, BOTH_SIDE_ORIENT_DESC
from ...util import REGION, get_soma_inds
import numpy as np
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def 对向的轮廓方位激励缺口直线(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind in range(ORIENT_SUM):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            for level in [receptive_field_level]:
                mother_inds.extend(
                    get_soma_inds(f'方位-S{level}', [
                        f'{ORIENTS[(orient_ind)]}方位的缺口',
                        f'{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向的内轮廓方位',
                    ] * 1))
                father_inds.extend(
                    get_soma_inds(
                        f'线_轮廓直线-S{receptive_field_level}',
                        [
                            f'{ORIENTS[orient_ind]}方向的缺口{side}轮廓直线_DAdd{ORIENTS[orient_ind]}方向',
                            f'{ORIENTS[orient_ind]}方向的缺口{side}轮廓直线_DAdd{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向',
                            # f'{ORIENTS[orient_ind]}方向的缺口{side}轮廓直线_DAdd{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向',
                        ]))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 更小尺度的像素点抑制缺口直线(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    side = '内'
    # for orient_ind in range(ORIENT_SUM // 2):
    for orient_ind in range(ORIENT_SUM):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS[1:]:
            for lower_level in [
                    level for level in RECEPTIVE_FIELD_LEVELS
                    if level < receptive_field_level
            ]:
                mother_inds.extend(
                    get_soma_inds(f'方位-S{lower_level}', [
                        f'{ORIENTS[orient_ind]}方位的像素点_A抑制',
                        f'{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方位的像素点_A抑制'
                    ]))
                father_inds.extend(
                    get_soma_inds(f'线_轮廓直线-S{receptive_field_level}', [
                        f'{ORIENTS[orient_ind]}方向的缺口{side}轮廓直线_DAdd',
                    ] * 2))
                reset_nerve_props_matrix.extend(
                    [65 * 3 / (receptive_field_level // 2 + 1)] *
                    (REGION[f'线_轮廓直线-S{receptive_field_level}']
                     ['hyper_col_sum'] * 2))
    return make_new_nerve_packs(mother_inds,
                                father_inds,
                                cortex_obj,
                                reset_nerve_props_matrix=np.array(
                                    reset_nerve_props_matrix,
                                    dtype=[('transmitter_release_sum', 'float')]))


def form_init_nerve():
    return [
        对向的轮廓方位激励缺口直线,
        同向的轮廓方位抑制缺口直线,
        更小尺度的像素点抑制缺口直线,
    ]