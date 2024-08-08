import numpy as np
from consts.feature import VISUAL_FIELD_WH, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE
from experiments.util import get_soma_inds

APPEAR_NERVE_SUFFIXs = [
    '群体编码出现', '群体编码出现_A前馈预测', '群体编码出现_A易化前馈预测'
    #  '群体编码出现_A前馈抑制', '群体编码出现_A易化前馈抑制'
]
DISAPPEAR_NERVE_SUFFIXs = [
    '群体编码消失', '群体编码消失_Astp预测', '群体编码消失_A易化stp预测'
    #  '群体编码消失_Astp抑制', '群体编码消失_A易化stp抑制'
]

POPU_ABSTRACT_APPEAR_INDS = np.concatenate(
    tuple([
        get_soma_inds(f'属性-{abstract_type}', [
            f'{abstract_name}-群体编码出现',
        ]) for abstract_type, abstract_values in
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
        for abstract_name, _ in abstract_values
    ]))

POPU_ABSTRACT_DISAPPEAR_INDS = np.concatenate(
    tuple([
        get_soma_inds(f'属性-{abstract_type}', [
            f'{abstract_name}-群体编码消失',
        ]) for abstract_type, abstract_values in
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
        for abstract_name, _ in abstract_values
    ]))

GENERATIVE_POPU_ABSTRACT_APPEAR_INDS = np.concatenate(
    tuple([
        get_soma_inds(f'属性-{abstract_type}', [
            f'{abstract_name}-泛化-群体编码出现',
        ]) for abstract_type, abstract_values in
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
        for abstract_name, _ in abstract_values
    ]))

GENERATIVE_POPU_ABSTRACT_DISAPPEAR_INDS = np.concatenate(
    tuple([
        get_soma_inds(f'属性-{abstract_type}', [
            f'{abstract_name}-泛化-群体编码消失',
        ]) for abstract_type, abstract_values in
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
        for abstract_name, _ in abstract_values
    ]))

POPU_ABSTRACT_DISAPPEAR_STP_INDS = np.concatenate(
    tuple([
        get_soma_inds(f'属性-{abstract_type}', [
            f'{abstract_name}-群体编码消失_Astp预测',
        ]) for abstract_type, abstract_values in
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
        for abstract_name, _ in abstract_values
    ]))

NOWA_FEATURE_GRID_INDS = get_soma_inds(
    '位置_当前特征', [f'{y_or_x}' for y_or_x in range(VISUAL_FIELD_WH[0])])

ANCHOR_FEATURE_GRID_INDS = get_soma_inds(
    '位置_锚点特征', [f'{y_or_x}' for y_or_x in range(VISUAL_FIELD_WH[0])])

WHOLE_CENTER_GRID_INDS = get_soma_inds(
    '位置_整体中心', [f'{y_or_x}' for y_or_x in range(VISUAL_FIELD_WH[0])])

SINGLE_ABSTRACT_APPEAR_INDS = np.concatenate(
    tuple([
        get_soma_inds(f'属性-{abstract_type}', f'{abstract_name}-个体编码出现')
        for abstract_type, abstract_values in
        COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
        for abstract_name, _ in abstract_values
    ]))

PREDICT_INDS = get_soma_inds(
    '数字', [f'前馈预测_DMax_棘{i}' for i in range(SPINE_SUM_ON_A_DENDRITE)])
PREDICT_INDS.sort()
PREDICT_SUPRISE_INDS = get_soma_inds('数字', '前馈预测意外')
PREDICT_BIAS_INDS = get_soma_inds('数字', '前馈预测偏差')
ACCUMULATE_PREDICT_INDS = get_soma_inds('数字', '累积前馈预测')
