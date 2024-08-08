import itertools
from consts.feature import ORIENTS, RECEPTIVE_FIELD_LEVELS, ANGLES, VISUAL_FIELD_WH, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLE_NAMES, CONTOUR_CENTER_NAMES, CONTOUR_CENTER_ORIENTS, MIN_ANGLE, CROSS_NAMES, FEATURE_TYPES, CONTOUR_SIDES
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
import numpy as np
from ...form_nerve.form_nerve import form_nerve
from experiments import REGION

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 激励属性_类型(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type in FEATURE_TYPES:
        for feature_name in {
                '角': ANGLE_NAMES,
                # '叉': CROSS_NAMES,
                '轮廓中心': CONTOUR_CENTER_NAMES,
        }[feature_type]:
            mother_inds.extend(
                get_soma_inds(feature_type, f'{feature_name}-注意力竞争结果出现'))
            father_inds.extend(
                np.tile(
                    get_soma_inds(
                        f'属性-类型',
                        f'类型{feature_type}-个体编码_DAdd',
                    ), REGION[feature_type]['hyper_col_sum']))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励属性_朝向_角(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for feature_type in ['角', '叉']:
        for orient in ORIENTS:
            for angle in ANGLES:
                corner_orient = ((orient +
                                  (orient + angle)) / 2) % 360 or 360.0
                # 和目标朝向的差值小于最小角度的，都是潜在的朝向
                sparse_orients = ORIENTS[np.abs(ORIENTS -
                                                corner_orient) < MIN_ANGLE]
                # 取潜在朝向中夹角最小的那个朝向作为最终朝向
                sparse_orient = sparse_orients[np.argmin(sparse_orients)]

                this_mother_inds = get_soma_inds(
                    feature_type,
                    f'方位{orient}和{(orient+angle)%360 or 360.0}的{feature_type}-注意力竞争结果出现'
                )
                mother_inds.extend(this_mother_inds)
                father_inds.extend(
                    np.tile(
                        get_soma_inds(
                            f'属性-朝向',
                            f'朝向{sparse_orient}-个体编码_DAdd',
                        ), REGION[feature_type]['hyper_col_sum']))
                reset_nerve_props_matrix.extend([65] * this_mother_inds.size)
    return make_new_nerve_packs(mother_inds,
                                father_inds,
                                cortex_obj,
                                reset_nerve_props_matrix=np.array(
                                    reset_nerve_props_matrix,
                                    dtype=[('transmitter_release_sum', 'float')
                                           ]))


def 激励属性_朝向_轮廓中心(cortex_obj):
    mother_inds, father_inds = [], []
    side = '内'
    for contour_orient in CONTOUR_CENTER_ORIENTS:
        mother_inds.extend(
            get_soma_inds('轮廓中心', f'朝向{contour_orient}的{side}轮廓中心-注意力竞争结果出现'))
        father_inds.extend(
            np.tile(get_soma_inds(
                f'属性-朝向',
                f'朝向{contour_orient}-个体编码_DAdd',
            ), REGION['轮廓中心']['hyper_col_sum']))
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励属性_朝向'))


def 激励属性_角度_角(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type in ['角', '叉']:
        for orient in ORIENTS:
            for angle in ANGLES:
                this_mother_inds = get_soma_inds(
                    feature_type,
                    f'方位{orient}和{(orient+angle)%360 or 360.0}的{feature_type}-注意力竞争结果出现'
                )
                mother_inds.extend(this_mother_inds)
                father_inds.extend(
                    np.tile(get_soma_inds(
                        f'属性-角度',
                        f'角度{angle}-个体编码_DAdd',
                    ), this_mother_inds.size))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励属性_角度_轮廓中心(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds('轮廓中心', f'朝向{orient}的内轮廓中心的开口角度{angle}'))
            father_inds.extend(
                np.tile(get_soma_inds(
                    f'属性-角度',
                    f'角度{angle}-个体编码_DAdd',
                ), REGION['轮廓中心']['hyper_col_sum']))
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励属性_朝向'))


def 激励属性_尺度_角(cortex_obj):
    mother_inds, father_inds = [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        mother_inds.extend(get_soma_inds('角', f'尺度{receptive_field_level}'))
        father_inds.extend(
            np.tile(
                get_soma_inds(f'属性-尺度', f'尺度{receptive_field_level}-个体编码'),
                #   f'尺度{receptive_field_level}-个体编码'),
                REGION['角']['hyper_col_sum']))
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '激励属性_尺度_角'))


def 禁止激励属性_尺度_角(cortex_obj):
    mother_inds, father_inds = [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        mother_inds.extend(get_soma_inds('角',
                                         f'尺度{receptive_field_level}_A抑制'))
    father_inds = axon_end_inds['激励属性_尺度_角']
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, '禁止激励属性_尺度_角'))


def 解禁激励属性_尺度_角(cortex_obj):
    mother_inds, father_inds = [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        mother_inds.extend(get_soma_inds('角', f'汇总角的注意力竞争结果_A抑制'))
    father_inds = axon_end_inds['禁止激励属性_尺度_角']
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


# def 约束激励属性_尺度_角(cortex_obj):
#     mother_inds, father_inds = [], []
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#         for angle_name in ANGLE_NAMES:
#             mother_inds.extend(get_soma_inds('角', f'汇总角的注意力竞争结果'))
#             father_inds.extend(
#                 np.tile(
#                     get_soma_inds(f'属性-尺度',
#                                   f'尺度{receptive_field_level}-个体编码_DMin'),
#                     REGION['角']['hyper_col_sum']))
#     return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励属性_尺度_轮廓中心(cortex_obj):
    mother_inds, father_inds = [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        mother_inds.extend(get_soma_inds('轮廓中心', f'尺度{receptive_field_level}'))
        father_inds.extend(
            np.tile(
                get_soma_inds(f'属性-尺度',
                              f'尺度{receptive_field_level}-个体编码_DMin'),
                REGION['轮廓中心']['hyper_col_sum']))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励属性_尺度_注意力竞争结果(cortex_obj):
    LOOP_PROPS = [(feature_type, feature_name)
                  for feature_type in ['角', '轮廓中心'] for feature_name in {
                      '角': ANGLE_NAMES,
                      '轮廓中心': [f'{side}轮廓中心' for side in CONTOUR_SIDES],
                  }[feature_type]]
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            mother_inds.extend(
                get_soma_inds(
                    feature_type,
                    f'{feature_name}的注意力竞争结果',
                ))
            father_inds.extend(
                np.tile(
                    get_soma_inds(f'属性-尺度',
                                  f'尺度{receptive_field_level}-个体编码_DMin'),
                    REGION[feature_type]['hyper_col_sum']))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 限制所有抽象个体编码兴奋(cortex_obj):
    mother_inds, father_inds = [], []
    father_inds = list(
        itertools.chain(*[
            get_soma_inds(f'属性-{abstract_type}',
                          f'{abstract_name}-个体编码_DAdd限制最大值')
            for abstract_type, abstract_values in
            COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
            for abstract_name, _ in abstract_values
        ]))
    mother_inds = np.tile(get_soma_inds('全局调控', '公用调控兴奋_A限制抽象个体编码最大兴奋'),
                          len(father_inds))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # 激励属性_类型,
        # 激励属性_朝向_角,
        # 激励属性_朝向_轮廓中心,
        # 激励属性_角度_角,
        # 激励属性_角度_轮廓中心,
        激励属性_尺度_角,
        禁止激励属性_尺度_角,
        解禁激励属性_尺度_角,
        # 约束激励属性_尺度_角,
        激励属性_尺度_轮廓中心,
        激励属性_尺度_注意力竞争结果,
        # 限制所有抽象个体编码兴奋,
    ]
