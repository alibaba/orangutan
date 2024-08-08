from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np
from consts.feature import COMMON_ABSTRACT_NAMES, VISUAL_FIELD_WH

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 当前特征位置激励扫视行动(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(
        get_soma_inds('位置_当前特征', [f'{y}' for y in range(VISUAL_FIELD_WH[0])],
                      0))
    father_inds = np.tile(get_soma_inds(f'全局调控', f'扫视到下个特征_DMax'),
                          VISUAL_FIELD_WH[0])
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 数字onehot激励扫视行动(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(get_soma_inds('数字', '累积前馈预测onehot'))
    father_inds = np.tile(get_soma_inds(f'全局调控', f'扫视到下个特征_DMax数字onehot'),
                          REGION['数字']['hyper_col_sum'])
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        当前特征位置激励扫视行动,
        数字onehot激励扫视行动,
    ]
