from .experiment_config.mock_input_and_percept_feature import (
    INIT_CORTEX_OPTS as init_mock_input_and_percept_feature,
    RUN_CORTEX_OPTS as run_mock_input_and_percept_feature,
)

CORTEX_OPTS = [
    # init_mock_input_and_percept_feature,
    run_mock_input_and_percept_feature,
][0]

EXPERIMENT_NAME = "mnist"
APP_MODE = "view"

DATAS_DIR = f"/Users/laola/CodeProject/Orangutan/experiments/{EXPERIMENT_NAME}/datas"

SAVE_AND_HISTORY_SUFFIX = ["", "_debug"][0]
SAVE_DIR = f"{DATAS_DIR}/save"
HISTORY_DIR = f"{DATAS_DIR}/history"
INPUT_DIR = f"{DATAS_DIR}/input"
