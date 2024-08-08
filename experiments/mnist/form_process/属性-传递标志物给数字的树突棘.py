from consts.feature import COMMON_ABSTRACT_NAMES, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from ...util import REGION, get_soma_inds
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from consts.nerve_params import SPINE_SENSITIVE_ABSTRACT_TYPES_LIST, SPINE_SENSITIVE_ABSTRACT_COMBINATIONS_LIST, SPINE_IND_MAPS

axon_end_inds = {}


def 传递标志物给数字的树突棘(cortex_obj):
    mother_inds, father_inds, transmitter_release_sum = [], [], []

    for spine_sensitive_abstract_combinations, spine_sensitive_abstract_types, spine_ind_map in zip(
            SPINE_SENSITIVE_ABSTRACT_COMBINATIONS_LIST,
            SPINE_SENSITIVE_ABSTRACT_TYPES_LIST,
            SPINE_IND_MAPS,
    ):

        for spine_sensitive_abstract_combination in spine_sensitive_abstract_combinations:
            spine_ind = spine_ind_map[spine_sensitive_abstract_combination]

            for abstract_type, peak_abstract_name_ind in zip(
                    spine_sensitive_abstract_types,
                    spine_sensitive_abstract_combination):
                abstract_info_list = COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES[
                    abstract_type]
                abstract_name_inds = np.arange(len(abstract_info_list))
                close_abstract_name_inds = [
                    abstract_name_ind
                    for abstract_name_ind in abstract_name_inds
                    if abs(abstract_name_ind - peak_abstract_name_ind) < 1
                ]

                for close_abstract_name_ind in close_abstract_name_inds:
                    abstract_name, abstract_type = abstract_info_list[
                        close_abstract_name_ind]
                    mother_inds.extend(
                        np.tile(
                            get_soma_inds(f'属性-{abstract_type}',
                                           
                                          f'{abstract_name}-群体编码出现_A转运标记物'),
                            10))
                    father_inds.extend(
                        get_soma_inds('数字',  
                                      f'前馈预测_DMax_棘{spine_ind}'))
                                    #   f'前馈预测_DMax_棘{spine_ind}_{abstract_type}'))
                    abstract_name_ind_offset = abs(close_abstract_name_ind -
                                                   peak_abstract_name_ind)
                    transmitter_release_sum.extend(
                        [65 * (1 - abstract_name_ind_offset)] *
                        REGION['数字']['hyper_col_sum'])

    return form_nerve.make_new_nerve_packs(mother_inds,
                                           father_inds,
                                           cortex_obj,
                                           reset_nerve_props_matrix=np.array(
                                               transmitter_release_sum,
                                               dtype=[('transmitter_release_sum',
                                                       'float')]))


def form_init_nerve():
    return [
        传递标志物给数字的树突棘,
    ]
