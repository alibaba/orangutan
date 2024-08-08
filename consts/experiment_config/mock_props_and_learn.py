import numpy as np
from .default_config import DEFAULT_CONFIG
# from ...experiments.mnist.experiment_enviroment.run_env.mock_features1 import mock_features

common_cortex_opts = {
    **DEFAULT_CONFIG,
    'CORTEX_W':
    1000000,
    'controller':
    'mock_props_and_learn_controller',
    'region_names': [
        '全局调控',
        '位置_当前特征',
        '位置_锚点特征',
        '位置_整体中心',
        '位置_当前特征相对锚点特征的偏移',
        '位置_当前特征相对整体中心的偏移',
        '属性',
        '数字',
    ],
    'MNIST_INPUTS_LIST': [
        # *([f'{num}_{i}' for i in range(20) for num in range(10)])
        # *([f'{num}_{i}' for num in range(10) for i in range(20)])
        # *([f'{num}_{i}' for num in [2] for i in range(20)])
        # *(list(mock_features.keys())),
        # *[
        #     '0_27', '0_32', '0_200', '0_202', '0_45', '0_255', '0_442', '0_89',
        #     '0_400', '0_238', '0_191', '0_189', '0_295', '0_412', '0_116',
        #     '0_318'
        # ],
        # *[
        #     '6_2', '6_18', '6_48', '6_108', '6_124', '6_160', '6_174', '6_214',
        #     '6_702', '6_47', '6_59', '6_64', '6_120', '6_123', '6_111',
        #     '6_144', '6_234', '6_356', '6_422'
        # ],
        *[
            '8_66', '8_283', '8_314', '8_435', '8_448', '8_473', '8_678',
            '8_43', '8_93', '8_171', '8_311', '8_49'
        ],
        # *[
        #     '0_27', '6_2', '8_66', '0_32', '6_18', '8_283', '0_200', '6_48',
        #     '8_314', '0_202', '6_108', '8_435', '0_45', '6_124', '8_448',
        #     '0_255', '6_160', '8_473', '0_442', '6_174', '8_678', '0_89',
        #     '6_214', '8_43', '0_400', '6_702', '8_93', '0_238', '6_47',
        #     '8_171', '0_191', '6_59', '8_311', '0_189', '6_64', '8_49',
        #     '0_295', '6_120', '0_412', '6_123', '0_116', '6_111', '0_318',
        #     '6_144', '6_234', '6_356', '6_422'
        # ],
        # *([
        #     f'{num}_{i}' for i in [
        #         # range(10),
        #         range(20),
        #     ][0] for num in [
        #         # [2, 5],
        #         [5],
        #     ][0]
        # ] * 50)
    ],
}

INIT_CORTEX_OPTS = {
    **common_cortex_opts,
    'name': 'train',
    'MODE': 'init',
    'enable_posterior_form': 0,
    'WRITE_STAGES_lambda': lambda cortex_obj: [],
    'write_slice_lambda': lambda cortex, get_soma_inds, REGION: [],
    'form_synapse_rules': [
        '属性-个体编码激励群体编码',
    ],
    'WRITE_NERVE_PROPS': [],
}

RUN_CORTEX_OPTS = {
    **common_cortex_opts,
    'name':
    'predict',
    'MODE':
    'run',
    'IS_MOCK_RECORD_PROPS':
    1,
    'render_load_cortex_name': ['cortex_save', 'cortex_save_posterior'][1],
    'enable_posterior_form':
    1,
    # 'form_posterior_synapse_rules': [
    #     '属性-通用前馈预测',
    # ],
    'WRITE_STAGES_lambda':
    lambda cortex_obj: [
        *([
            'init',
            'form_debug_circuit',
            'form_debug_circuit_with_prop_value_map_list',
            # 'mock_input',
            # 'mock_next_props',
            # 'load_next_feature',
            # 'create_new_dendrite_spine',
            # 'spike_start',
            # 'mock_feature_cycle_end',
            # 'cal_and_mock_predict_error',
            'mnist_end',
            # # # 'hippocampal_replay_start',
            # # 'before_mock_marker_remain'
            # 'before_form_synapse',
            # # 'form_synapse',
            # # 'firm_synapse',
            # 'before_add_LTP',
            # 'add_LTP',
            # 'spike_soma',
            'spike_axon',
            # 'spike_axon_end',
            # 'spike_dendrite',
            'cycle_end',
            # 'weaken_synapse',
            # 'form_circuit_between_nerves',
            # 'adjust_LTP_limit_of_each_stable_circuit',
            # 'enlarge_spine',
            # 'shrink_spine',
            # 'spine_compete',
            # 'before_spine_compete',
            # *(['adjust_LTP_limit_of_each_stable_circuit']
            #   #   if cortex_obj.tick > 1400 else []),
            #   if 'mock_excites' not in cortex_obj.controller.mock_props.
            #   nowa_feature_exinfo else []),
            # 'on_after_weaken_synapse',
            # 'on_cortex_cycle_end',
            # # 'reset_cortex_props_to_initial_state',
            # 'before_mock_input',
            # 'after_mock_input',
            #     'after_form_synapse',
            #     # # 'weaken_synapse_by_seretonin',
            #     'spine_competition',
            # 'new_fa_nerve',
            # 'reset_cortex_props_to_initial_state',
            # 'before_cut_off',
            # 'after_cut_off',
            # 'axon_end_post_spine_active',
            # 'reset_cortex_props_to_initial_state',
        ]),
    ],
    'write_slice_lambda':
    lambda cortex_obj, cortex, get_soma_inds, REGION, TYPE: np.concatenate((
        cortex['ind'][(cortex['region_no'] == REGION['全局调控']['region_no'])],
        cortex['ind'][(cortex['region_no'] >= REGION['位置_当前特征']['region_no'])],
        # cortex['ind'][cortex['type'] == TYPE['soma']],
    )),
    'WRITE_NERVE_PROPS': [
        'excite',
        'marker_remain',
        # 'dopamine_remain',
        'exinfo_0',
        'exinfo_1',
        'exinfo_2',
        'exinfo_3',
        'exinfo_4',
        # 'seretonin_remain',
        'Fa',
        'STP',
        'LTP',
        'max_circuit_length',
        'spine_active',
        # 'anti_spine_active',
        # 'increased_LTP',
    ],
}