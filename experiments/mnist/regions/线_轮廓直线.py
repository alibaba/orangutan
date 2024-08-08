from consts.feature import VISUAL_FIELD_WH, RECEPTIVE_FIELD_LEVELS, ORIENTS, ORIENT_SUM, BOTH_SIDE_ORIENT_DESC, ORIENT_CONTOUR_SIDES
from consts.nerve_props import TYPE
from util import is_can_init_orient_mask_map


def get_neuron_in_pic_mask(orient_ind, receptive_field_level):
    # TODO 此处需要计算所有方向上是否都在图片范围内，这个轮廓才算在图片内
    return is_can_init_orient_mask_map[
        (ORIENTS[orient_ind],
         receptive_field_level)] * is_can_init_orient_mask_map[
             (ORIENTS[(orient_ind + ORIENT_SUM // 2) % ORIENT_SUM],
              receptive_field_level)]


region_info = [{
    'region_name':
    f'线_轮廓直线',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[{
            'name':
            f'汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                    'dendrites': [],
                },
            ],
            'axons': [
                {
                    'name': f'$_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                    'dendrites': [],
                },
            ],
            'axons': [
                {
                    'name': f'$_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞_反馈',
            'feature': {},
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    }
                },
            ],
            'axons': [
                {
                    'name': f'$_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
                {
                    'name': f'$_A全或无强抑制',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 2,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
    ],
}, *[{
    'region_name':
    f'线_轮廓直线-S{receptive_field_level}',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        *[{
            'name':
            f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线',
            'feature': {},
            'neuron_in_pic_mask':
            get_neuron_in_pic_mask(orient_ind, receptive_field_level),
            'dendrites': [
                {
                    'name':
                    f'$_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                    'dendrites': [
                        {
                            'name': f'$_DMax{ORIENTS[orient_ind]}方向',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                        {
                            'name':
                            f'$_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                    ],
                },
            ],
            'axons': []
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞',
            'feature': {},
            'neuron_in_pic_mask':
            get_neuron_in_pic_mask(orient_ind, receptive_field_level),
            'dendrites': [
                {
                    'name':
                    f'$_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                    'dendrites': [
                        {
                            'name': f'$_DMax{ORIENTS[orient_ind]}方向',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                        {
                            'name':
                            f'$_DMax{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向',
                            'feature': {
                                'type': TYPE['dendrite_max'],
                            },
                        },
                    ],
                },
            ],
            'axons': [
                {
                    'name': f'$_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ]
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
        *[{
            'name':
            f'{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向_{side}轮廓直线_复杂细胞_反馈',
            'feature': {},
            'neuron_in_pic_mask':
            get_neuron_in_pic_mask(orient_ind, receptive_field_level),
            'dendrites': [
                {
                    'name': f'$_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                    },
                },
            ],
            'axons': []
        } for side in ORIENT_CONTOUR_SIDES
          for orient_ind in range(ORIENT_SUM // 2)],
    ],
} for receptive_field_level in RECEPTIVE_FIELD_LEVELS]]
