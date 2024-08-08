from consts.experiment import CORTEX_OPTS
import itertools
from ..input_mocker.abstract_mocker import Abstract_mocker
from experiments.util import get_soma_inds


class Abstract_controller():

    def __init__(self, cortex_obj):
        self.cortex_obj = cortex_obj
        self.cortex = cortex_obj.cortex
        self.input_mocker = self.get_input_mocker()

    def get_mock_feature_list(self, run_tick_sum_per_feature):
        return list(
            itertools.chain(
                *[[(mnist_name, {
                    'play_direction': 'forward'
                })] * run_tick_sum_per_feature
                  for mnist_name in CORTEX_OPTS['MNIST_INPUTS_LIST']]))

    def get_input_mocker(self):
        return Abstract_mocker(self.cortex_obj)

    def mock_input(self):
        self.input_mocker.mock_input()

    def is_can_nerve_spike(self):
        return True

    def is_can_form_synapse(self):
        return CORTEX_OPTS['enable_posterior_form']

    def is_can_weaken_synapse(self):
        return CORTEX_OPTS['enable_posterior_form']

    def is_can_reset_cortex_props_at_cycle_end(self):
        return False

    def is_at_mnist_start(self):
        return False

    def is_at_mnist_end(self):
        return False

    def prepare_for_form_synapse(self):
        pass

    def get_active_num(self):
        return

    def on_cortex_inited(self):
        pass

    def on_cortex_start(self):
        pass

    def on_cortex_cycle_end(self):
        pass

    def on_after_form_synapse(self):
        pass

    def on_after_weaken_synapse(self):
        pass

    def is_mocking_intersection_features(self):
        return False

    def form_circuit(self):
        return

    def form_circuit_between_nerves(self, mother_inds, father_ind):
        return
