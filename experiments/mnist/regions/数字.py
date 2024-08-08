from consts.nerve_props import TYPE, RELEASE_TYPE
from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE
# , SPINE_SENSITIVE_ABSTRACT_COMBINATIONS_LIST, SPINE_SENSITIVE_ABSTRACT_TYPES_LIST
import itertools

# spine_sensitive_abstract_types_list = []
# for spine_sensitive_abstract_types, spine_sensitive_abstract_combinations in zip(
#         SPINE_SENSITIVE_ABSTRACT_TYPES_LIST,
#         SPINE_SENSITIVE_ABSTRACT_COMBINATIONS_LIST):
#     spine_sensitive_abstract_types_list.extend(
#         [spine_sensitive_abstract_types] *
#         len(spine_sensitive_abstract_combinations))

region_info = {
    'region_name':
    '数字',
    'region_shape': (1, 10, 1),
    'neurons': [
        {
            'name':
            'input',
            'feature': {},
            'axons': [
                {
                    'name': 'input_A激励前馈预测意外',
                    'feature': {
                        'step_length': 5,
                    },
                },
                {
                    'name': 'input_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
                {
                    'name': 'input_A转运标记物',
                    'feature': {
                        'release_type': RELEASE_TYPE['marker'],
                        'transmitter_release_sum': 10,
                    },
                },
                {
                    'name': 'input_易化属性互相预测',
                    'feature': {
                        'release_type': RELEASE_TYPE['Fa'],
                        'RP': -65 * 65,
                    },
                },
            ]
        },
        {
            'name':
            'input-出现',
            'feature': {},
            'axons': [
                {
                    'name': 'input-出现_A转运标记物',
                    'feature': {
                        'release_type': RELEASE_TYPE['marker'],
                        'transmitter_release_sum': 1,
                    },
                },
            ]
        },
        {
            'name':
            'input-持续',
            'feature': {},
            'axons': [
                {
                    'name': 'input-持续_A禁止激励数字出现',
                    'feature': {
                        'post_sign': -1,
                    },
                },
                {
                    'name': 'input-持续_A易化激励属性',
                    'feature': {
                        'release_type': RELEASE_TYPE['Fa'],
                    },
                },
            ]
        },
        {
            'name': 'input-消失',
            'feature': {},
            'axons': []
        },
        {
            'name':
            '前馈预测',
            'feature': {
                'RP': -.1,
                'transmitter_release_sum': .1,
            },
            'dendrites': [
                # {
                #     'name':
                #     '前馈预测_DAdd',
                #     'feature': {
                #         'RP': -.1,
                #         'transmitter_release_sum': .1,
                #     },
                #     'dendrites': [
                #     ],
                # },
                {
                    'name':
                    '前馈预测_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                        'RP': -.1,
                        'transmitter_release_sum': .1,
                        'self_synapse': 1,
                    },
                    'dendrites': [{
                        'name': f'前馈预测_DMax_棘{i}',
                        'feature': {
                            'type': TYPE['dendrite_max'],
                            'RP': -.1,
                            'transmitter_release_sum': .1,
                        }
                    } for i in range(SPINE_SUM_ON_A_DENDRITE)],
                },
            ],
            'axons': [
                {
                    'name': '前馈预测_A激励累积前馈预测',
                    'feature': {},
                },
                {
                    'name': '前馈预测_A禁止前馈抑制',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 1,
                    },
                },
            ],
        },
        {
            'name':
            '前馈抑制',
            'feature': {
                'RP': -.1,
                'transmitter_release_sum': .1,
            },
            'dendrites': [
                # {
                #     'name':
                #     '前馈抑制_DAdd',
                #     'feature': {},
                #     'dendrites': [
                #     ],
                # },
                {
                    'name':
                    '前馈抑制_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                        'RP': -.1,
                        'transmitter_release_sum': .1,
                        'self_synapse': 1,
                    },
                    'dendrites': [{
                        'name': f'前馈抑制_DMax_棘{i}',
                        'feature': {
                            'type': TYPE['dendrite_max'],
                            'RP': -.1,
                            'transmitter_release_sum': .1,
                        },
                    } for i in range(SPINE_SUM_ON_A_DENDRITE)],
                },
            ],
            'axons': [
                {
                    'name': '前馈抑制_A抑制累积前馈预测',
                    'feature': {
                        'post_sign': -1,
                        'refractory': 1,
                    },
                },
                {
                    'name': '前馈抑制_A禁止前馈激励',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 1,
                    },
                },
            ],
        },
        {
            'name':
            '累积前馈预测',
            'feature': {
                # 'self_synapse': 1,
                'produce_marker_per_spike': 65,
            },
            'dendrites': [
                {
                    'name': '累积前馈预测_DMax',
                    'feature': {
                        'type': TYPE['dendrite_max'],
                        'self_synapse': 1,
                    },
                },
            ],
            'axons': [
                {
                    'name': '累积前馈预测_A易化激励累积前馈预测',
                    'feature': {
                        'release_type': RELEASE_TYPE['Fa'],
                        'transmitter_release_sum': 1,
                    },
                },
                {
                    'name': '累积前馈预测_A反馈预测属性',
                    'feature': {},
                },
                {
                    'name': '累积前馈预测_A易化属性横向预测',
                    'feature': {
                        'release_type': RELEASE_TYPE['Fa'],
                        'transmitter_release_sum': 1,
                    },
                },
                {
                    'name': '累积前馈预测_A易化STD属性横向预测',
                    'feature': {
                        'release_type': RELEASE_TYPE['Fa'],
                        'transmitter_release_sum': 1,
                    },
                },
                {
                    'name': '累积前馈预测_A全或无解禁激励数字预测onehot',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 2,
                    },
                },
                {
                    'name': '累积前馈预测_A激励onehot',
                    'feature': {
                        'step_length': 2,
                    },
                },
            ],
        },
        {
            'name':
            '累积前馈预测onehot',
            'feature': {},
            'dendrites': [
                {
                    'name':
                    '累积前馈预测onehot_DMin',
                    'feature': {
                        'type': TYPE['dendrite_min'],
                    },
                    'dendrites': [
                        {
                            'name': '累积前馈预测onehot_DAdd累积前馈预测',
                            'feature': {},
                        },
                        # {
                        #     'name': '累积前馈预测onehot_DAdd限制累积前馈预测最大值',
                        #     'feature': {},
                        # },
                    ]
                },
            ],
            'axons': [
                {
                    'name': '累积前馈预测onehot_A易化属性横向预测',
                    'feature': {
                        'release_type': RELEASE_TYPE['Fa'],
                        'transmitter_release_sum': 1,
                    },
                },
                {
                    'name': '累积前馈预测onehot_A全或无弱抑制',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 1,
                    },
                },
                {
                    'name': '累积前馈预测onehot_A激励得出结论',
                    'feature': {
                        'step_length': 6,
                    },
                },
                {
                    'name': '累积前馈预测onehot_A抑制',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ],
        },
        {
            'name': '累积前馈预测onehot出现',
            'feature': {},
            'dendrites': [],
            'axons': [],
        },
        {
            'name':
            '累积前馈预测onehot持续',
            'feature': {},
            'dendrites': [],
            'axons': [
                {
                    'name': '累积前馈预测onehot持续_A激励行动',
                    'feature': {
                        'transmitter_release_sum': 1,
                    },
                },
                {
                    'name': '累积前馈预测onehot持续_A禁止激励数字预测onehot出现',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ],
        },
        {
            'name': '前馈预测意外',
            'feature': {
                'produce_marker_per_spike': .00001
            },
        },
        {
            'name': '前馈预测偏差',
            'feature': {
                'produce_marker_per_spike': .00001
            },
        },
    ],
}
