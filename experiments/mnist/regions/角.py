from consts.feature import VISUAL_FIELD_WH, RECEPTIVE_FIELD_LEVELS, ANGLE_NAMES
from consts.nerve_props import TYPE

region_info = {
    'region_name':
    '角',
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
                    'name': f'$_A步长{step_length}的激励',
                    'feature': {
                        'step_length': step_length,
                    },
                } for step_length in [3, 5]],
            ]
        } for angle_name in ANGLE_NAMES],
        *[{
            'name':
            f'{angle_name}的注意力竞争',
            'feature': {},
            'dendrites': [],
            'axons': []
        } for angle_name in ANGLE_NAMES],
        *[{
            'name':
            f'{angle_name}的注意力竞争结果',
            'feature': {},
            'dendrites': [],
            'axons': [
            ]
        } for angle_name in ANGLE_NAMES],
        {
            'name':
            '汇总角',
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
            '汇总角的注意力竞争结果',
            'feature': {},
            'dendrites': [
            ],
            'axons': [
                {
                    'name': f'$_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        },
    ],
}
