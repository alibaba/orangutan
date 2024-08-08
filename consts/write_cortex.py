import importlib
from experiments import REGION, experiment_enviroment
from consts.experiment import EXPERIMENT_NAME
from .nerve_props import PART_PROPS, STATIC_PROP_NAMES
from consts.experiment import CORTEX_OPTS


def is_can_write(cortex_obj, write_stage):
    is_can_write = True

    WRITE_STAGES = CORTEX_OPTS['WRITE_STAGES_lambda'](cortex_obj)

    if write_stage not in WRITE_STAGES:
        is_can_write = False

    return is_can_write


# 记录动态变化的属性
WRITE_NERVE_PROPS = CORTEX_OPTS['WRITE_NERVE_PROPS']
# WRITE_PART_PROPS_DTYPE = [(k, v[0]) for k, v in PART_PROPS.items()
#                           if k in WRITE_NERVE_PROPS]
WRITE_PART_PROPS = [k for k, v in PART_PROPS.items() if k in WRITE_NERVE_PROPS]
