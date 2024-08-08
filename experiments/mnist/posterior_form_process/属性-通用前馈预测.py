import numpy as np
from ...form_nerve.marker import Marker
from ...form_nerve.form_nerve import form_nerve
from ...util import save_new_marker_2_map
from consts.feature import COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from ..regions import REGION
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE
from consts.nerve_props import TYPE, SYNAPSE_TYPE
import itertools

marker = Marker(REGION)
spring_nerve_packs_by_marker = form_nerve.spring_nerve_packs_by_marker
axon_end_markers = {}
MARKER_REMAIN_THRESHOLD = 1

need_add_LTP_appear_nerve_inds = []
need_add_LTP_disappear_nerve_inds = []


def 属性前馈预测数字(cortex_obj):
    global need_add_LTP_appear_nerve_inds
    need_add_LTP_appear_nerve_inds = []
    mother_filter_markers, father_filter_markers = [], []

    mother_filter_markers = list(
        itertools.chain(*[[
            marker.get(f'属性-{abstract_type}', f'{abstract_name}-群体编码出现_A前馈预测'),
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-泛化-群体编码出现_A前馈预测')
        ] for abstract_type, abstract_values in
                          COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
                          for abstract_name, _ in abstract_values]))
    mother_marker_inds = marker.filter(cortex_obj, mother_filter_markers)
    mother_marker_inds = mother_marker_inds[
        cortex_obj.cortex['marker_remain'][mother_marker_inds] >
        MARKER_REMAIN_THRESHOLD]

    father_filter_markers.extend([
        marker.get('数字', f'前馈预测_DMax_棘{i}')
        for i in range(SPINE_SUM_ON_A_DENDRITE)
    ])
    father_marker_inds = marker.filter(cortex_obj, father_filter_markers)

    def reset_nerve_props(cortex_obj, new_nerve_slice, mother_inds,
                          father_inds):
        # 把预测的数字ind存在marker_exinfo1里
        cortex_obj.cortex['exinfo_1'][new_nerve_slice] = father_inds

    def new_nerve_callback(nerve_slice_or_inds, cortex_obj):

        save_new_marker_2_map(axon_end_markers, '属性前馈预测')(nerve_slice_or_inds,
                                                          cortex_obj)

        need_add_LTP_appear_nerve_inds.extend(
            cortex_obj.cortex['ind'][nerve_slice_or_inds])

    return spring_nerve_packs_by_marker(
        mother_marker_inds,
        father_marker_inds,
        cortex_obj,
        new_nerve_callback=new_nerve_callback,
        reset_nerve_props_lambda=reset_nerve_props,
        is_posterior=2,
        synapse_type=SYNAPSE_TYPE['excite'],
    )


def 易化属性前馈预测数字(cortex_obj):
    global need_add_LTP_appear_nerve_inds
    mother_filter_markers, father_filter_markers = [], []

    mother_filter_markers = list(
        itertools.chain(*[[
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-群体编码出现_A易化前馈预测'),
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-泛化-群体编码出现_A易化前馈预测')
        ] for abstract_type, abstract_values in
                          COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
                          for abstract_name, _ in abstract_values]))
    mother_marker_inds = marker.filter(cortex_obj, mother_filter_markers)
    mother_marker_inds = mother_marker_inds[
        cortex_obj.cortex['marker_remain'][mother_marker_inds] >
        MARKER_REMAIN_THRESHOLD]

    father_filter_markers.extend(axon_end_markers.get(f'属性前馈预测', []))
    father_filter_markers.extend(axon_end_markers.get(f'易化属性前馈预测', []))
    father_marker_inds = marker.filter(cortex_obj, father_filter_markers)

    def reset_nerve_props(cortex_obj, new_nerve_slice, mother_inds,
                          father_inds):
        # 突触后神经突的marker_exinfo1存放着预测的数字ind，需要继承下来，存在marker_exinfo1里
        cortex_obj.cortex['exinfo_1'][new_nerve_slice] = cortex_obj.cortex[
            'exinfo_1'][father_inds]

    def new_nerve_callback(nerve_slice_or_inds, cortex_obj):

        save_new_marker_2_map(axon_end_markers,
                              '易化属性前馈预测')(nerve_slice_or_inds, cortex_obj)

        need_add_LTP_appear_nerve_inds.extend(
            cortex_obj.cortex['ind'][nerve_slice_or_inds])

        cortex_obj.write_cortex('new_fa_nerve')

    is_loop = None

    def add_LTP_lambda(new_nerve_slice, existed_nerve_inds):
        nonlocal is_loop
        is_loop = len(new_nerve_slice) > 0 or len(existed_nerve_inds) > 0
        if not is_loop:
            form_nerve.add_LTP_with_form_and_firm_nerve_inds(
                cortex_obj, need_add_LTP_appear_nerve_inds, 'appear')

    new_nerve_slice, existed_nerve_inds = spring_nerve_packs_by_marker(
        mother_marker_inds,
        father_marker_inds,
        cortex_obj,
        new_nerve_callback=new_nerve_callback,
        reset_nerve_props_lambda=reset_nerve_props,
        add_LTP_lambda=add_LTP_lambda,
        is_posterior=2,
        synapse_type=SYNAPSE_TYPE['Fa'],
    )

    return [
        new_nerve_slice,
        existed_nerve_inds,
        is_loop,
    ]


