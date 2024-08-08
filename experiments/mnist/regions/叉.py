from consts.feature import VISUAL_FIELD_WH, RECEPTIVE_FIELD_LEVELS, ORIENTS, ANGLES, ORIENT_SIDES
from consts.nerve_props import TYPE
import numpy as np
from util import is_can_init_orient_mask_map


region_info = {
    'region_name':
    '叉',
    'region_shape': (*VISUAL_FIELD_WH, 1),
    'neurons': [
        # *[{
        #     'name':
        #     f'方位{orient}和{(orient+angle)%360 or 360.0}的叉',
        #     'feature': {
        #         'exinfo_0': float(f'{int(orient)}.{int(orient+angle)}'),
        #     },
        #     'dendrites': [
        #         {
        #             'name': f'$_DMin',
        #             'feature': {
        #                 'transmitter_release_sum': 65 * 2,
        #                 'type': TYPE['dendrite_min'],
        #             },
        #         },
        #     ],
        #     'axons': []
        # } for orient in ORIENTS for angle in ANGLES],
        # # 注意力竞争
        # *[{
        #     'name':
        #     f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争',
        #     'feature': {
        #         'exinfo_0': float(f'{int(orient)}.{int(orient+angle)}')
        #     },
        #     'dendrites': [
        #         {
        #             'name':
        #             f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争_DAdd',
        #             'feature': {},
        #         },
        #     ],
        #     'axons': [
        #         {
        #             'name':
        #             f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争_A激励属性',
        #             'feature': {
        #                 'step_length': 3,
        #             },
        #         },
        #     ]
        # } for orient in ORIENTS for angle in ANGLES],
        *[
            {
                'name':
                f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果出现',
                'feature': {
                    'exinfo_0': float(f'{int(orient)}.{int(orient+angle)}')
                },
                'dendrites': [
                    # {
                    #     'name':
                    #     f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果出现_DMin',
                    #     'feature': {
                    #         'type': TYPE['dendrite_min'],
                    #     },
                    # },
                ],
                'axons': [
                    # {
                    #     'name':
                    #     f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果出现_A抑制',
                    #     'feature': {
                    #         'post_sign': -1,
                    #     },
                    # },
                    # {
                    #     'name':
                    #     f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果出现_A全或无禁止反馈激励射线',
                    #     'feature': {
                    #         'post_sign': -1,
                    #         'all_or_none': 2,
                    #     },
                    # },
                ]
            } for orient in ORIENTS for angle in ANGLES
        ],
        # *[{
        #     'name':
        #     f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果持续',
        #     'feature': {
        #         'self_synapse': 1,
        #         'exinfo_0': float(f'{int(orient)}.{int(orient+angle)}')
        #     },
        #     'dendrites': [
        #         {
        #             'name':
        #             f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果持续_DAdd',
        #             'feature': {},
        #         },
        #     ],
        #     'axons': [
        #         {
        #             'name':
        #             f'方位{orient}和{(orient+angle)%360 or 360.0}的叉-注意力竞争结果持续_A抑制',
        #             'feature': {
        #                 'post_sign': -1,
        #             },
        #         },
        #     ]
        # } for orient in ORIENTS for angle in ANGLES],
        *[{
            'name': f'尺度{receptive_field_level}',
            'feature': {},
            'dendrites': [],
            'axons': []
        } for receptive_field_level in RECEPTIVE_FIELD_LEVELS],
        # {
        #     'name':
        #     f'最大尺度',
        #     'feature': {},
        #     'dendrites': [
        #         {
        #             'name': f'最大尺度_DMax',
        #             'feature': {},
        #             'dendrites': []
        #         },
        #     ],
        #     'axons': [
        #         {
        #             'name': f'最大尺度_A全或无弱抑制',
        #             'feature': {
        #                 'post_sign': -1,
        #                 'all_or_none': 1,
        #             },
        #         },
        #     ]
        # },
    ],
}
