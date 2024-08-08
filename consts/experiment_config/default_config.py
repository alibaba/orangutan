import numpy as np
DEFAULT_CONFIG = {
    'MODE':
    'init',
    'IS_MOCK_RECORD_PROPS':
    0,
    'CORTEX_W':
    1000000,
    'load_cortex_name': ['cortex_save', 'cortex_save_posterior'][0],
    'render_load_cortex_name': ['cortex_save', 'cortex_save_posterior'][0],
    'enable_posterior_form':
    0,
    'controller':
    '',
    'WRITE_STAGES_lambda':
    lambda cortex_obj: ['init'],
    'write_slice_lambda':
    lambda cortex_obj, cortex, get_soma_inds, REGION, TYPE: np.concatenate((
        cortex['ind'][(cortex['region_no'] == REGION['全局调控']['region_no'])],
    )),
    'WRITE_NERVE_PROPS': ['excite'],
    'MNIST_INPUTS_LIST': [],
    'region_names': [],
    'form_synapse_rules': [],
    'form_posterior_synapse_rules': [],
}