def STP属性前馈预测数字(cortex_obj):
    global need_add_LTP_disappear_nerve_inds
    need_add_LTP_disappear_nerve_inds = []
    mother_filter_markers, father_filter_markers = [], []

    mother_filter_markers = list(
        itertools.chain(*[[
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-群体编码消失_Astp预测'),
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-泛化-群体编码消失_Astp预测')
        ] for abstract_type, abstract_values in
                          COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
                          for abstract_name, _ in abstract_values]))
    mother_marker_inds = marker.filter(cortex_obj, mother_filter_markers)
    mother_marker_inds = mother_marker_inds[
        cortex_obj.cortex['marker_remain'][mother_marker_inds] >
        MARKER_REMAIN_THRESHOLD]

    father_filter_markers.extend(axon_end_markers.get(f'属性前馈预测', []))
    father_filter_markers.extend(axon_end_markers.get(f'易化属性前馈预测', []))
    father_filter_markers.extend(axon_end_markers.get(f'STP属性前馈预测', []))
    father_filter_markers.extend(axon_end_markers.get(f'易化STP属性前馈预测', []))
    father_marker_inds = marker.filter(cortex_obj, father_filter_markers)

    # father_marker_inds = father_marker_inds[
    #     cortex_obj.cortex['marker_remain'][father_marker_inds] > 3.5]

    # # 适当降低属性消失stp细胞的marker_remain，让其只能竞争过那些非常不稳定的属性出现易化细胞
    # cortex_obj.cortex['marker_remain'][mother_marker_inds] *= .2

    def reset_nerve_props(cortex_obj, new_nerve_slice, mother_inds,
                          father_inds):
        # 突触后神经突的marker_exinfo1存放着预测的数字ind，需要继承下来，存在marker_exinfo1里
        cortex_obj.cortex['exinfo_1'][new_nerve_slice] = cortex_obj.cortex[
            'exinfo_1'][father_inds]

    def new_nerve_callback(nerve_slice_or_inds, cortex_obj):
        cortex = cortex_obj.cortex

        save_new_marker_2_map(axon_end_markers,
                              'STP属性前馈预测')(nerve_slice_or_inds, cortex_obj)

        need_add_LTP_disappear_nerve_inds.extend(
            cortex['ind'][nerve_slice_or_inds])

        # #
        # ''' 上一组特征属性与当前特征属性细胞（出现或消失）的突触建立STP后，需要将father的marker_remain重置
        #     让后面的易化stp细胞以及下一轮特征序列的stp细胞，无法与这些突触建立突触，避免混淆
        # '''
        # cortex_obj.reset_cortex_props_to_initial_state(
        #     reset_inds=cortex['post_ind'][nerve_slice_or_inds],
        #     include_props=['marker_remain'])
        # cortex_obj.write_cortex('new_nerve')

        # 除了本次发生或强化的突触，重置其他类型为4、5的突触
        reset_marker_remain_inds = cortex['ind'][np.isin(
            cortex['synapse_type'],
            [SYNAPSE_TYPE['STP'], SYNAPSE_TYPE['Fa_STP']])],
        reserve_marker_remain_inds = nerve_slice_or_inds
        reserve_marker_remain = cortex['marker_remain'][
            reserve_marker_remain_inds]
        cortex_obj.reset_cortex_props_to_initial_state(
            reset_inds=reset_marker_remain_inds,
            include_props=['marker_remain'])
        cortex['marker_remain'][
            reserve_marker_remain_inds] = reserve_marker_remain

    return spring_nerve_packs_by_marker(
        mother_marker_inds,
        father_marker_inds,
        cortex_obj,
        new_nerve_callback=new_nerve_callback,
        reset_nerve_props_lambda=reset_nerve_props,
        is_posterior=2,
        synapse_type=SYNAPSE_TYPE['STP'],
    )


