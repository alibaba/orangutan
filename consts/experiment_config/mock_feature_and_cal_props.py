import numpy as np
from .default_config import DEFAULT_CONFIG

common_cortex_opts = {
    **DEFAULT_CONFIG,
    'CORTEX_W': 10000000,
    'controller': 'mock_feature_and_cal_props_controller',
    'region_names': [
        '全局调控',
        '角',
        '叉',
        '轮廓中心',
        '外轮廓边界',
        '位置_整体中心',
        '位置_当前特征',
        '位置_当前特征相对整体中心的偏移',
        '位置_锚点特征',
        '位置_当前特征相对锚点特征的偏移',
        '属性',
    ],
}

INIT_CORTEX_OPTS = {
    **common_cortex_opts,
    'MODE':
    'init',
    'WRITE_STAGES_lambda':
    lambda cortex_obj: [],
    'write_slice_lambda':
    lambda cortex, get_soma_inds, REGION: [],
    'WRITE_NERVE_PROPS': [],
    'form_synapse_rules': [
        # 位置
        '位置-激励特征位置和整体中心位置',
        '位置-激励当前特征相对整体中心的偏移',
        '位置-激励当前特征相对锚点特征的偏移',

        # 属性
        '属性-特征激励属性',
        '属性-绝对属性激励相对属性',
        '属性-锚点的绝对属性激励相对锚点的属性',
        '属性-出现持续消失_个体编码',
        '属性-个体编码激励群体编码',
    ],
}

RUN_CORTEX_OPTS = {
    **common_cortex_opts,
    'MODE':
    'run',
    'IS_MOCK_RECORD_PROPS':
    0,
    'WRITE_STAGES_lambda':
    lambda cortex_obj: [
        *([
            'init',
            # 'spike_start',
            # 'cycle_end',
        ]),
    ],
    'write_slice_lambda':
    lambda cortex_obj, cortex, get_soma_inds, REGION, TYPE: np.concatenate((
        cortex['ind'][(cortex['region_no'] <= REGION['轮廓中心']['region_no'])],
        cortex['ind'][cortex['type'] == TYPE['soma']],
    )),
    'WRITE_NERVE_PROPS': [
        'excite',
    ],
    'MNIST_INPUTS_LIST':
    # [(f'{num}_{i}', num) for num in range(10) for i in range(10)],
    [f'{num}_{i}' for num in [2] for i in range(20)],
}