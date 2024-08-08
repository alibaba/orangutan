from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}


def 激励前馈预测意外(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                'input_A激励前馈预测意外')
    father_inds = get_soma_inds('数字',  
                                '前馈预测意外')
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励前馈预测意外'))


def 抑制激励前馈预测意外(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot_A抑制')
    father_inds = axon_end_inds['激励前馈预测意外']
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '抑制激励前馈预测意外'))


def 激励前馈预测偏差(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                '累积前馈预测onehot')
    father_inds = get_soma_inds('数字',  
                                '前馈预测偏差')
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励前馈预测偏差'))


def 抑制激励前馈预测偏差(cortex_obj):
    mother_inds = get_soma_inds('数字',  
                                'input_A抑制')
    father_inds = axon_end_inds['激励前馈预测偏差']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励前馈预测意外,
        抑制激励前馈预测意外,
        激励前馈预测偏差,
        抑制激励前馈预测偏差,
    ]
