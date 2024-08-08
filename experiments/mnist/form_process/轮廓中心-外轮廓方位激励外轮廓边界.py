from numpy.lib.npyio import save
from consts.nerve_props import RELEASE_TYPE, TYPE
from consts.feature import ORIENT_SUM, ORIENTS, CONTOUR_CENTER_ORIENTS, RECEPTIVE_FIELD_LEVELS, CONTOUR_SIDES, BOTH_SIDE_ORIENT_DESC, ORIENT_SIDES, ORIENT_CONTOUR_SIDES
from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np
import math

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 汇总各个方向各个尺度外轮廓方位的最大值(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(f'方位-S{receptive_field_level}', 
                               f'{orient}方向的外轮廓方位'))
            father_inds.extend(
                get_soma_inds('轮廓中心',  
                              f'汇总{orient}方向各个尺度的外轮廓方位的最大值_DMax'))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励各个方向各个尺度的轮廓尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(f'方位-S{receptive_field_level}', 
                               f'{orient}方向的外轮廓方位'))
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f'外轮廓边界',  
                        f'{orient}方位{receptive_field_level}尺度的外轮廓边界_DMax'),
                    REGION[f'方位-S{receptive_field_level}']
                    ['hyper_col_sum']))
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励各个方向各个尺度的轮廓尺度'))


# 在每一个柱内，在每一个方向上，只允许兴奋最大的那个尺度激励边界细胞
def 全或无禁止激励各个方向各个尺度的轮廓尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    '轮廓中心',  
                    f'汇总{orient}方向各个尺度的外轮廓方位的最大值_A全或无禁止激励各个方向各个尺度的轮廓尺度'))
    father_inds = axon_end_inds['激励各个方向各个尺度的轮廓尺度']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


# 在全局范围内，只允许位于整体中心的那个柱内的细胞激励边界细胞
def 禁止激励各个方向各个尺度的轮廓尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    '轮廓中心',  
                    f'汇总{orient}方向各个尺度的外轮廓方位的最大值_A禁止激励各个方向各个尺度的轮廓尺度'))
    father_inds = axon_end_inds['激励各个方向各个尺度的轮廓尺度']
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励各个方向各个尺度的轮廓尺度'))


def 解禁激励各个方向各个尺度的轮廓尺度(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds('轮廓中心',  
                              '外轮廓中心-注意力竞争结果出现_A解禁激励各个方向各个尺度的轮廓尺度'))
    father_inds = axon_end_inds['禁止激励各个方向各个尺度的轮廓尺度']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        汇总各个方向各个尺度外轮廓方位的最大值,
        激励各个方向各个尺度的轮廓尺度,
        全或无禁止激励各个方向各个尺度的轮廓尺度,
        禁止激励各个方向各个尺度的轮廓尺度,
        解禁激励各个方向各个尺度的轮廓尺度,
    ]
