from consts.nerve_props import TYPE
from consts.nerve_params import SRP
from consts.base import GRAY_IMG_PATH
from consts.feature import RECEPTIVE_FIELD_LEVELS, global_axon_end_inds, ORIENT_SUM, ORIENTS, CONTOUR_SIDES, ORIENT_SIDES, ORIENT_CONTOUR_SIDES
from ...util import get_soma_inds, get_around_and_center_pos_inds_with_gray_img, save_axon_end_inds_with_new_nerves
import numpy as np
import itertools
import math
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}
gray_maps = {}
for orient_ind, orient in enumerate(ORIENTS):
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        gray_filefold_path = f'{GRAY_IMG_PATH}/d{receptive_field_level}'
        orient_img = math.ceil(orient) % 90 + 90
        rotate_time = orient // 90 - 1
        gray_img_path = f'{gray_filefold_path}/{orient_img}.jpg'
        around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = get_around_and_center_pos_inds_with_gray_img(
            '点',
            f'方位-S{receptive_field_level}',
            gray_img_path,
            gray_img_rotate_time=rotate_time)
        gray_maps[(orient,
                   receptive_field_level)] = (around_pos_inds, center_pos_inds,
                                              inrange_mother_pos_mask,
                                              gray_matrix)


def 反馈调节禁止激励各个尺度各个方向的轮廓方位(cortex_obj):
    mother_inds = []
    side = '内'
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = gray_maps[
                (orient, receptive_field_level)]
            # for side in CONTOUR_SIDES:
            mother_inds.extend(
                get_soma_inds('点', f'轮廓方位对边缘点的反馈_A禁止激励轮廓方位', around_pos_inds))
    father_inds = global_axon_end_inds['激励各个尺度各个方向的内轮廓方位']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '反馈调节禁止激励各个尺度各个方向的内轮廓方位'))


def 反馈调节解禁激励这个尺度这个方向的轮廓方位(cortex_obj):
    mother_inds = []
    side = '内'
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = gray_maps[
                (orient, receptive_field_level)]
            # for side in CONTOUR_SIDES:
            mother_inds.extend(
                get_soma_inds(
                    f'方位-S{receptive_field_level}',
                    f'对{orient}方向{side}轮廓方位的反馈_A解禁边缘点激励{orient}方向的{side}轮廓方位',
                    center_pos_inds))
    father_inds = axon_end_inds['反馈调节禁止激励各个尺度各个方向的内轮廓方位']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 反馈调节禁止激励各个尺度各个方向的垂直方位(cortex_obj):
    mother_inds = []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = gray_maps[
                (orient, receptive_field_level)]
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds('点', '轮廓方位对边缘点的反馈_A禁止激励轮廓方位',
                                  around_pos_inds))
    father_inds = global_axon_end_inds['激励各个尺度各个方向的垂直方位']
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '反馈调节禁止激励各个尺度各个方向的垂直方位'))


def 反馈调节解禁激励这个尺度这个方向的垂直方位(cortex_obj):
    mother_inds = []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = gray_maps[
                (orient, receptive_field_level)]
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f'方位-S{receptive_field_level}',
                        f'对{orient}方向的{orient_side}侧方位的反馈_A解禁边缘点激励{orient}方向{orient_side}侧方位',
                        center_pos_inds))
    father_inds = axon_end_inds['反馈调节禁止激励各个尺度各个方向的垂直方位']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def form_init_nerve():
    return [
        反馈调节禁止激励各个尺度各个方向的轮廓方位,
        反馈调节解禁激励这个尺度这个方向的轮廓方位,
        反馈调节禁止激励各个尺度各个方向的垂直方位,
        反馈调节解禁激励这个尺度这个方向的垂直方位,
    ]