from consts.feature import VISUAL_FIELD_WH, ORIENT_SUM, ORIENTS, CONTOUR_SIDES, ORIENT_SIDES, BOTH_SIDE_ORIENT_DESC
from consts.nerve_props import TYPE

region_info = {
    'region_name':
    '方位汇总',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[{
            'name':
            f'汇总{orient}方向的{side}轮廓方位',
            'feature': {
                'exinfo_0': orient,
            },
            'dendrites': [
                {
                    'name': f'汇总{orient}方向的{side}轮廓方位_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
            'axons': []
        } for orient in ORIENTS for side in CONTOUR_SIDES],
        *[{
            'name':
            f'汇总{orient}方向的{orient_side}侧方位',
            'feature': {
                'exinfo_0': orient,
            },
            'dendrites': [
                {
                    'name': f'汇总{orient}方向的{orient_side}侧方位_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
            'axons': []
        } for orient in ORIENTS for orient_side in ORIENT_SIDES],
        *[{
            'name':
            f'汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向上的两端方位',
            'feature': {},
            'dendrites': [
                {
                    'name':
                    f'汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向上的两端方位_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                        'transmitter_release_sum': 65 * 2,
                    },
                    'dendrites': [],
                },
            ],
            'axons': []
        } for orient_ind in range(ORIENT_SUM // 2)],
    ],
}
