from consts.nerve_props import TYPE
from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np
import math
import itertools
from ..regions.全局调控 import ACTION_NAMES

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 激励onehot(cortex_obj):
    mother_inds = get_soma_inds('全局调控',  
                                [f'{name}_A激励onehot' for name in ACTION_NAMES])
    father_inds = get_soma_inds('全局调控',  
                                [f'{name}onehot' for name in ACTION_NAMES])
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励onehot'))


def 激励onehot行动调控(cortex_obj):
    mother_inds = get_soma_inds('全局调控',  
                                ACTION_NAMES)
    father_inds = np.tile(
        get_soma_inds('全局调控',  
                      'onehot行动调控_DMax'), len(ACTION_NAMES))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 全或无禁止激励onehot行动调控(cortex_obj):
    mother_inds = np.tile(
        get_soma_inds('全局调控',  
                      'onehot行动调控_A全或无弱抑制'), len(ACTION_NAMES))
    father_inds = axon_end_inds['激励onehot']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励onehot,
        激励onehot行动调控,
        全或无禁止激励onehot行动调控,
    ]
