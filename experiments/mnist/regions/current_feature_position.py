from consts.feature import VISUAL_FIELD_WH
from consts.nerve_props import TYPE

region_info = [{
    'region_name':
    'current_feature_position',
    'region_shape': (1, 2, 1),
    'neurons': [
        *[{
            'name':
            f'{x_or_y}',
            'feature': {},
            'dendrites': [
                {
                    'name': f'{x_or_y}_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                },
            ],
            'axons': [
                {
                    'name': f'{x_or_y}_A_inhibit',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for x_or_y in range(VISUAL_FIELD_WH[0])],
    ],
}]
