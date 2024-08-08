import importlib
from consts.experiment import EXPERIMENT_NAME
regions = importlib.import_module(f'experiments.{EXPERIMENT_NAME}.regions')
REGION = regions.REGION
SOMA_SLICE_MAP=regions.SOMA_SLICE_MAP
form_init_nerve = importlib.import_module(
    f'experiments.{EXPERIMENT_NAME}.form_process').form_init_nerve
form_synapse = importlib.import_module(
    f'experiments.{EXPERIMENT_NAME}.posterior_form_process').form_process
experiment_enviroment = importlib.import_module(
    f'experiments.{EXPERIMENT_NAME}.experiment_enviroment')
