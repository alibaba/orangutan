from pickle import TRUE
from consts.feature import ORIENTS, RECEPTIVE_FIELD_LEVELS, ANGLES, FEATURE_TYPES, COMMON_ABSTRACT_TYPES_MAP, SCALE_LEVEL_RATIOS
from ...util import get_soma_inds, get_popu_orients, get_popu_receptive_field_levels, get_popu_props
import numpy as np
from ...form_nerve.form_nerve import form_nerve
import math

axon_end_inds = {}


def make_record_single_ind_to_population_soma(same_value_mask):

    def record_single_ind_to_population_soma(cortex_obj, new_nerve_slice,
                                             mother_inds, father_inds):
        ''' 把群体编码对应的属性值相等的个体编码的胞体的ind记录到群体编码的胞体上，用于后续形成后验突触时的相关计算
        '''
        mother_inds = np.asarray(mother_inds)
        father_inds = np.asarray(father_inds)
        population_soma_inds = cortex_obj.cortex['soma_ind'][
            father_inds[same_value_mask]]
        cortex_obj.cortex['exinfo_1'][population_soma_inds] = mother_inds[
            same_value_mask]

    return record_single_ind_to_population_soma


def 生成群体编码(prop_type):

    def 群体编码(cortex_obj):
        mother_inds, father_inds, transmitter_release_sum = [], [], []
        same_value_mask = []
        prop_values = COMMON_ABSTRACT_TYPES_MAP[prop_type]['values']
        prop_names = COMMON_ABSTRACT_TYPES_MAP[prop_type]['names']
        for suffix in ['', '-泛化']:
            for prop_value in prop_values:
                popu_props = get_popu_props(prop_type, prop_value, {
                    '': 4,
                    '-泛化': 8
                }[suffix])
                for _, father_prop_value, axon_end_release_sum_ratio in popu_props:
                    for abstract_type in prop_names:
                        mother_inds.extend(
                            get_soma_inds(f'属性-{abstract_type}', [
                                f'{abstract_type}{prop_value}-个体编码',
                                f'{abstract_type}{prop_value}-个体编码出现',
                                f'{abstract_type}{prop_value}-个体编码持续',
                                f'{abstract_type}{prop_value}-个体编码消失',
                            ]))
                        father_inds.extend(
                            get_soma_inds(f'属性-{abstract_type}', [
                                f'{abstract_type}{father_prop_value}{suffix}-群体编码',
                                f'{abstract_type}{father_prop_value}{suffix}-群体编码出现_DMax',
                                f'{abstract_type}{father_prop_value}{suffix}-群体编码持续_DMax',
                                f'{abstract_type}{father_prop_value}{suffix}-群体编码消失_DMax',
                            ]))
                        transmitter_release_sum.extend(
                            [65 * axon_end_release_sum_ratio] * 4)
                        same_value_mask.extend(
                            [prop_value == father_prop_value] * 4)

        return form_nerve.make_new_nerve_packs(
            mother_inds,
            father_inds,
            cortex_obj,
            reset_nerve_props_lambda=make_record_single_ind_to_population_soma(
                same_value_mask),
            reset_nerve_props_matrix=np.array(transmitter_release_sum,
                                              dtype=[
                                                  ('transmitter_release_sum',
                                                   'float')
                                              ]))

    return 群体编码


def form_init_nerve():
    return [
        生成群体编码(prop_type) for prop_type in COMMON_ABSTRACT_TYPES_MAP.keys()
    ]