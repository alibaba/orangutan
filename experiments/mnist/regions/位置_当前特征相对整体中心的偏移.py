from consts.feature import VISUAL_FIELD_WH

region_info = [{
    'region_name':
    '位置_当前特征相对整体中心的偏移',
    'region_shape': (1, 2, 1),
    'neurons': [
        *[
            {
                'name':
                f'{x_or_y}',
                'feature': {},
                'axons': [
                    {
                        'name': f'{x_or_y}_A抑制',
                        'feature': {
                            'post_sign': -1,
                        },
                    },
                ],
            } for x_or_y in range(-VISUAL_FIELD_WH[0], VISUAL_FIELD_WH[0] + 1)
        ],
    ],
}]
