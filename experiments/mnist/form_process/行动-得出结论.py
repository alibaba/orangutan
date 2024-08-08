from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np
from consts.feature import COMMON_ABSTRACT_NAMES, VISUAL_FIELD_WH

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 数字激励得出结论(cortex_obj):
    mother_inds = get_soma_inds(f'数字', f'累积前馈预测onehot_A激励得出结论')
    father_inds = np.tile(get_soma_inds(f'全局调控', f'得出结论_DMax'),
                          REGION['数字']['hyper_col_sum'])
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 全或无禁止数字激励得出结论(cortex_obj):
    mother_inds = get_soma_inds(f'数字', f'累积前馈预测onehot')
    father_inds = np.tile(get_soma_inds(f'全局调控', f'得出结论_DMax全或无抑制'),
                          REGION['数字']['hyper_col_sum'])
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 当前特征位置加强禁止数字激励得出结论(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(
        get_soma_inds('位置_当前特征', [f'{y}' for y in range(VISUAL_FIELD_WH[0])],
                      0))
    father_inds = np.tile(get_soma_inds(f'全局调控', f'得出结论_DAdd全或无抑制'),
                          VISUAL_FIELD_WH[0])
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        数字激励得出结论,
        全或无禁止数字激励得出结论,
        当前特征位置加强禁止数字激励得出结论,
    ]
