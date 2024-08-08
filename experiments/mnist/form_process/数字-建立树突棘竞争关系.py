from cmath import inf
from ...util import REGION, get_soma_inds
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from consts.nerve_params import SPINE_SENSITIVE_ABSTRACT_TYPES_LIST, SPINE_SENSITIVE_ABSTRACT_COMBINATIONS_LIST, SPINE_SENSITIVE_ABSTRACT_NAME_SUM, SPINE_IND_MAPS
from consts.nerve_props import TYPE
from consts.feature import COMMON_ABSTRACT_TYPE_NAME_MAP, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES

axon_end_inds = {}


def 建立树突棘竞争关系(cortex_obj):
    mother_inds, father_inds, transmitter_release_sum = [], [], []
    MAX_SINGLE_DISTANCE = 1

    def get_abstract_value_with_peak_abstract_ind(abstract_type,
                                                  peak_abstract_ind):
        abstract_meta = COMMON_ABSTRACT_TYPE_NAME_MAP[abstract_type]
        abstract_name_inds = np.arange(len(abstract_meta['values']))
        close_abstract_name_inds = [
            abstract_name_ind for abstract_name_ind in abstract_name_inds
            if abs(abstract_name_ind - peak_abstract_ind) < 1
        ]
        abstract_values = [
            abstract_meta['values'][abstract_ind]
            for abstract_ind in close_abstract_name_inds
        ]
        # 如果value是无，则和索引最接近的只能有一个索引
        assert '无' not in abstract_values or len(abstract_values) == 1
        abstract_value = abstract_values[0] if len(abstract_values) == 1 else (
            abstract_values[0] *
            abs(close_abstract_name_inds[0] - peak_abstract_ind) +
            abstract_values[1] *
            abs(close_abstract_name_inds[1] - peak_abstract_ind))
        return abstract_value

    for spine_sensitive_abstract_combinations, spine_sensitive_abstract_types, spine_ind_map in zip(
            SPINE_SENSITIVE_ABSTRACT_COMBINATIONS_LIST,
            SPINE_SENSITIVE_ABSTRACT_TYPES_LIST,
            SPINE_IND_MAPS,
    ):
        for father_spine_sensitive_abstract_combination in spine_sensitive_abstract_combinations:
            father_spine_ind = spine_ind_map[
                father_spine_sensitive_abstract_combination]
            father_spine_sensitive_abstract_combination = np.asarray(
                father_spine_sensitive_abstract_combination)
            mother_spine_inds = []
            father_spine_inds = []
            axon_end_release_sums = []
            for mother_spine_sensitive_abstract_combination in spine_sensitive_abstract_combinations:
                mother_spine_ind = spine_ind_map[
                    mother_spine_sensitive_abstract_combination]
                mother_spine_sensitive_abstract_combination = np.asarray(
                    mother_spine_sensitive_abstract_combination)
                distance_vector = np.full(len(spine_sensitive_abstract_types),
                                          np.inf)
                for abstract_type_ind, (
                        abstract_type, father_peak_abstract_ind,
                        mother_peak_abstract_ind) in enumerate(
                            zip(spine_sensitive_abstract_types,
                                father_spine_sensitive_abstract_combination,
                                mother_spine_sensitive_abstract_combination)):
                    abstract_meta = COMMON_ABSTRACT_TYPE_NAME_MAP[
                        abstract_type]
                    father_abstract_value = get_abstract_value_with_peak_abstract_ind(
                        abstract_type, father_peak_abstract_ind)
                    mother_abstract_value = get_abstract_value_with_peak_abstract_ind(
                        abstract_type, mother_peak_abstract_ind)
                    if father_abstract_value != '无' and mother_abstract_value != '无':
                        if abstract_meta['value_recyclable'] != False:
                            abstract_distance = min(
                                abs(father_abstract_value -
                                    mother_abstract_value),
                                abs(abstract_meta['value_recyclable'] -
                                    father_abstract_value) +
                                abs(abstract_meta['value_recyclable'] -
                                    mother_abstract_value),
                            )
                        else:
                            abstract_distance = abs(father_abstract_value -
                                                    mother_abstract_value)
                    elif father_abstract_value == '无' and mother_abstract_value == '无':
                        abstract_distance = 0
                    else:
                        abstract_distance = inf

                    distance_vector[
                        abstract_type_ind] = abstract_distance / abstract_meta[
                            'value_internal'] / (
                                len(abstract_meta['values']) /
                                SPINE_SENSITIVE_ABSTRACT_NAME_SUM)

                spine_distance = np.linalg.norm(distance_vector) or inf
                # if (distance_vector > MAX_SINGLE_DISTANCE).any() or spine_distance == 0:
                # if spine_distance == 0:
                # or (1 / spine_distance) < .4:
                # continue

                # mother_inds.extend(
                #     get_soma_inds('数字',  
                #                   f'前馈预测_DMax_棘{mother_spine_ind}'))
                mother_spine_inds.extend(
                    get_soma_inds('数字',  
                                  f'前馈预测_DMax_棘{mother_spine_ind}'))
                father_spine_inds.extend(
                    get_soma_inds('数字',  
                                  f'前馈预测_DMax_棘{father_spine_ind}'))
                axon_end_release_sums.extend([1 / spine_distance] *
                                             REGION['数字']['hyper_col_sum'])

            axon_end_release_sums = np.asarray(axon_end_release_sums)
            mother_spine_inds = np.asarray(mother_spine_inds)
            father_spine_inds = np.asarray(father_spine_inds)
            axon_end_release_sums *= min(1,
                                         1 / (max(axon_end_release_sums) or 1))
            able_axon_end_release_sums_on_father_mask = np.asarray(
                axon_end_release_sums) > .4
            mother_inds.extend(
                mother_spine_inds[able_axon_end_release_sums_on_father_mask])
            father_inds.extend(
                father_spine_inds[able_axon_end_release_sums_on_father_mask])
            transmitter_release_sum.extend(
                np.asarray(axon_end_release_sums)
                [able_axon_end_release_sums_on_father_mask])

    def reset_nerve_props_lambda(cortex_obj, new_nerve_slice, mother_inds,
                                 father_inds):
        cortex_obj.cortex['transmitter_release_sum'][
            new_nerve_slice] = transmitter_release_sum
        # max_axon_end_release_sum_on_spine = cortex_obj.cortex['float_util']
        # max_axon_end_release_sum_on_spine[:] = 0
        # np.maximum.at(
        #     max_axon_end_release_sum_on_spine,
        #     cortex_obj.cortex['post_ind'][new_nerve_slice],
        #     cortex_obj.cortex['transmitter_release_sum'][new_nerve_slice],
        # )
        # cortex_obj.cortex['transmitter_release_sum'][
        #     new_nerve_slice] *= np.minimum(
        #         1, 1 / max_axon_end_release_sum_on_spine[
        #             cortex_obj.cortex['post_ind'][new_nerve_slice]])

        # max_axon_end_release_sum = max(transmitter_release_sum)
        # cortex_obj.cortex['transmitter_release_sum'][
        #     new_nerve_slice] = np.asarray(transmitter_release_sum) * min(
        #         1, 1 / max_axon_end_release_sum)
        cortex_obj.cortex['type'][new_nerve_slice] = TYPE['spine_connect']

    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_lambda=reset_nerve_props_lambda)


def form_init_nerve():
    return [
        建立树突棘竞争关系,
    ]
