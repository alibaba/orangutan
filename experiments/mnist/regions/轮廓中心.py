from consts.feature import RECEPTIVE_FIELD_LEVELS, VISUAL_FIELD_WH, CONTOUR_SIDES, CONTOUR_SIDES
from util import is_can_init_orient_mask_map


def get_neuron_in_pic_mask(receptive_field_level):
    return is_can_init_orient_mask_map[
        (90.0, receptive_field_level)] * is_can_init_orient_mask_map[
            (180.0, receptive_field_level)] * is_can_init_orient_mask_map[
                (270.0, receptive_field_level)] * is_can_init_orient_mask_map[
                    (360.0, receptive_field_level)]


neuron_in_pic_mask_map = {
    receptive_field_level: get_neuron_in_pic_mask(receptive_field_level)
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS
}

region_info = {
    'region_name':
    '轮廓中心',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[
            {
                'name':
                f'{side}轮廓中心',
                'feature': {},
                'dendrites': [
                    {
                        'name': '$_DAdd',
                        'feature': {
                            # 整体扩大所有轮廓中心的感知兴奋，使得轮廓中心兴奋水平和角的兴奋水平对齐
                            'transmitter_release_sum': 65 * 3.75
                        },
                    },
                ],
                'axons': [
                    *[{
                        'name': f'$_A步长{step_length}的激励',
                        'feature': {
                            'step_length': step_length,
                        },
                    } for step_length in [2, 4]],
                ]
            } for side in CONTOUR_SIDES
        ],
        *[{
            'name': f'{side}轮廓中心的注意力竞争',
            'feature': {},
            'dendrites': [],
            'axons': []
        } for side in CONTOUR_SIDES],
        *[{
            'name':
            f'{side}轮廓中心的注意力竞争结果',
            'feature': {},
            'dendrites': [],
            'axons': [
                {
                    'name': f'$_A全或无强抑制',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 2,
                    },
                },
            ]
        } for side in CONTOUR_SIDES],
        # *[{
        #     'name': f'尺度{receptive_field_level}',
        #     'feature': {},
        #     'dendrites': [],
        #     'axons': []
        # } for receptive_field_level in RECEPTIVE_FIELD_LEVELS]
    ]
}