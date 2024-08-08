import importlib
from consts.experiment import EXPERIMENT_NAME, CORTEX_OPTS
from consts.region_and_synapse import REGION_AND_SYNAPSE_META

# REGIONS_INDEX = REGION_AND_SYNAPSE_META['region_names']
REGIONS_INDEX = CORTEX_OPTS['region_names']

regions_index = [
    importlib.import_module(
        f'experiments.{EXPERIMENT_NAME}.regions.{region_name}').region_info
    for region_name in REGIONS_INDEX
]