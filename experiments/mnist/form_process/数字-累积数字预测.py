from numpy.lib.npyio import save
from consts.nerve_props import TYPE
from consts.nerve_params import SRP
from consts.base import GRAY_IMG_PATH_D7, GRAY_IMG_PATH_D5, GRAY_IMG_PATH_D9, GRAY_IMG_PATH_D13
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}
from consts.experiment import EXPERIMENT_NAME
from ..regions import REGION


def 激励累积前馈预测(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '前馈预测_A激励累积前馈预测')
    father_inds = get_soma_inds('数字',  
                                '累积前馈预测_DMax')
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励累积前馈预测'))

def 禁止激励累积前馈预测(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '前馈抑制_A禁止前馈激励')
    father_inds = axon_end_inds['激励累积前馈预测']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


# def STP激励累积前馈预测(cortex_obj):
#     mother_inds = get_soma_inds('数字',  
#                                 '累积前馈预测_ASTP激励累积前馈预测')
#     father_inds = axon_end_inds['激励累积前馈预测']
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 累积前馈预测自维持(cortex_obj):
#     mother_inds = get_soma_inds('数字',  
#                                 '累积前馈预测_A自维持')
#     father_inds = get_soma_inds('数字',  
#                                 '累积前馈预测')
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 横向预测偏差抑制累积前馈预测(cortex_obj):
#     mother_inds = get_soma_inds('数字',  
#                                 '横向预测偏差抑制数字_A抑制累积前馈预测')
#     father_inds = get_soma_inds('数字',  
#                                 '累积前馈预测')
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 横向预测偏差STD激励累积前馈预测(cortex_obj):
#     mother_inds = get_soma_inds('数字',  
#                                 '横向预测偏差抑制数字_ASTD激励累积前馈预测')
#     father_inds = axon_end_inds['激励累积前馈预测']
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 横向预测偏差抑制累积前馈预测(cortex_obj):
#     mother_markers = marker.filter(cortex_obj,
#                                    marker.get('数字', '横向预测偏差抑制数字_A抑制累积前馈预测'))
#     father_markers = marker.filter(cortex_obj,
#                                    marker.get('数字', '累积前馈预测'))
#     return spring_nerve_packs_by_marker(mother_markers, father_markers,
#                                         cortex_obj)

# def 横向预测偏差STD激励累积前馈预测(cortex_obj):
#     mother_markers = marker.filter(cortex_obj,
#                                    marker.get('数字', '横向预测偏差抑制数字_A抑制累积前馈预测'))
#     # father_markers = marker.filter(cortex_obj,
#     #                                marker.get('数字', '累积前馈预测'))
#     axon_end_inds['STP激励累积前馈预测']
#     return spring_nerve_packs_by_marker(mother_markers, father_markers,
#                                         cortex_obj)

# def 易化激励累积前馈预测(cortex_obj):
#     mother_inds = get_soma_inds('数字',  
#                                 '累积前馈预测_A易化激励累积前馈预测')
#     father_inds = axon_end_inds['激励累积前馈预测']
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

# def 禁止激励累积前馈预测(cortex_obj):
#     mother_inds = np.tile(
#         get_soma_inds('全局调控',  
#                       '开启反馈预测_A抑制激励累积兴奋'), 10)
#     father_inds = axon_end_inds['激励累积前馈预测']
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 抑制累积前馈预测(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '前馈抑制_A抑制累积前馈预测')
    father_inds = get_soma_inds('数字',  
                                '累积前馈预测')
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '抑制累积前馈预测'))


def 禁止抑制累积前馈预测(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '前馈预测_A禁止前馈抑制')
    father_inds = axon_end_inds['抑制累积前馈预测']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励累积前馈预测,
        禁止激励累积前馈预测,
        抑制累积前馈预测,
        禁止抑制累积前馈预测,
        # STP激励累积前馈预测,
        # 累积前馈预测自维持,
        # 易化激励累积前馈预测,
        # 禁止激励累积前馈预测,
        # 横向预测偏差抑制累积前馈预测,
        # 横向预测偏差STD激励累积前馈预测,
    ]
