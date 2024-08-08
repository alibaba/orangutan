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
    'contour_center',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[
            {
                'name':
                f'{side}_contour_center',
                'feature': {},
                'dendrites': [
                    {
                        'name': '$_DAdd',
                        'feature': {
                            'transmitter_release_sum': 65 * 3.75
                        },
                    },
                ],
                'axons': [
                    *[{
                        'name': f'$_A_excitation_with_step_length_{step_length}',
                        'feature': {
                            'step_length': step_length,
                        },
                    } for step_length in [2, 4]],
                ]
            } for side in CONTOUR_SIDES
        ],
        *[{
            'name': f'attention_competition_of_{side}_contour_center',
            'feature': {},
            'dendrites': [],
            'axons': []
        } for side in CONTOUR_SIDES],
        *[{
            'name':
            f'attention_competition_result_of_{side}_contour_center',
            'feature': {},
            'dendrites': [],
            'axons': [
                {
                    'name': f'$_A_all_or_none_strong_inhibit',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 2,
                    },
                },
            ]
        } for side in CONTOUR_SIDES],
    ]
}