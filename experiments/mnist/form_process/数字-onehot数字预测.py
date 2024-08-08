from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from ..regions import REGION

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def 激励onehot数字预测全局调控(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测')
    father_inds = np.tile(
        get_soma_inds('全局调控',  
                      'onehot数字预测_DMax'), REGION['数字']['hyper_col_sum'])
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励数字预测onehot(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测_A激励onehot')
    father_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot_DAdd累积前馈预测')
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励数字预测onehot'))


def 全或无禁止激励数字预测onehot(cortex_obj):
    mother_inds = np.tile(
        get_soma_inds('全局调控',  
                      'onehot数字预测_A全或无弱抑制'), REGION['数字']['hyper_col_sum'])
    father_inds = axon_end_inds['激励数字预测onehot']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


# def 解禁激励数字预测onehot(cortex_obj):
#     mother_inds = get_soma_inds('数字',  
#                                 '累积前馈预测_A全或无解禁激励数字预测onehot')
#     father_inds = axon_end_inds['禁止激励数字预测onehot']
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


# def 限制激励数字预测onehot的最大值(cortex_obj):
#     mother_inds = np.tile(
#         get_soma_inds('全局调控',  
#                       '公用调控兴奋_A限制激励数字预测onehot的最大值'),
#         REGION['数字']['hyper_col_sum'])
#     father_inds = get_soma_inds('数字',  
#                                 '累积前馈预测onehot_DAdd限制累积前馈预测最大值')
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励数字预测onehot出现(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot')
    father_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot出现')
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励数字预测onehot出现'))


def 激励数字预测onehot持续(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot')
    father_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot持续')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 禁止激励数字预测onehot出现(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot持续_A禁止激励数字预测onehot出现')
    father_inds = axon_end_inds['激励数字预测onehot出现']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励onehot数字预测全局调控,
        激励数字预测onehot,
        全或无禁止激励数字预测onehot,
        # 解禁激励数字预测onehot,
        # 限制激励数字预测onehot的最大值,
        #
        激励数字预测onehot出现,
        激励数字预测onehot持续,
        禁止激励数字预测onehot出现,
    ]
