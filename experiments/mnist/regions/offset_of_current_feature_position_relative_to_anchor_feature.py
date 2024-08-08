from consts.feature import VISUAL_FIELD_WH

region_info = [{
    'region_name':
    'offset_of_current_feature_position_relative_to_anchor_feature',
    'region_shape': (1, 2, 1),
    'neurons': [
        *[
            {
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
                ],
            } for x_or_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1)
        ],
    ],
}]
