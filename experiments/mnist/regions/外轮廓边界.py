from consts.feature import ORIENTS, RECEPTIVE_FIELD_LEVELS
from consts.nerve_props import TYPE, RELEASE_TYPE

region_info = [{
    'region_name':
    '外轮廓边界',
    'region_shape': (1, 1, 1),
    'neurons': [
        *[{
            'name':
            f'{orient}方位{receptive_field_level}尺度的外轮廓边界',
            'feature': {},
            'dendrites': [
                {
                    'name': f'{orient}方位{receptive_field_level}尺度的外轮廓边界_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
            'axons': [
                {
                    'name':
                    f'{orient}方位{receptive_field_level}尺度的外轮廓边界_A解禁激励相对特征',
                    'feature': {
                        'post_sign': -1,
                    },
                },
                {
                    'name':
                    f'{orient}方位{receptive_field_level}尺度的外轮廓边界_A禁止解禁激励相对特征',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for orient in ORIENTS
          for receptive_field_level in RECEPTIVE_FIELD_LEVELS],
    ],
}]