def 易化STP属性前馈预测数字(cortex_obj):
    global need_add_LTP_disappear_nerve_inds
    mother_filter_markers, father_filter_markers = [], []

    mother_filter_markers = list(
        itertools.chain(*[[
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-群体编码消失_A易化stp预测'),
            marker.get(f'属性-{abstract_type}',
                       f'{abstract_name}-泛化-群体编码消失_A易化stp预测')
        ] for abstract_type, abstract_values in
                          COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
                          for abstract_name, _ in abstract_values]))
    mother_marker_inds = marker.filter(cortex_obj, mother_filter_markers)
    mother_marker_inds = mother_marker_inds[
        cortex_obj.cortex['marker_remain'][mother_marker_inds] >
        MARKER_REMAIN_THRESHOLD]

    father_filter_markers.extend(axon_end_markers.get(f'STP属性前馈预测', []))
    father_filter_markers.extend(axon_end_markers.get(f'易化STP属性前馈预测', []))
    father_marker_inds = marker.filter(cortex_obj, father_filter_markers)

    def reset_nerve_props(cortex_obj, new_nerve_slice, mother_inds,
                          father_inds):
        # 突触后神经突的marker_exinfo1存放着预测的数字ind，需要继承下来，存在marker_exinfo1里
        cortex_obj.cortex['exinfo_1'][new_nerve_slice] = cortex_obj.cortex[
            'exinfo_1'][father_inds]

    def new_nerve_callback(nerve_slice_or_inds, cortex_obj):
        save_new_marker_2_map(axon_end_markers,
                              '易化STP属性前馈预测')(nerve_slice_or_inds, cortex_obj)
        need_add_LTP_disappear_nerve_inds.extend(
            cortex_obj.cortex['ind'][nerve_slice_or_inds])

    is_loop = None

    def add_LTP_lambda(new_nerve_slice, existed_nerve_inds):
        nonlocal is_loop
        is_loop = len(new_nerve_slice) > 0 or len(existed_nerve_inds) > 0
        if not is_loop:
            form_nerve.add_LTP_with_form_and_firm_nerve_inds(
                cortex_obj, need_add_LTP_disappear_nerve_inds, 'disappear')

    new_nerve_slice, existed_nerve_inds = spring_nerve_packs_by_marker(
        mother_marker_inds,
        father_marker_inds,
        cortex_obj,
        new_nerve_callback=new_nerve_callback,
        reset_nerve_props_lambda=reset_nerve_props,
        add_LTP_lambda=add_LTP_lambda,
        is_posterior=2,
        synapse_type=SYNAPSE_TYPE['Fa_STP'],
    )

    return [
        new_nerve_slice,
        existed_nerve_inds,
        is_loop,
    ]


def form_init_nerve(cortex_obj):
    return [
        # # stp细胞不能和同属于当前特征的预测抽象细胞建立突触，所以要先于当前预测抽象细胞和其他之前被建立或强化的突触建立突触
        # STP属性前馈预测数字,
        # 易化STP属性前馈预测数字,
        #
        属性前馈预测数字,
        易化属性前馈预测数字,
        #
        STP属性前馈预测数字,
        易化STP属性前馈预测数字,
    ]