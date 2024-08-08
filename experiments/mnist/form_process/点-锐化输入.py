from ..regions import REGION
from consts.feature import ORIENTS, ORIENT_SUM, PIXEL_ORIENTS, ORIENT_SIDES, RECEPTIVE_FIELD_LEVELS
from ...util import get_soma_inds, get_around_and_center_hyper_col_inds_with_around_mask, save_axon_end_inds_with_new_nerves, get_around_and_center_hyper_col_inds_with_around_mask
import numpy as np
import itertools
import math
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def 原始input激励input(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(get_soma_inds('点', 'raw_input'))
    father_inds.extend(get_soma_inds('点', 'input锐化'))
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
                                           cortex_obj)


def 四周相邻点的最大值抑制input(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    around_pos_inds, center_pos_inds, _ = get_around_and_center_hyper_col_inds_with_around_mask(
        '点',
        '点',
        np.array([
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ]).astype(bool))
    mother_inds.extend(get_soma_inds('点', 'raw_input', around_pos_inds))
    father_inds.extend(get_soma_inds('点', f'input锐化_DMax抑制', center_pos_inds))
    axon_end_release_sums.extend([65 / 2] * center_pos_inds.size)
    return form_nerve.make_new_nerve_packs(mother_inds,
                                           father_inds,
                                           cortex_obj,
                                           reset_nerve_props_matrix=np.array(
                                               axon_end_release_sums,
                                               dtype=[('transmitter_release_sum',
                                                       'float')]))


def form_init_nerve():
    return [
        原始input激励input,
        四周相邻点的最大值抑制input,
    ]
