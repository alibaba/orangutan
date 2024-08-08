from consts.feature import COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 激励属性出现(cortex_obj):
    mother_inds, father_inds = [], []
    for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items(
    ):
        for abstract_name, _ in abstract_values:
            mother_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              [f'{abstract_name}-个体编码_A激励出现和持续'] * 2))
            father_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              f'{abstract_name}-个体编码出现_DMin'))
            father_inds.extend(
                get_soma_inds(f'属性-{abstract_type}', f'个体编码出现汇总_DMax'))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励属性持续(cortex_obj):
    mother_inds, father_inds = [], []
    for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items(
    ):
        for abstract_name, _ in abstract_values:
            mother_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              f'{abstract_name}-个体编码_A激励出现和持续'))
            father_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              f'{abstract_name}-个体编码持续_DMin'))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 全局调控限制激励属性出现和持续的时机(cortex_obj):
    mother_inds, father_inds = [], []
    for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items(
    ):
        for abstract_name, _ in abstract_values:
            mother_inds.extend(get_soma_inds('全局调控', ['公用调控兴奋_A限制属性出现时机'] * 2))
            father_inds.extend(
                get_soma_inds(f'属性-{abstract_type}', [
                    f'{abstract_name}-个体编码出现_DMin',
                    f'{abstract_name}-个体编码持续_DMin',
                ]))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励属性消失(cortex_obj):
    mother_inds, father_inds = [], []
    for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items(
    ):
        for abstract_name, _ in abstract_values:
            mother_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              [f'{abstract_name}-个体编码持续'] * 2))
            father_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              f'{abstract_name}-个体编码消失'))
            father_inds.extend(
                get_soma_inds(f'属性-{abstract_type}', f'个体编码消失汇总_DMax'))
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励属性消失'))


def 禁止激励属性消失(cortex_obj):
    mother_inds = []
    for abstract_type, abstract_values in COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items(
    ):
        for abstract_name, _ in abstract_values:
            mother_inds.extend(
                get_soma_inds(f'属性-{abstract_type}',
                              [f'{abstract_name}-个体编码_A禁止激励消失'] * 2))
    father_inds = axon_end_inds['激励属性消失']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励属性出现,
        激励属性持续,
        # 全局调控限制激励属性出现和持续的时机,
        激励属性消失,
        禁止激励属性消失,
    ]