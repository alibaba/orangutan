from consts.nerve_props import TYPE, RELEASE_TYPE
region_info = {
    'region_name':
    '数字_全局调控',
    'region_shape': (1, 1, 1),
    'neurons': [
        {
            'name':
            '测试阶段',
            'feature': {
                
            },
            'dendrites': [],
            'axons': [
                {
                    'name': '测试阶段_A禁止激励前馈预测偏差',
                    'feature': {
                        'post_sign': -1,
                    },
                },
            ],
        },
        {
            'name':
            '初步预测兴奋门槛',
            'feature': {
                
            },
            'axons': [
                {
                    'name': '初步预测兴奋门槛_A阻止激励标准化初步预测兴奋',
                    'feature': {
                        'post_sign': -1,
                        'all_or_none': 1,
                    },
                },
                {
                    'name': '初步预测兴奋门槛_A解禁激励标准化初步预测兴奋',
                    'feature': {
                        'post_sign': -1,
                        'transmitter_release_sum': 10 * 2,
                    },
                },
            ],
        },
    ],
}
