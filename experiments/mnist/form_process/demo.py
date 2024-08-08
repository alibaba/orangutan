from ..regions import REGION
from consts.feature import ORIENTS, ORIENT_SUM, PIXEL_ORIENTS, ORIENT_SIDES, RECEPTIVE_FIELD_LEVELS
from ...util import get_soma_inds, get_around_and_center_hyper_col_inds_with_around_mask, save_axon_end_inds_with_new_nerves, get_around_and_center_hyper_col_inds_with_around_mask
import numpy as np
import itertools
import math
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}

pixel_delta_masks = [
    get_around_and_center_hyper_col_inds_with_around_mask(
        '点', '点',
        np.array([
            [315, 360, 45],
            [270, np.inf, 90],
            [225, 180, 135],
        ]) == pixel_orient) for pixel_orient in PIXEL_ORIENTS
]


def get_orient_matrix(pixel_orient):
    orient_matrix = np.array([
        [315, 0 if pixel_orient < 90 else 360, 45],
        [270, np.inf, 90],
        [225, 180, 135],
    ])
    return orient_matrix


def 激励各个方位相邻点的差值(cortex_obj):
    mother_inds, father_inds = [], []
    for pixel_orient_ind, pixel_orient in enumerate(PIXEL_ORIENTS):
        around_pos_inds, center_pos_inds, _ = pixel_delta_masks[
            pixel_orient_ind]
        mother_inds.extend(get_soma_inds('点', 'input锐化_A抑制', center_pos_inds))
        father_inds.extend(
            get_soma_inds('点', f'input_DAdd抑制', around_pos_inds))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励这个方位相邻点的差值'))


def 禁止激励各个方位相邻点的差值(cortex_obj):
    mother_inds = []
    for pixel_orient_ind, pixel_orient in enumerate(PIXEL_ORIENTS):
        around_pos_inds, center_pos_inds, inrange_around_pos_mask = pixel_delta_masks[
            pixel_orient_ind]
        mother_inds.extend(get_soma_inds('点', 'input_A抑制', around_pos_inds))
    father_inds = axon_end_inds['激励这个方位相邻点的差值']
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def form_init_nerve():
    return [
        激励各个方位相邻点的差值,
        禁止激励各个方位相邻点的差值,
    ]
