import numpy as np
from .experiment_config.mock_input_and_percept_feature import (
    INIT_CORTEX_OPTS as init_mock_input_and_percept_feature,
    RUN_CORTEX_OPTS as run_mock_input_and_percept_feature,
)
from .experiment_config.mock_feature_and_cal_props import (
    INIT_CORTEX_OPTS as init_mock_feature_and_cal_props,
    RUN_CORTEX_OPTS as run_mock_feature_and_cal_props,
)
from .experiment_config.mock_props_and_learn import (
    INIT_CORTEX_OPTS as init_mock_props_and_learn_cortex_opts,
    RUN_CORTEX_OPTS as run_mock_props_and_learn_cortex_opts,
)

CORTEX_OPTS = [
    # init_mock_input_and_percept_feature,
    run_mock_input_and_percept_feature,
    # init_mock_feature_and_cal_props,
    # run_mock_feature_and_cal_props,
    # init_mock_props_and_learn_cortex_opts,
    # run_mock_props_and_learn_cortex_opts,
][0]

EXPERIMENT_NAME = "mnist"
APP_MODE = "view"

DATAS_DIR = f"/Users/laola/CodeProject/Orangutan/experiments/{EXPERIMENT_NAME}/datas"

# SAVE_AND_HISTORY_SUFFIX = ['', '_stp'][0]
SAVE_AND_HISTORY_SUFFIX = ["", "_debug"][0]
SAVE_DIR = f"{DATAS_DIR}/save"
# 2check
# HISTORY_DIR = f'{DATAS_DIR}/history'
HISTORY_DIR = f"{DATAS_DIR}/history"
#
INPUT_DIR = f"{DATAS_DIR}/input"
