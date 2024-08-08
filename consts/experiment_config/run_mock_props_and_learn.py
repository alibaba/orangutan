import numpy as np

CORTEX_OPTS = {
    'name':
    'predict',
    'MODE':
    'run',
    'IS_MOCK_RECORD_PROPS':
    1,
    'CORTEX_W':
    1000000,
    # 'CORTEX_SPINE_W': 10000,
    'mode':
    'learn',
    'load_cortex_name': ['cortex_save', 'cortex_save_posterior'][0],
    'render_load_cortex_name': ['cortex_save', 'cortex_save_posterior'][1],
    'enable_posterior_form':
    1,
    'controller':
    'mock_props_and_learn',
    'WRITE_STAGES_lambda':
    lambda cortex_obj: [
        *([
            'init',
            'form_debug_circuit',
            # 'mock_input',
            # 'mock_next_props',
            # 'load_next_feature',
            # 'create_new_dendrite_spine',
            # 'spike_start',
            # 'mock_feature_cycle_end',
            # 'cal_and_mock_predict_error',
            # 'mnist_end',
            # # # 'hippocampal_replay_start',
            # # 'before_mock_marker_remain'
            # 'before_form_synapse',
            # # 'form_synapse',
            # # 'firm_synapse',
            # 'before_add_LTP',
            # 'add_LTP',
            # 'spike_axon_end',
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
    'MNIST_INPUTS_LIST': [
        # *([f'{num}_{i}' for i in range(20) for num in range(10)])
        # *([f'{num}_{i}' for num in range(10) for i in range(20)])
        *([f'{num}_{i}' for num in [2] for i in range(20)])
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