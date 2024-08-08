from consts.feature import VISUAL_FIELD_WH, RECEPTIVE_FIELD_LEVELS, ANGLE_NAMES
from consts.nerve_props import TYPE

region_info = {
    'region_name':
    'angle',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[{
            'name':
            angle_name,
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                },
            ],
            'axons': [
                *[{
                    'name': f'$_A_excitation_with_step_length_{step_length}',
                    'feature': {
                        'step_length': step_length,
                    },
                } for step_length in [3, 5]],
            ]
        } for angle_name in ANGLE_NAMES],
        *[{
            'name':
            f'attention_competition_of_{angle_name}',
            'feature': {},
            'dendrites': [],
            'axons': []
        } for angle_name in ANGLE_NAMES],
        *[{
            'name':
            f'attention_competition_result_of_{angle_name}',
            'feature': {},
            'dendrites': [],
            'axons': [
            ]
        } for angle_name in ANGLE_NAMES],
        {
            'name':
            'summary_angles',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
            'axons': []
        },
        {
            'name':
            'summarize_angle_attention_competition_results',
            'feature': {},
            'dendrites': [
            ],
            'axons': [
                {
                    'name': f'$_A_inhibit',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        },
    ],
}
