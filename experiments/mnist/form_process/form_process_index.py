import importlib
from consts.experiment import EXPERIMENT_NAME, CORTEX_OPTS

FORM_PROCESS_NAMES = CORTEX_OPTS['form_synapse_rules']
FORM_PROCESS_INDEX = [
    importlib.import_module(
        f'experiments.{EXPERIMENT_NAME}.form_process.{form_process_name}').
    form_init_nerve for form_process_name in FORM_PROCESS_NAMES
]