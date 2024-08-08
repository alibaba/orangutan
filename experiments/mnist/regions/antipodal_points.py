from consts.feature import VISUAL_FIELD_WH, RECEPTIVE_FIELD_LEVELS, ORIENTS, ORIENT_SUM, BOTH_SIDE_ORIENT_DESC, ORIENT_CONTOUR_SIDES
from consts.nerve_props import TYPE
from util import is_can_init_orient_mask_map


def get_neuron_in_pic_mask(orient_ind, receptive_field_level):
    return is_can_init_orient_mask_map[
        (ORIENTS[orient_ind],
         receptive_field_level)] * is_can_init_orient_mask_map[
             (ORIENTS[(orient_ind + ORIENT_SUM // 2) % ORIENT_SUM],
              receptive_field_level)]


region_info = [{
    'region_name':
    f'antipodal_points',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[{
            'name':
            f'summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                    'dendrites': [],
                },
            ],
            'axons': [
                {
                    'name': f'$_A_inhibit',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                    'dendrites': [],
                },
            ],
            'axons': [
                {
                    'name': f'$_A_inhibit',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'summary_{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell_feedback',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    }
                },
            ],
            'axons': [
                {
                    'name': f'$_A_inhibit',
                    'feature': {
                        'post_sign': -1,
                    },
                },
                {
                    'name': f'$_A_all_or_none_strong_inhibit',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 2,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
    ],
}, *[{
    'region_name':
    f'antipodal_points-S{receptive_field_level}',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[{
            'name':
            f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line',
            'feature': {},
            'neuron_in_pic_mask':
            get_neuron_in_pic_mask(orient_ind, receptive_field_level),
            'dendrites': [
                {
                    'name':
                    f'$_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                    'dendrites': [
                        {
                            'name': f'$_DMax{ORIENTS[orient_ind]}_direction',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                        {
                            'name':
                            f'$_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}_direction',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                    ],
                },
            ],
            'axons': []
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell',
            'feature': {},
            'neuron_in_pic_mask':
            get_neuron_in_pic_mask(orient_ind, receptive_field_level),
            'dendrites': [
                {
                    'name':
                    f'$_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                    'dendrites': [
                        {
                            'name': f'$_DMax{ORIENTS[orient_ind]}_direction',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                        {
                            'name':
                            f'$_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}_direction',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                    ],
                },
            ],
            'axons': [
                {
                    'name': f'$_A_inhibit',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}_direction_{side}_contour_straight_line_complex_cell_feedback',
            'feature': {},
            'neuron_in_pic_mask':
            get_neuron_in_pic_mask(orient_ind, receptive_field_level),
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
            'axons': []
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
    ],
} for receptive_field_level in RECEPTIVE_FIELD_LEVELS]]
