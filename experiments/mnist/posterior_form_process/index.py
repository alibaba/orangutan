import importlib
from consts.experiment import EXPERIMENT_NAME, CORTEX_OPTS
from consts.region_and_synapse import REGION_AND_SYNAPSE_META

# FORM_PROCESS_NAMES = REGION_AND_SYNAPSE_META['form_posterior_synapse_rules']
FORM_PROCESS_NAMES = CORTEX_OPTS['form_posterior_synapse_rules']

FORM_PROCESS_INDEX = [
    importlib.import_module(
        f'experiments.{EXPERIMENT_NAME}.posterior_form_process.{form_process_name}'
    ).form_init_nerve for form_process_name in FORM_PROCESS_NAMES
]