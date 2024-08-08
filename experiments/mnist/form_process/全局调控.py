from consts.nerve_props import TYPE
from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np
import math
import itertools
axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 公用兴奋阈值自维持(cortex_obj):
    mother_inds = get_soma_inds('全局调控',  
                                '公用调控兴奋_A自维持')
    father_inds = get_soma_inds('全局调控',  
                                '公用调控兴奋')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # 公用兴奋阈值自维持,
    ]
