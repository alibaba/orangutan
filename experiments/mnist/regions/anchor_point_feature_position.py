from consts.feature import VISUAL_FIELD_WH

region_info = [{
    'region_name':
    'anchor_point_feature_position',
    'region_shape': (1, 2, 1),
    'neurons': [
        *[{
            'name':
            f'{x_or_y}',
            'feature': {},
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
