from consts.feature import VISUAL_FIELD_WH

region_info = [{
    'region_name':
    '位置_锚点特征',
    'region_shape': (1, 2, 1),
    'neurons': [
        *[{
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
            ]
        } for x_or_y in range(VISUAL_FIELD_WH[0])],
    ],
}]
