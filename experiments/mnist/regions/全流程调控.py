from consts.feature import VISUAL_FIELD_WH, RECEPTIVE_FIELD_LEVELS, ORIENTS, ORIENT_SUM
from consts.nerve_props import TYPE, RELEASE_TYPE

region_info = {
    'region_name':
    '全流程调控',
    'region_shape': (1, 1, 1),
    'neurons': [
        {
            'name': '信号输入',
            'feature': {
                'excite': 89960,
                'self_synapse': 2,
            },
        },
        {
            'name': '计算相邻点差值',
            'feature': {},
        },
        {
            'name': '激励边缘点',
            'feature': {},
        },
        {
            'name': '激励轮廓方位',
            'feature': {},
        },
        *[
            {
                'name': '激励轮廓直线',
                'feature': {},
            },
            {
                'name': '激励射线',
                'feature': {},
            },
        ],
        *[
            {
                'name': '汇总轮廓直线',
                'feature': {},
            },
            {
                'name': '汇总射线',
                'feature': {},
            },
        ],
        *[
            {
                'name': '激励轮廓中心',
                'feature': {},
            },
            {
                'name': '激励角',
                'feature': {},
            },
        ],
        {
            'name': '激励数字',
            'feature': {},
        },
        *[
            {
                'name': '反馈预测角',
                'feature': {},
            },
            {
                'name': '反馈预测轮廓中心',
                'feature': {},
            },
        ],
        {
            'name': '计算预测偏差或意外',
            'feature': {},
        },
        {
            'name': '建立或调整预测回路',
            'feature': {},
        },
        {
            'name':
            '反馈激励轮廓直线',
            'feature': {},
            'dendrites': [
                {
                    'name': '反馈激励轮廓直线_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
        },
        {
            'name': '反馈激励轮廓方位',
            'feature': {},
        },
        {
            'name': '反馈激励边缘点',
            'feature': {},
        },
        {
            'name': '激励像素独占轮廓方位',
            'feature': {},
        },
        {
            'name': '激励像素独占轮廓直线',
            'feature': {},
        },
        {
            'name': '汇总像素独占轮廓直线',
            'feature': {},
        },
        {
            'name':
            '激励像素独占轮廓中心',
            'feature': {},
            'axons': [
                {
                    'name': '激励像素独占轮廓中心_A易化激励像素独占轮廓中心',
                    'feature': {
                        'transmitter_release_sum': .01,
                        'release_type': RELEASE_TYPE['Fa'],
                    },
                },
                {
                    'name': '激励像素独占轮廓中心_A解禁激励像素独占轮廓中心',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        },
    ],
}
