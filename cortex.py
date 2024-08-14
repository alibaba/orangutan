import math
import numpy as np
import importlib
from consts.base import LEN
from consts.feature import ABSTRACT_EXCITE
from consts.experiment import APP_MODE, CORTEX_OPTS, EXPERIMENT_NAME
from consts.nerve_props import (
    DENDRITE_TYPE,
    PART_PROPS_DTYPE,
    PART_PROPS_MATRIX,
    TYPE,
    PART_PROPS_KEYS_MAP,
    RELEASE_TYPE,
    PART_PROPS,
    DYNAMIC_PROP_NAMES,
    STATIC_PROP_NAMES,
    SPINE_EXINFO,
    POSTERIOR_SYNAPSE_EXINFO,
)
from consts.write_cortex import is_can_write, WRITE_PART_PROPS
from consts.nerve_params import (
    ATP,
    PRE_LTP_SUM_BASE,
    DIED_LTP_THRESHOLD,
    POST_SYNAPSE_RESOURCE_SUM,
    POSTERIOR_SYNAPSE_TRANSMITTER_SUM,
    SPINE_SUM_ON_A_DENDRITE,
    STANDARD_PREDICT_EXCITE,
    ABSTRACT_SYNAPSE_RP,
)
from util import print_exe_timecost, exchange_slice_to_inds
from experiments import (
    REGION,
    form_init_nerve,
    form_synapse,
    experiment_enviroment,
    SOMA_SLICE_MAP,
)
from utils.write_n_read_cortex import Write_n_read_cortex
from experiments.util import get_soma_inds

from experiments.mnist.experiment_enviroment.run_env.mock_globals import (
    APPEAR_NERVE_SUFFIXs,
)

mock_module = importlib.import_module(
    f"experiments.{EXPERIMENT_NAME}.experiment_enviroment.{experiment_enviroment.USE_ENV}"
)
PREDICT_SUPRISE_INDS = mock_module.mock_globals.PREDICT_SUPRISE_INDS
SINGLE_ABSTRACT_APPEAR_INDS = mock_module.mock_globals.SINGLE_ABSTRACT_APPEAR_INDS
POPU_ABSTRACT_APPEAR_INDS = mock_module.mock_globals.POPU_ABSTRACT_APPEAR_INDS
PREDICT_INDS = mock_module.mock_globals.PREDICT_INDS
PREDICT_BIAS_INDS = mock_module.mock_globals.PREDICT_BIAS_INDS
write_n_read_cortex = Write_n_read_cortex()

Controller = importlib.import_module(
    f'experiments.{EXPERIMENT_NAME}.experiment_enviroment.{experiment_enviroment.USE_ENV}.controller.{CORTEX_OPTS["controller"]}'
).Controller


class Cortex:

    def __init__(self):
        pass

    def init(self):
        self.init_tick()
        self.mnist_name = None
        self.mock_file_name = None
        self.nerve_marker_map = {}
        global cortex_map
        self.cortex = {
            name: np.full(CORTEX_OPTS["CORTEX_W"], -1, dtype)
            for name, dtype in PART_PROPS_DTYPE
        }

        if CORTEX_OPTS["MODE"] == "init":
            self.init_cortex()
            self.save_cortex()
        elif CORTEX_OPTS["MODE"] == "run":
            self.load_cortex()

        self.controller = Controller(self)
        self.controller.on_cortex_inited()

        self.spine_circuit_map = {}

        self.write_cortex("init")

        self.start_cortex_cycle()

    def init_tick(self):
        self.tick = 0
        self.write_cortex_tick = 1

    def record_circuit_on_a_spine(self, spine_ind, nerve_ind, feature_ind):
        self.spine_circuit_map[spine_ind] = self.spine_circuit_map.get(spine_ind, {})
        self.spine_circuit_map[spine_ind][feature_ind] = self.spine_circuit_map[
            spine_ind
        ].get(feature_ind, [])

        self.spine_circuit_map[spine_ind][feature_ind].append(nerve_ind)

    @print_exe_timecost()
    def init_cortex(self):
        self.new_ind_start = 0
        self.init_static_parts()
        self.update_new_marker_start()
        self.record_static_parts()
        self.init_static_nerves()
        self.record_static_nerves()

    def reset_cortex_props_to_initial_state(
        self, reset_inds=None, exclude_props=[], include_props=[], reset_force=0
    ):
        if isinstance(reset_inds, np.ndarray):
            reset_inds = list(reset_inds)

        if isinstance(reset_inds, list) and len(reset_inds) == 0:
            return

        reset_prop_names = DYNAMIC_PROP_NAMES
        if len(include_props) > 0:
            reset_prop_names = include_props
        elif len(exclude_props) > 0:
            reset_prop_names = [
                prop_name
                for prop_name in reset_prop_names
                if prop_name not in exclude_props
            ]
        for prop_name in reset_prop_names:
            self.reset_cortex_single_prop_to_initial_state(
                reset_inds, prop_name, reset_force
            )

        self.write_cortex("reset_cortex_props_to_initial_state")

    def reset_cortex_single_prop_to_initial_state(
        self, reset_inds, prop_name, reset_force=0
    ):
        cortex_slice = (
            np.asarray(reset_inds) if reset_inds else slice(self.new_ind_start)
        )

        if prop_name == "excite":

            is_can_reset_mask = self.cortex["self_synapse"][cortex_slice] <= reset_force

            if reset_inds:
                self.cortex["excite"][cortex_slice[is_can_reset_mask]] = self.cortex[
                    "RP"
                ][cortex_slice[is_can_reset_mask]]

            else:
                self.cortex["excite"][cortex_slice][is_can_reset_mask] = self.cortex[
                    "RP"
                ][cortex_slice][is_can_reset_mask]

        else:
            unique_vals = np.unique(PART_PROPS[prop_name][1:])

            if unique_vals.size == 1:
                self.cortex[prop_name][cortex_slice] = unique_vals[0]

            else:
                self.cortex[prop_name][cortex_slice] = np.asarray(
                    PART_PROPS[prop_name][1:]
                )[self.cortex["type"][cortex_slice]]

    def update_new_marker_start(self):
        self.new_marker_start = np.max(self.cortex["marker"]) + 1

    def save_cortex(self, save_type="save"):
        self.write_cortex(save_type)
        print("[save_cortex]", save_type, "succ!")

    def load_cortex(self):
        write_n_read_cortex.init_cortex_save_data(cortex_obj=self)
        self.new_ind_start = write_n_read_cortex.cortex_info["cortex_slice_stop"]
        self.record_static_parts(write_n_read_cortex.cortex_info)
        self.record_static_nerves(write_n_read_cortex.cortex_info)
        # self.record_spine_marker_sypanses(write_n_read_cortex.cortex_info)

        # Set initial non-static custom attribute for dendrite
        for region_info in REGION.values():
            has_no_static_feature_nerves = [
                neuron
                for neuron in region_info["neurons"].values()
                if len(
                    [
                        feature_name
                        for feature_name in neuron.get("feature", {}).keys()
                        if feature_name not in STATIC_PROP_NAMES
                    ]
                )
                > 0
            ]
            for nerve_info in has_no_static_feature_nerves:
                nerve_inds = self.cortex["ind"][self.cortex_static_part_slice][
                    (
                        self.cortex["neuron_no"][self.cortex_static_part_slice]
                        == nerve_info["neuron_no"]
                    )
                    * (
                        self.cortex["region_no"][self.cortex_static_part_slice]
                        == region_info["region_no"]
                    )
                ]
                for feature_name, feature_value in nerve_info["feature"].items():
                    if feature_name in STATIC_PROP_NAMES:
                        continue
                    self.cortex[feature_name][nerve_inds] = feature_value

        # Load marker map information.
        self.nerve_marker_map = write_n_read_cortex.cortex_info["nerve_marker_map"]
        self.update_new_marker_start()

    def record_static_parts(self, cortex_info=None):
        if cortex_info:
            self.cortex_static_part_slice = slice(
                cortex_info["cortex_static_part_slice_stop"]
            )
        else:
            self.cortex_static_part_slice = slice(self.new_ind_start)

    def record_static_nerves(self, cortex_info=None):
        if cortex_info:
            self.cortex_static_nerve_slice = slice(
                cortex_info["cortex_static_part_slice_stop"],
                cortex_info["cortex_static_nerves_slice_stop"],
            )
        else:
            self.cortex_static_nerve_slice = slice(
                self.cortex_static_part_slice.stop, self.new_ind_start
            )

    def init_static_parts(self):
        cortex = self.cortex
        self.col_no_start = LEN[
            "col_no"
        ]  # The pillar number is set as a three-digit number, starting from 100.
        self.new_ind_start += 1  # Set the 0th nerve to be an empty nerve.

        for region_name in REGION.keys():
            region_info = REGION[region_name]
            (
                col_sum,
                neuron_sum,
                matrix_range,
                neuron_inds,
                col_nos,
                region_row_nos,
                region_hyper_col_nos,
                hyper_col_ind,
                mini_col_ind,
                neuron_nos,
                mother_neuron_nos,
                markers,
                neuron_in_pic_mask,
                pre_inds,
                post_inds,
                soma_inds,
            ) = self.get_init_soma_params(region_info, self.col_no_start)
            self.new_ind_start += neuron_sum
            # Attributes set each other's dependencies, do not randomly adjust the order.
            self.set_soma_base_props(matrix_range, region_info, neuron_in_pic_mask)
            cortex["col_no"][matrix_range] = col_nos
            cortex["region_no"][matrix_range] = region_info["region_no"]
            cortex["neuron_no"][matrix_range] = neuron_nos
            cortex["mother_neuron_no"][matrix_range] = mother_neuron_nos
            cortex["ind"][matrix_range] = neuron_inds
            cortex["marker"][matrix_range] = markers
            cortex["region_row_no"][matrix_range] = region_row_nos
            cortex["region_hyper_col_no"][matrix_range] = region_hyper_col_nos
            cortex["hyper_col_ind"][matrix_range] = hyper_col_ind
            cortex["mini_col_ind"][matrix_range] = mini_col_ind
            cortex["post_ind"][matrix_range] = post_inds
            cortex["pre_ind"][matrix_range] = pre_inds
            cortex["soma_ind"][matrix_range] = soma_inds
            self.set_soma_features(
                matrix_range, region_info, col_sum, neuron_in_pic_mask
            )
            self.col_no_start += col_sum

    def get_init_soma_params(self, region_info, col_no_start):
        region_name = region_info["region_name"]
        region_shape = region_info["region_shape"]
        region_row_sum, hyper_col_sum_per_row, mini_col_sum_in_hyper_col = region_shape
        hyper_col_sum = hyper_col_sum_per_row * region_row_sum
        col_sum = hyper_col_sum * mini_col_sum_in_hyper_col
        mini_col_sum_per_row = hyper_col_sum_per_row * mini_col_sum_in_hyper_col
        all_neuron_sum = 0
        col_nos = []
        region_row_nos = []
        region_hyper_col_nos = []
        hyper_col_inds = []
        mini_col_inds = []
        neuron_nos = []
        mother_neuron_nos = []
        markers = []
        all_neuron_in_pic_mask = []
        pre_inds = []
        post_inds = []
        soma_inds = []

        for neuron_name, neuron_info in region_info["neurons"].items():
            neuron_slice_info = SOMA_SLICE_MAP[region_name][neuron_name]
            matrix_range = neuron_slice_info["cortex_slice"]
            neuron_in_pic_mask = neuron_slice_info.get(
                "neuron_in_pic_mask", np.full(col_sum, True)
            ).repeat(mini_col_sum_in_hyper_col)
            all_neuron_in_pic_mask.extend(neuron_in_pic_mask)
            neuron_sum = matrix_range.stop - matrix_range.start
            all_neuron_sum += neuron_sum
            # matrix_range = slice(self.new_ind_start,
            #                      self.new_ind_start + neuron_sum)
            # self.static_part_slice_map[region_name][neuron_name] = matrix_range
            col_nos.extend(np.arange(col_sum)[neuron_in_pic_mask] + col_no_start)
            region_row_nos.extend(
                np.arange(region_row_sum).repeat(mini_col_sum_per_row)[
                    neuron_in_pic_mask
                ]
                + 1
            )
            region_hyper_col_nos.extend(
                np.tile(
                    np.arange(hyper_col_sum_per_row).repeat(mini_col_sum_in_hyper_col),
                    region_row_sum,
                )[neuron_in_pic_mask]
                + 1
            )
            hyper_col_inds.extend(
                np.arange(region_info["hyper_col_sum"])[neuron_in_pic_mask].repeat(
                    mini_col_sum_in_hyper_col
                )
            )
            mini_col_inds.extend(
                np.tile(np.arange(mini_col_sum_in_hyper_col), hyper_col_sum)[
                    neuron_in_pic_mask
                ]
                + 1
            )
            neuron_nos.extend(
                np.tile([neuron_info["neuron_no"]], col_sum)[neuron_in_pic_mask]
            )
            mother_neuron_nos.extend(
                np.tile([neuron_info["mother_neuron_no"]], col_sum)[neuron_in_pic_mask]
            )
            markers.extend(
                np.tile([neuron_info["marker"]], col_sum)[neuron_in_pic_mask]
            )
            pre_inds.extend(
                exchange_slice_to_inds(
                    SOMA_SLICE_MAP[region_name][neuron_info["pre_name"]]["cortex_slice"]
                )
                if neuron_info.get("pre_name")
                else np.full(neuron_sum, -1)
            )
            post_inds.extend(
                exchange_slice_to_inds(
                    SOMA_SLICE_MAP[region_name][neuron_info["post_name"]][
                        "cortex_slice"
                    ]
                )
                if neuron_info.get("post_name")
                else np.full(neuron_sum, -1)
            )
            soma_inds.extend(
                exchange_slice_to_inds(
                    SOMA_SLICE_MAP[region_name][neuron_info["soma_name"]][
                        "cortex_slice"
                    ]
                )
                if neuron_info.get("soma_name")
                else np.full(neuron_sum, -1)
            )

        matrix_range = slice(self.new_ind_start, self.new_ind_start + all_neuron_sum)
        neuron_inds = np.arange(matrix_range.start, matrix_range.stop)
        return (
            col_sum,
            all_neuron_sum,
            matrix_range,
            neuron_inds,
            col_nos,
            region_row_nos,
            region_hyper_col_nos,
            hyper_col_inds,
            mini_col_inds,
            neuron_nos,
            mother_neuron_nos,
            markers,
            all_neuron_in_pic_mask,
            pre_inds,
            post_inds,
            soma_inds,
        )

    def set_soma_base_props(self, matrix_range, region_info, neuron_in_pic_mask):
        part_types = np.repeat(
            [neuron["type"] for neuron in region_info["neurons"].values()],
            region_info["mini_col_sum_in_region"],
        )[neuron_in_pic_mask]
        init_props = PART_PROPS_MATRIX[part_types]
        for prop, _ in PART_PROPS_DTYPE:
            self.cortex[prop][matrix_range] = init_props[prop]

    def set_soma_features(self, matrix_range, region_info, col_sum, neuron_in_pic_mask):
        reset_map = {
            prop_name: np.repeat(
                [
                    neuron_info.get("feature", {}).get(prop_name, -999)
                    for neuron_info in region_info["neurons"].values()
                ],
                col_sum,
            )[neuron_in_pic_mask]
            for prop_name in region_info["feature_set"]
        }
        for prop_name, prop_vals in reset_map.items():
            set_mask = self.cortex["bool_util"][: len(prop_vals)]
            set_mask[:] = prop_vals != -999
            self.cortex[prop_name][matrix_range][set_mask] = prop_vals[set_mask]

    def init_static_nerves(self):
        for make_new_nerve_packs in form_init_nerve:
            if not callable(make_new_nerve_packs):
                continue
            print(make_new_nerve_packs)
            make_new_nerve_packs(self)

    def add_marker_remain(self, add_inds):
        self.cortex["marker_remain"][add_inds] = (
            self.cortex["tick_spike_times"][add_inds]
            * self.cortex["LTP"][add_inds]
            * self.cortex["produce_marker_per_spike"][add_inds]
        )

        self.cortex["dopamine_remain"][add_inds] = self.cortex["marker_remain"][
            add_inds
        ]

    def update_all_marker_inds(self):
        # A synapse is considered effective only if the marker_remain is greater than 1, otherwise it is just a dendrite without computational function.
        self.all_marker_inds = np.where(self.cortex["marker_remain"] > 1)[0]

    def is_can_form_synapse(self):
        return (
            CORTEX_OPTS["enable_posterior_form"] == 1
            and self.controller.is_can_form_synapse()
        )

    def is_can_activate_dendritic_spine(self):
        current_mock_data = self.controller.input_mocker.mock_data_loader.current_data
        return (
            current_mock_data["play_direction"] == "backward"
            and self.controller.input_mocker.get_is_last_feature()
        )

    def activate_dendritic_spine(self):
        active_spine_inds = self.get_active_spine_inds_of_nowa_num()
        if len(active_spine_inds) > 0:
            # Translation: Only the most active dendritic spine is active
            active_spine_ind = active_spine_inds[
                np.argmax(
                    self.get_spine_active_with_max_circuit_length(active_spine_inds)
                )
            ]

            self.mark_spine_is_form_synapse(active_spine_ind)

            # If the most active spike already exists in a stable loop, marker_remain will not be strengthened.
            if self.get_stable_spine_mask(np.array([active_spine_ind]))[0] == False:
                self.set_active_dendritic_spine_marker_remain(
                    active_spine_ind, is_new_spine=False
                )
        else:
            self.create_new_dendrite_spine()

    def mark_spine_is_form_synapse(self, spine_ind):
        self.cortex[SPINE_EXINFO["is_form_synapse"]][self.get_all_spine_inds()] = 0
        self.cortex[SPINE_EXINFO["is_form_synapse"]][spine_ind] = 1

    def create_new_dendrite_spine(self):
        new_active_dendritic_spine_ind = self.get_new_active_dendritic_spine_ind()
        self.mark_spine_as_created(new_active_dendritic_spine_ind)
        self.set_active_dendritic_spine_marker_remain(
            new_active_dendritic_spine_ind, is_new_spine=True
        )
        self.mark_spine_is_form_synapse(new_active_dendritic_spine_ind)

        self.write_cortex("create_new_dendrite_spine")

    def mark_spine_as_created(self, spine_ind):
        self.cortex["exinfo_0"][spine_ind] = 1
        self.cortex["spine_active"][spine_ind] = 400

    def set_active_dendritic_spine_marker_remain(
        self, activate_dendritic_spine_ind, is_new_spine
    ):
        MAX_MARKER_REMAIN = 2600

        if is_new_spine:
            self.cortex["marker_remain"][
                activate_dendritic_spine_ind
            ] = MAX_MARKER_REMAIN

        else:
            max_synapse_active_spine_force = np.max(
                self.cortex["spine_active"][activate_dendritic_spine_ind]
            )
            self.cortex["marker_remain"][activate_dendritic_spine_ind] = (
                MAX_MARKER_REMAIN
                * self.cortex["spine_active"][activate_dendritic_spine_ind]
                / max_synapse_active_spine_force
            )

    def get_new_active_dendritic_spine_ind(self):
        all_spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return all_spine_inds_of_nowa_num[
            self.cortex["max_circuit_length"][all_spine_inds_of_nowa_num] == 0
        ][0]

    def get_active_spine_inds_of_nowa_num(self):
        all_spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return all_spine_inds_of_nowa_num[
            self.get_active_spine_mask(all_spine_inds_of_nowa_num)
        ]

    def get_active_spine_inds_of_all_num(self):
        all_spine_inds_of_all_num = self.get_all_spine_inds()
        return all_spine_inds_of_all_num[
            self.get_active_spine_mask(all_spine_inds_of_all_num)
        ]

    def get_active_spine_mask(self, spine_inds):
        MIN_SPINE_ACTIVE_RATIO_THRESHOLD = 0.25
        stable_spine_mask = self.get_stable_spine_mask(spine_inds)
        spine_resource_limit_of_each_synapse = np.full(
            len(spine_inds), POST_SYNAPSE_RESOURCE_SUM
        )
        spine_resource_limit_of_each_synapse[stable_spine_mask] = (
            self.get_resource_limit_of_spine(spine_inds[stable_spine_mask])
        )
        return (
            self.cortex["spine_active"][spine_inds]
            / spine_resource_limit_of_each_synapse
        ) > MIN_SPINE_ACTIVE_RATIO_THRESHOLD

    def get_spine_active_with_max_circuit_length(self, spine_inds):
        spine_resource_limit_of_each_synapse = self.get_resource_limit_of_spine(
            spine_inds
        )
        return (
            self.cortex["spine_active"][spine_inds]
            / spine_resource_limit_of_each_synapse
            * self.cortex["max_circuit_length"][spine_inds]
        )

    def get_spine_inds_of_nowa_num(self):
        active_num = self.controller.get_active_num()
        return self.get_all_spine_inds(active_num)

    def get_all_spine_inds(self, nums=np.arange(10), is_inhibit_spine=False):
        if not isinstance(nums, list):
            nums = [nums]

        return np.concatenate(
            tuple(
                [
                    get_soma_inds(
                        "number",
                        [
                            f'fore{"inhibit" if is_inhibit_spine else "predict"}_DMax_spin{i}'
                            for i in range(SPINE_SUM_ON_A_DENDRITE)
                        ],
                        hyper_col_inds_in_region=num,
                    )
                    for num in nums
                ]
            )
        ).astype(int)

    def form_synapse(self):
        self.new_synapse_inds = []
        self.used_parent_marker_inds = set()
        is_new_form = False
        is_new_firm = False

        for form_synapse_func in form_synapse:
            for make_new_nerve_packs in form_synapse_func(self):
                this_is_new_form, this_is_new_firm = self.exe_make_new_nerve_packs(
                    make_new_nerve_packs
                )

                is_new_form = is_new_form or this_is_new_form
                is_new_firm = is_new_firm or this_is_new_firm

    def exe_make_new_nerve_packs(self, make_new_nerve_packs):
        self.update_all_marker_inds()

        new_nerve_slice, existed_nerve_inds, *is_loop = make_new_nerve_packs(self)

        is_new_form = new_nerve_slice and len(new_nerve_slice) > 0
        is_new_firm = len(existed_nerve_inds) > 0
        if is_new_form or is_new_firm:
            self.used_parent_marker_inds.update(self.cortex["pre_ind"][new_nerve_slice])
            self.used_parent_marker_inds.update(
                self.cortex["post_ind"][new_nerve_slice]
            )
            self.new_synapse_inds.extend(self.cortex["ind"][new_nerve_slice])

            if is_new_form:
                self.write_cortex("form_synapse")

            if is_new_firm:
                self.write_cortex("firm_synapse")

        if len(is_loop) and is_loop[0]:
            loop_is_new_form, loop_is_new_firm = self.exe_make_new_nerve_packs(
                make_new_nerve_packs
            )
            is_new_form = is_new_form or loop_is_new_form
            is_new_firm = is_new_firm or loop_is_new_firm

        return is_new_form, is_new_firm

    def get_active_prop_inds(self):
        cortex = self.cortex
        return cortex["ind"][POPU_ABSTRACT_APPEAR_INDS][
            (
                cortex["excite"][POPU_ABSTRACT_APPEAR_INDS]
                - cortex["RP"][POPU_ABSTRACT_APPEAR_INDS]
            )
            == ABSTRACT_EXCITE
        ]

    def mock_input(self):
        self.controller.mock_input()

    def init_calculate_inds(self):
        self.vary_soma_inds = set(
            np.compress(
                (self.cortex["excite"] >= ATP) * (self.cortex["type"] == TYPE["soma"]),
                self.cortex["ind"],
            )
        )
        self.vary_axon_inds = set()
        self.vary_axon_end_inds = set()
        self.vary_step_axon_end_inds = set()
        self.vary_dendrite_inds = set()

    def start_cortex_cycle(self):
        self.reset_cortex_props_to_initial_state()
        while True:
            self.cortex_cycle()

    @print_exe_timecost()
    def cortex_cycle(self):
        print("tick:", self.tick)

        if callable(self.controller.on_cortex_start):
            self.controller.on_cortex_start()

        if not hasattr(self, "vary_soma_inds"):
            self.init_calculate_inds()

        self.write_cortex("before_mock_input")
        self.mock_input()
        self.write_cortex("after_mock_input")

        if self.controller.is_can_nerve_spike():
            self.cortex_cycle_subcontent_in_predict_mode()

        if self.is_can_form_synapse():
            if self.is_can_activate_dendritic_spine():
                self.activate_dendritic_spine()
                self.adjust_LTP_limit_of_each_stable_circuit(POST_SYNAPSE_RESOURCE_SUM)
            self.controller.prepare_for_form_synapse()
            # self.form_synapse()
            # self.controller.form_circuit()
            self.update_max_circuit_length()
            self.controller.on_after_form_synapse()

            self.weaken_synapse()
            self.add_marker_remain(
                self.get_form_or_firm_synapse_inds_on_stable_spines()
            )
            self.controller.on_after_weaken_synapse()
            if self.controller.is_at_mnist_end():
                self.adjust_LTP_limit_of_each_stable_circuit()
                self.record_has_marker_remain_and_stable_spine_parents_info()
                self.has_marker_remain_and_stable_spine_inherit_size_form_parent()
                self.write_cortex("adjust_LTP_limit_of_each_stable_circuit")

        if callable(self.controller.on_cortex_cycle_end):
            self.controller.on_cortex_cycle_end()
            self.write_cortex("on_cortex_cycle_end")

        if self.controller.is_can_reset_cortex_props_at_cycle_end():
            self.reset_cortex_props_to_initial_state(reset_force=1)
            self.init_calculate_inds()
            self.write_cortex("reset_cortex_props_to_initial_state")

        self.add_tick()

    def record_has_marker_remain_and_stable_spine_parents_info(self):
        has_marker_remain_and_stable_spine_inds = (
            self.get_has_marker_remain_and_stable_spine_inds_of_nowa_num()
        )
        if not len(has_marker_remain_and_stable_spine_inds):
            return

        self.cortex[SPINE_EXINFO["parents_info"]][
            has_marker_remain_and_stable_spine_inds
        ] = self.tick

        nowa_mnist_name = self.controller.mock_props.nowa_mnist_name.replace("_", "0")

        self.cortex[SPINE_EXINFO["parents_info"]][
            has_marker_remain_and_stable_spine_inds
        ] = self.cortex[SPINE_EXINFO["parents_info"]][
            has_marker_remain_and_stable_spine_inds
        ] * math.pow(
            10, len(nowa_mnist_name) + 1
        ) + int(
            nowa_mnist_name
        )

        if self.controller.is_mocking_intersection_features():
            largest_spine_ind = str(
                self.controller.mock_props.nowa_feature_exinfo["largest_spine_ind"]
            )
            self.cortex[SPINE_EXINFO["parents_info"]][
                has_marker_remain_and_stable_spine_inds
            ] = self.cortex[SPINE_EXINFO["parents_info"]][
                has_marker_remain_and_stable_spine_inds
            ] * math.pow(
                10, len(largest_spine_ind) + 1
            ) + int(
                largest_spine_ind
            )

    def has_marker_remain_and_stable_spine_inherit_size_form_parent(self):
        if self.controller.is_mocking_intersection_features():
            has_marker_remain_and_stable_spine_inds = (
                self.get_has_marker_remain_and_stable_spine_inds_of_nowa_num()
            )
            largest_spine_ind = self.controller.mock_props.nowa_feature_exinfo[
                "largest_spine_ind"
            ]
            self.cortex[SPINE_EXINFO["size"]][
                has_marker_remain_and_stable_spine_inds
            ] = self.cortex[SPINE_EXINFO["size"]][largest_spine_ind]

    def get_form_or_firm_synapse_inds(self):
        posterior_synapse_slice = self.get_posterior_synapse_slice()
        return self.cortex["ind"][posterior_synapse_slice][
            (self.cortex["is_synapse"][posterior_synapse_slice] == 2)
            * (self.cortex["LTP"][posterior_synapse_slice] > 0)
        ]

    def get_form_or_firm_synapse_inds_on_stable_spines(self):
        form_or_firm_synapse_inds = self.get_form_or_firm_synapse_inds()
        stable_spine_mask = self.get_stable_spine_mask(
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
                form_or_firm_synapse_inds
            ].astype(int)
        )
        return form_or_firm_synapse_inds[stable_spine_mask]

    def get_has_synapse_spine_inds(self):
        all_spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return all_spine_inds_of_nowa_num[
            (self.cortex["max_circuit_length"][all_spine_inds_of_nowa_num] > 0)
        ]

    def get_has_synapse_but_unactive_spine_inds(self):
        all_spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return all_spine_inds_of_nowa_num[
            (self.cortex["spine_active"][all_spine_inds_of_nowa_num] == 0)
            * (self.cortex["max_circuit_length"][all_spine_inds_of_nowa_num] > 0)
        ]

    def get_stable_but_unactive_spine_inds(self):
        all_spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return all_spine_inds_of_nowa_num[
            (self.cortex["spine_active"][all_spine_inds_of_nowa_num] == 0)
            * self.get_stable_spine_mask(all_spine_inds_of_nowa_num)
        ]

    def cortex_cycle_subcontent_in_predict_mode(self):
        self.write_cortex("cycle_start")
        if self.controller.is_at_mnist_start():
            self.all_posterior_synapse_post_anti_spine_active()
            self.init_spine_active()
            # self.init_spine_min_excite()
            self.all_posterior_synapse_post_max_pre_synapse_LTP()
        self.init_spine_min_excite()
        self.spike()
        active_0_step_length_axon_inds = self.get_active_0_step_length_axon_inds()
        # If there is an axon with a step length of 0, the excitatory transmission of the axon will be immediately executed in the current frame.
        if len(active_0_step_length_axon_inds):
            bak_vary_soma_inds = self.vary_soma_inds
            self.vary_soma_inds = set(
                self.cortex["soma_ind"][active_0_step_length_axon_inds]
            )
            self.spike()
            self.vary_soma_inds.update(bak_vary_soma_inds)
        self.update_max_circuit_length()
        self.leak_nerves_excite_to_rest_potential()
        self.update_axon_current_step()

        self.write_cortex("cycle_end")

    def get_active_0_step_length_axon_inds(self):
        self.cortex["bool_util"][:] = 0
        self.cortex["bool_util"][list(self.vary_soma_inds)] = 1
        axon_inds = self.cortex["ind"][
            (
                (self.cortex["type"] == TYPE["axon"])
                * (self.cortex["step_length"] == 0)
                * (self.cortex["bool_util"][self.cortex["soma_ind"]] == 1)
            )
        ]
        return axon_inds

    def init_spine_active(self):
        self.cortex["spine_active"][self.get_all_spine_inds()] = -1
        # self.cortex['spine_active'][self.get_has_synapse_spine_inds()] = np.inf

    def init_spine_min_excite(self):
        self.cortex[SPINE_EXINFO["min_excite"]][self.get_all_spine_inds()] = -np.inf

    def add_tick(self):
        self.tick += 1

    @print_exe_timecost()
    def spike(self):
        self.cortex["is_active"][:] = 0
        self.write_cortex("spike_start")
        # Dendritic synaptic excitation needs to occur in the soma from elsewhere before the circuit begins, so that the excitation obtained from the soma at this time is its own dendritic synaptic excitation.
        self.dendrite_self_synaptic()
        self.spike_soma()
        self.spike_axon()
        self.spike_axon_end_loop()
        self.leak_nerves_excite_to_rest_potential()
        self.spike_dendrite_loop()

    # @print_exe_timecost()
    def spike_soma(self):
        cortex_slice = slice(self.new_ind_start)
        spike_inds = list(self.vary_soma_inds)

        self.set_spike_times_with_excite(spike_inds)
        self.cortex["is_active"][spike_inds] = 1

        to_inds = self.cortex["ind"][cortex_slice][
            (self.cortex["mother_type"][cortex_slice] == TYPE["soma"])
            * (self.cortex["is_active"][self.cortex["pre_ind"][cortex_slice]] == 1)
        ]

        spike_excite = (
            self.cortex["tick_spike_times"][self.cortex["pre_ind"][to_inds]]
            * self.cortex["transmitter_release_sum"][self.cortex["pre_ind"][to_inds]]
        )

        self.cortex["excite"][to_inds] = self.cortex["RP"][to_inds]

        self.post_excite(spike_inds, to_inds, spike_excite)

        self.add_marker_remain(spike_inds)

        self.vary_axon_inds.update(
            np.compress(self.cortex["type"][to_inds] == TYPE["axon"], to_inds)
        )
        self.vary_axon_end_inds.update(
            np.compress(self.cortex["type"][to_inds] == TYPE["axon_end"], to_inds)
        )
        self.vary_soma_inds.clear()

        # After the update of the axon terminal, the presynaptic axon terminal also needs to be involved in the subsequent calculations.
        self.cortex["bool_util"][cortex_slice] = False
        self.cortex["bool_util"][to_inds] = True
        vary_axon_end_inds = slice(
            self.cortex_static_part_slice.stop, self.new_ind_start
        )
        update_vary_axon_end_inds = np.compress(
            self.cortex["bool_util"][self.cortex["post_ind"][vary_axon_end_inds]],
            self.cortex["ind"][vary_axon_end_inds],
        )
        update_vary_axon_end_inds = update_vary_axon_end_inds[
            update_vary_axon_end_inds != -1
        ]
        self.vary_axon_end_inds.update(update_vary_axon_end_inds)

        self.write_cortex("spike_soma")

    def get_reach_step_length_inds(self, nerve_inds):
        nerve_inds = np.asarray(nerve_inds)
        reach_step_length_mask = (
            self.cortex["current_step"][nerve_inds]
            >= self.cortex["step_length"][nerve_inds]
        )
        return (
            nerve_inds[reach_step_length_mask],
            nerve_inds[~reach_step_length_mask],
            reach_step_length_mask,
        )

    def update_axon_current_step(self):

        # Reset the current step size of all neurons at rest.
        self.cortex["current_step"][self.cortex["excite"] == self.cortex["RP"]] = 1

        add_step_inds = self.cortex["ind"][
            (
                (self.cortex["current_step"] < self.cortex["step_length"])
                * (self.cortex["type"] == TYPE["axon"])
                * (self.cortex["excite"] > self.cortex["RP"])
            )
        ]

        self.cortex["current_step"][add_step_inds] += 1

        self.vary_axon_inds.update(
            add_step_inds[
                self.cortex["current_step"][add_step_inds]
                == self.cortex["step_length"][add_step_inds]
            ]
        )

    def spike_axon(self):
        axon_end_slice = slice(self.cortex_static_part_slice.stop, self.new_ind_start)

        spike_inds = list(self.vary_axon_inds)

        spike_inds, _, _ = self.get_reach_step_length_inds(spike_inds)

        self.set_spike_times_with_excite(spike_inds)
        self.cortex["is_active"][spike_inds] = 1

        to_nerves_mask = self.cortex["bool_util"][axon_end_slice]
        to_nerves_mask[:] = (
            self.cortex["mother_type"][axon_end_slice] == TYPE["axon"]
        ) * (self.cortex["is_active"][self.cortex["pre_ind"][axon_end_slice]] == 1)
        to_inds = self.cortex["ind"][axon_end_slice][to_nerves_mask]
        spike_inds = self.cortex["pre_ind"][to_inds]

        spike_excite = self.get_axon_spike_excite(spike_inds, to_inds)

        self.cortex["excite"][to_inds] = self.cortex["RP"][to_inds]

        self.post_excite(spike_inds, to_inds, spike_excite)

        self.add_marker_remain(spike_inds)

        self.vary_axon_end_inds.update(to_inds)
        self.vary_axon_inds.clear()

        # After the update of the axon terminal, the associated presynaptic axon terminal also needs to be involved in subsequent calculations.
        self.cortex["bool_util"][axon_end_slice] = False
        self.cortex["bool_util"][to_inds] = True
        vary_inds = np.compress(
            (self.cortex["type"][axon_end_slice] == TYPE["axon_end"])
            * (self.cortex["bool_util"][self.cortex["post_ind"][axon_end_slice]]),
            self.cortex["ind"][axon_end_slice],
        )
        vary_inds = vary_inds[vary_inds != -1]
        self.vary_axon_end_inds.update(vary_inds)

        self.write_cortex("spike_axon")

    def get_axon_spike_excite(self, axon_inds, to_inds):
        transmitter_release_sum = self.cortex["transmitter_release_sum"][axon_inds]
        to_inds_has_size_mask = (self.cortex["is_synapse"][to_inds] > 0) * (
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["size"]][to_inds] > 0
        )
        transmitter_release_sum[to_inds_has_size_mask] = self.cortex[
            POSTERIOR_SYNAPSE_EXINFO["size"]
        ][to_inds[to_inds_has_size_mask]]

        return self.cortex["tick_spike_times"][axon_inds] * transmitter_release_sum

    def spike_axon_end_loop(self):
        self.mark_will_recv_excite_with_nerve_inds(list(self.vary_axon_end_inds))

        self.spike_axon_end()

        if len(self.vary_axon_end_inds):
            self.spike_axon_end_loop()
        else:
            self.vary_axon_end_inds = self.vary_step_axon_end_inds.copy()

    def spike_axon_end(self):
        spike_inds = np.asarray(list(self.vary_axon_end_inds), "int")
        cortex_slice = slice(self.new_ind_start)

        def filter_spike_inds(spike_inds):

            # Is there an upstream excitement
            will_no_recv_excite_inds_mask = (
                self.cortex["will_recv_excite"][spike_inds] == 0
            )
            will_recv_excite_spike_inds = spike_inds[~will_no_recv_excite_inds_mask]
            spike_inds = spike_inds[will_no_recv_excite_inds_mask]

            # Refactory period
            is_refractory_mask = self.cortex["refractory"][spike_inds] == 2
            spike_inds = spike_inds[~is_refractory_mask]

            # _, no_reach_step_length_spike_inds, can_spike_mask = self.get_reach_step_length_inds(
            #     spike_inds)

            # return spike_inds, ~can_spike_mask, no_reach_step_length_spike_inds, will_recv_excite_spike_inds
            return spike_inds, will_recv_excite_spike_inds

        # spike_inds, _, _, will_recv_excite_spike_inds = filter_spike_inds(
        spike_inds, will_recv_excite_spike_inds = filter_spike_inds(spike_inds)
        # TODO Only the axon terminals with changing lengths will increase their step lengths, which does not apply to neurons that continuously release neurotransmitters.
        # self.vary_step_axon_end_inds.update(no_reach_step_length_spike_inds)

        to_inds = self.get(spike_inds, "post_ind")

        # When a postsynaptic neuron needs to receive excitation, all of its presynaptic neurons must participate in the computation, regardless of their own state changes.
        self.cortex["float_util"][cortex_slice] = 0
        self.cortex["float_util"][to_inds] = 1
        spike_inds = np.compress(
            (
                self.cortex["float_util"][cortex_slice][
                    self.cortex["post_ind"][cortex_slice]
                ]
                == 1
            ),
            self.cortex["ind"][cortex_slice],
        )

        # Get the final spike_inds and to_inds.
        spike_inds, _ = filter_spike_inds(
            # spike_inds, no_reach_step_length_spike_mask, _, _ = filter_spike_inds(
            spike_inds
        )
        to_inds = self.get(spike_inds, "post_ind")

        # For the synaptic axon terminals of the axon terminals, their axons also need to be involved in the calculation.
        # For the synaptic bouton of the axon terminal, it is necessary to involve their cell bodies in the calculation as well.
        to_axon_end_inds = np.unique(
            # to_inds[self.cortex['type'][to_inds] == TYPE['axon_end']])
            to_inds[
                np.logical_or(
                    self.cortex["type"][to_inds] == TYPE["axon_end"],
                    self.cortex["type"][to_inds] == TYPE["axon"],
                )
            ]
        )
        spike_axon_inds = self.cortex["pre_ind"][to_axon_end_inds]

        in_RP_to_inds_mask = (
            self.cortex["excite"][to_inds] == self.cortex["RP"][to_inds]
        )

        # This sentence is in a technical or scientific context, and it seems to be discussing the need to reset the excitation of a postsynaptic target before transmitting excitement to the synaptic target during axonal simulation.
        self.reset_cortex_props_to_initial_state(
            reset_inds=to_inds, include_props=["excite"]
        )

        # Convey the excitement of the axon to the axon terminals first.
        axon_spike_excite = self.get_axon_spike_excite(
            spike_axon_inds, to_axon_end_inds
        )
        # self.cortex['tick_spike_times'][
        #     spike_axon_inds] * -self.cortex['RP'][spike_axon_inds]
        self.post_excite(spike_axon_inds, to_axon_end_inds, axon_spike_excite)

        # Transmit the excitement of the axon terminals to the next axon terminals.
        self.set_spike_times_with_excite(spike_inds)
        spike_excite = self.get_spike_excite(spike_inds)

        # # Set the transmissible excitatory potential of the neurons that do not reach the transmission step to 0.
        # spike_excite[no_reach_step_length_spike_mask] = 0
        # And the current step length increases by 1.
        # self.cortex['current_step'][spike_inds] += 1

        # The specified site for the transmission of STP/STD/LTD/LTP/Fa is the axon terminal, and only occurs when the axon terminal transmits excitation to other axon terminals.
        self.reset_cortex_props_to_initial_state(
            reset_inds=to_inds,
            include_props=[
                "Fa",
                "anti_Fa",
                #    'spine_active'
            ],
        )
        self.post_excite_2_each_cal_type_targ(spike_inds, to_inds, spike_excite)
        # self.axon_end_post_max_circuit_length(spike_inds)
        if CORTEX_OPTS["IS_MOCK_RECORD_PROPS"]:
            self.axon_end_post_spine_active(spike_inds, spike_excite)
            self.posterior_synapse_post_excite_to_spine(spike_inds)
            # self.axon_end_post_min_spine_active(spike_inds)
        self.axon_end_post_Fa(spike_inds, spike_excite)
        self.axon_end_post_Fa_multi(spike_inds, spike_excite)
        self.axon_end_post_anti_Fa(spike_inds, spike_excite)
        self.axon_end_post_STP(spike_inds, spike_excite)
        self.axon_end_post_STD(spike_inds, spike_excite)
        # self.axon_end_post_STD_multi(spike_inds, spike_excite)
        self.post_marker(spike_inds, spike_excite)

        self.update_refractory(spike_inds)
        self.cortex["is_active"][spike_inds] = 1

        # Neurons that were originally at resting potential and then received excitatory input that is lower than the resting potential are considered to have no change in state and do not participate in further calculations.
        below_ATP_to_mask = self.cortex["excite"][to_inds] < ATP
        excite_no_vary_to_inds_mask = in_RP_to_inds_mask * below_ATP_to_mask
        vary_to_inds = to_inds[~excite_no_vary_to_inds_mask]

        # Updating changes in neural synapses
        self.vary_axon_end_inds = set(
            np.compress(
                self.cortex["type"][vary_to_inds] == TYPE["axon_end"], vary_to_inds
            )
        )
        self.vary_axon_end_inds.update(will_recv_excite_spike_inds)
        self.vary_dendrite_inds.update(
            np.compress(
                (self.cortex["type"][vary_to_inds] >= list(DENDRITE_TYPE.values())[0])
                * (
                    self.cortex["type"][vary_to_inds]
                    <= list(DENDRITE_TYPE.values())[-1]
                ),
                vary_to_inds,
            )
        )
        self.vary_soma_inds.update(
            np.compress(self.cortex["type"][vary_to_inds] == TYPE["soma"], vary_to_inds)
        )
        self.vary_axon_inds.update(
            np.compress(self.cortex["type"][vary_to_inds] == TYPE["axon"], vary_to_inds)
        )

        self.write_cortex("spike_axon_end")

    def update_refractory(self, spike_inds):
        is_need_refractory_mask = self.cortex["bool_util"][: len(spike_inds)]
        is_need_refractory_mask[:] = (self.cortex["refractory"][spike_inds] == 1) * (
            self.cortex["tick_spike_times"][spike_inds] > 0
        )
        self.cortex["refractory"][spike_inds[is_need_refractory_mask]] = 2

        for release_type in ["excite", "Fa", "STP", "STD", "marker"]:
            is_need_refractory_mask = (
                (self.cortex["refractory"][spike_inds] == 1)
                * (self.cortex["tick_spike_times"][spike_inds] > 0)
                * (self.cortex[release_type][spike_inds] > (PRE_LTP_SUM_BASE * 0.1))
            )
            self.cortex["refractory"][spike_inds[is_need_refractory_mask]] = 2

    def get_excite_inds_with_no_recv_excite(self, nerve_type):
        spike_inds = self.get_excite_inds_by_type(nerve_type)
        return spike_inds[self.cortex["will_recv_excite"][spike_inds] == 0]

    def mark_will_recv_excite_with_nerve_inds(self, spike_inds):
        self.cortex["will_recv_excite"][:] = 0
        self.cortex["will_recv_excite"][self.cortex["post_ind"][spike_inds]] = 1

    def get_spike_excite(self, spike_inds):

        # Basic Pulse Excitation
        base_excite = (
            self.cortex["tick_spike_times"][spike_inds]
            * self.cortex["LTP"][spike_inds]
            * self.cortex["transmitter_release_sum"][spike_inds]
        )

        # Cells without pulses, taken from issuing excitement as pulse excitement
        no_spike_mask = self.cortex["bool_util"][: len(spike_inds)]
        no_spike_mask[:] = self.cortex["tick_spike_times"][spike_inds] == 0
        base_excite[no_spike_mask] = self.cortex["spontaneous_firing"][
            spike_inds[no_spike_mask]
        ]

        max_potentiation = np.maximum(
            np.maximum(
                self.cortex["STP"][spike_inds],
                self.cortex["Fa"][spike_inds],
            ),
            1,
        )
        max_depression = np.maximum(
            np.maximum(
                self.cortex["STD"][spike_inds],
                self.cortex["anti_Fa"][spike_inds],
            ),
            1,
        )

        return base_excite * max_potentiation / max_depression

    def dendrite_self_synaptic(self):
        dendrite_vals = list(DENDRITE_TYPE.values())
        self_synaptic_dendrite_inds = (
            (self.cortex["type"] >= dendrite_vals[0])
            * (self.cortex["type"] <= dendrite_vals[-1])
            * (self.cortex["self_synapse"] > 0)
        )
        self.cortex["excite"][self_synaptic_dendrite_inds] = self.cortex["excite"][
            self.cortex["soma_ind"][self_synaptic_dendrite_inds]
        ]

    def spike_dendrite_loop(self):
        self.mark_will_recv_excite_with_nerve_inds(list(self.vary_dendrite_inds))

        self.spike_dendrite()

        if len(self.vary_dendrite_inds):
            self.spike_dendrite_loop()
        else:
            self.vary_dendrite_inds.clear()

    def spike_dendrite(self):
        spike_inds = np.asarray(list(self.vary_dendrite_inds), "int")
        will_no_recv_excite_inds_mask = self.cortex["will_recv_excite"][spike_inds] == 0
        no_spike_inds = spike_inds[~will_no_recv_excite_inds_mask]
        spike_inds = spike_inds[will_no_recv_excite_inds_mask]
        to_inds = self.get(spike_inds, "post_ind")

        # When a postsynaptic neuron needs to receive excitation, all of its presynaptic neurons must be involved in the calculation, regardless of whether they themselves have experienced a change in state.
        self.cortex["float_util"][:] = 0
        self.cortex["float_util"][to_inds] = 1
        spike_inds = np.compress(
            (self.cortex["will_recv_excite"] == 0)
            * (self.cortex["float_util"][self.cortex["post_ind"]] == 1),
            self.cortex["ind"],
        )
        to_inds = self.get(spike_inds, "post_ind")

        self.set_spike_times_with_excite(spike_inds)
        spike_excite = self.get_spike_excite(spike_inds)

        in_RP_to_inds_mask = (
            self.cortex["excite"][to_inds] == self.cortex["RP"][to_inds]
        )

        self.reset_cortex_props_to_initial_state(
            reset_inds=to_inds, include_props=["excite"]
        )
        self.post_excite_2_each_cal_type_targ(spike_inds, to_inds, spike_excite)
        self.post_marker(spike_inds, spike_excite)

        self.cortex["is_active"][spike_inds] = 1

        below_ATP_to_mask = self.cortex["excite"][to_inds] < ATP

        excite_no_vary_to_inds_mask = in_RP_to_inds_mask * below_ATP_to_mask
        vary_to_inds = to_inds[~excite_no_vary_to_inds_mask]

        self.vary_dendrite_inds = set(
            np.compress(
                (self.cortex["type"][vary_to_inds] >= list(DENDRITE_TYPE.values())[0])
                * (
                    self.cortex["type"][vary_to_inds]
                    <= list(DENDRITE_TYPE.values())[-1]
                ),
                vary_to_inds,
            )
        )
        self.vary_dendrite_inds.update(no_spike_inds)
        self.vary_soma_inds.update(
            np.compress(self.cortex["type"][vary_to_inds] == TYPE["soma"], vary_to_inds)
        )

        self.write_cortex("spike_dendrite")

    def get_is_spine_mask(self, nerve_inds):
        is_spine_mask = self.cortex["bool_util"]
        is_spine_mask[:] = False
        is_spine_mask[self.get_all_spine_inds()] = True
        return is_spine_mask[nerve_inds]

    def post_excite_2_each_cal_type_targ(self, spike_inds, to_inds, spike_excite):
        spike_2_targ_mask = self.cortex["bool_util"][: len(spike_inds)]
        spike_2_targ_mask[:] = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["excite"]
        )

        # max
        post_max_mask = (
            spike_2_targ_mask * self.cortex["type"][to_inds] == TYPE["dendrite_max"]
        )
        self.post_excite(
            spike_inds[post_max_mask],
            to_inds[post_max_mask],
            spike_excite[post_max_mask],
            "max",
        )
        # min
        post_min_mask = (
            spike_2_targ_mask * self.cortex["type"][to_inds] == TYPE["dendrite_min"]
        )
        self.post_excite(
            spike_inds[post_min_mask],
            to_inds[post_min_mask],
            spike_excite[post_min_mask],
            "min",
        )
        # multi
        post_multi_mask = (
            spike_2_targ_mask * self.cortex["type"][to_inds] == TYPE["dendrite_multi"]
        )
        self.post_excite(
            spike_inds[post_multi_mask],
            to_inds[post_multi_mask],
            spike_excite[post_multi_mask],
            "multi",
        )
        # add
        post_add_mask = (
            spike_2_targ_mask * ~post_max_mask * ~post_min_mask * ~post_multi_mask
        )
        spike_excite[post_add_mask] *= self.cortex["post_sign"][
            spike_inds[post_add_mask]
        ]
        self.post_excite(
            spike_inds[post_add_mask],
            to_inds[post_add_mask],
            spike_excite[post_add_mask],
            "add",
        )

    def post_excite(self, spike_inds, to_inds, excite, post_type="add"):
        if not len(spike_inds):
            return
        if post_type == "add":
            self.post_excite_add(spike_inds, to_inds, excite)
        elif post_type == "max":
            self.post_excite_max(to_inds, excite)
        elif post_type == "min":
            self.post_excite_min(spike_inds, to_inds, excite)
        elif post_type == "multi":
            self.post_excite_multi(to_inds, excite)

    def post_excite_add(self, spike_inds, to_inds, excite):
        spike_nerve_type = self.cortex["type"][spike_inds[0]]
        if spike_nerve_type in [TYPE["axon_end"], *DENDRITE_TYPE.values()]:

            # 1. Excitation transmission is not all or nothing when it occurs first.
            all_or_none_mask = self.cortex["bool_util"][: len(spike_inds)]
            all_or_none_mask[:] = self.cortex["all_or_none"][spike_inds].astype(bool)
            np.add.at(
                self.cortex["excite"],
                np.array(to_inds, int)[~all_or_none_mask],
                excite.astype(int)[~all_or_none_mask],
            )

            # Based on the transmitted excitation, determining whether the all-or-none synapse should execute all-or-none excitation transmission.
            posted_excite = (
                excite + self.cortex["excite"][to_inds] - self.cortex["RP"][to_inds]
            )
            all_or_none_can_post_mask = self.cortex["bool_util"][: len(spike_inds)]
            all_or_none_can_post_mask[:] = (
                (np.sign(posted_excite) == self.cortex["post_sign"][spike_inds])
                | (
                    (np.sign(posted_excite) == 0)
                    * (self.cortex["all_or_none"][spike_inds] == 2)
                )
            ) * all_or_none_mask
            np.add.at(
                self.cortex["excite"],
                np.array(to_inds, int)[all_or_none_can_post_mask],
                excite.astype(int)[all_or_none_can_post_mask],
            )
        else:
            np.add.at(self.cortex["excite"], np.array(to_inds, int), excite.astype(int))

    def post_excite_max(self, to_inds, excite):
        np.maximum.at(
            self.cortex["excite"],
            np.array(to_inds, int),
            #   excite.astype(int) + NRP
            excite + self.cortex["RP"][to_inds],
        )

    def post_excite_min(self, spike_inds, to_inds, excite):
        """In order to prevent the post-synaptic target itself from being very low in excitement, which would prevent the transmission of excitement to reach its minimum,
        setting their excitement to maximum before transmission can result in the final excitement being the minimum value of pre-synaptic excitement.
        """
        origin_will_recv_excite = self.cortex["float_util"][: len(to_inds)]
        origin_will_recv_excite[:] = self.cortex["will_recv_excite"][to_inds]
        self.cortex["will_recv_excite"][to_inds] = 2
        self.cortex["excite"][to_inds] = np.Inf

        np.minimum.at(
            self.cortex["excite"], to_inds, excite + self.cortex["RP"][to_inds]
        )
        self.cortex["will_recv_excite"][to_inds] = origin_will_recv_excite

    def post_excite_multi(self, to_inds, excite):
        unique_to_inds = np.unique(to_inds)
        self.cortex["excite"][unique_to_inds] = np.maximum(
            1, self.cortex["excite"][unique_to_inds]
        )
        np.multiply.at(self.cortex["excite"], np.array(to_inds, int), excite)

    # def axon_end_post_max_circuit_length(self, spike_inds):
    #     spike_inds = spike_inds[self.cortex['LTP'][spike_inds] > 0]
    #     np.maximum.at(self.cortex['max_circuit_length'],
    #                   self.cortex['post_ind'][spike_inds],
    #                   self.cortex['max_circuit_length'][spike_inds] + 1)

    def update_max_circuit_length(self):
        posterior_synapse_slice = self.get_posterior_synapse_slice()
        alive_posterior_synapse_inds = self.cortex["ind"][posterior_synapse_slice][
            self.cortex["LTP"][posterior_synapse_slice] > 0
        ]
        np.maximum.at(
            self.cortex["max_circuit_length"],
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
                alive_posterior_synapse_inds
            ].astype(int),
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["ind_in_circuit"]][
                alive_posterior_synapse_inds
            ],
        )

    def all_posterior_synapse_post_anti_spine_active(self):
        all_posterior_synapse_slice = self.get_posterior_synapse_slice()
        np.add.at(
            self.cortex["anti_spine_active"],
            self.cortex["post_ind"][all_posterior_synapse_slice],
            self.cortex["LTP"][all_posterior_synapse_slice],
        )

    def all_posterior_synapse_post_max_pre_synapse_LTP(self):
        all_posterior_synapse_slice = self.get_posterior_synapse_slice()
        np.maximum.at(
            self.cortex["max_pre_synapse_LTP"],
            self.cortex["post_ind"][all_posterior_synapse_slice],
            self.cortex["LTP"][all_posterior_synapse_slice],
        )

    def axon_end_post_spine_active(self, spike_inds, spike_excite):
        spike_inds = spike_inds[self.cortex["LTP"][spike_inds] > 0]
        post_spine_active_value = self.get_post_spine_active_value(spike_inds)
        # np.add.at(
        #     self.cortex['spine_active'],
        #     self.cortex['post_ind'][spike_inds],
        #     post_spine_active_value,
        # )
        spine_inds = self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
            spike_inds
        ].astype(int)
        self.cortex["spine_active"][
            spine_inds[self.cortex["spine_active"][spine_inds] == -1]
        ] = np.inf
        np.minimum.at(
            self.cortex["spine_active"],
            spine_inds,
            post_spine_active_value,
        )
        self.write_cortex("axon_end_post_spine_active")

    def axon_end_post_min_spine_active(self, spike_inds):
        pass

    def get_post_spine_active_value(self, spike_inds):
        # anti_spine_active_ratio = np.maximum(
        #     0, self.cortex['anti_spine_active'][spike_inds] -
        #     self.cortex['spine_active'][spike_inds]) / np.maximum(
        #         1, self.cortex['anti_spine_active'][spike_inds])
        spine_active_ratio = self.get_spine_active_ratio_with_excite_and_LTP(spike_inds)
        post_spine_active_value = self.cortex["LTP"][spike_inds] * spine_active_ratio
        # * (1 - anti_spine_active_ratio)
        return post_spine_active_value

    def get_spine_active_ratio_with_excite_and_LTP(self, spike_inds):
        ratio_with_full_excite = (
            self.cortex["excite"][spike_inds] - self.cortex["RP"][spike_inds]
        ) / ABSTRACT_EXCITE
        ratio_with_max_LTP = (
            self.cortex["LTP"][spike_inds]
            / self.cortex["max_pre_synapse_LTP"][self.cortex["post_ind"][spike_inds]]
        )
        return np.minimum(1, ratio_with_full_excite / ratio_with_max_LTP)

    def axon_end_post_Fa(self, spike_inds, spike_excite):
        release_type_is_Fa_mask = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["Fa"]
        )
        to_inds = self.cortex["post_ind"][spike_inds[release_type_is_Fa_mask]]
        np.maximum.at(self.cortex["Fa"], to_inds, spike_excite[release_type_is_Fa_mask])

    def axon_end_post_Fa_multi(self, spike_inds, spike_excite):
        spike_inds = self.cortex["ind"][
            (self.cortex["release_type"] == RELEASE_TYPE["Fa_multi"])
        ]
        spike_excite = self.get_spike_excite(spike_inds)
        to_inds = self.cortex["post_ind"][spike_inds]
        # Avoid multiplying with 0, set all the Fa of the postsynaptic targets with Fa of 0 to 1.
        self.cortex["Fa"][to_inds] = 1
        np.multiply.at(self.cortex["Fa"], to_inds, spike_excite)

    def axon_end_post_anti_Fa(self, spike_inds, spike_excite):

        release_type_is_anti_Fa_mask = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["anti_Fa"]
        )
        to_inds = self.cortex["post_ind"][spike_inds[release_type_is_anti_Fa_mask]]

        # self.reset_calculate_props(to_inds, 'anti_Fa')

        np.maximum.at(
            self.cortex["anti_Fa"], to_inds, spike_excite[release_type_is_anti_Fa_mask]
        )

    def axon_end_post_STD(self, spike_inds, spike_excite):
        release_type_is_STD_mask = self.cortex["bool_util"][: len(spike_inds)]
        release_type_is_STD_mask[:] = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["STD"]
        )
        to_inds = self.cortex["post_ind"][spike_inds[release_type_is_STD_mask]]
        np.add.at(self.cortex["STD"], to_inds, spike_excite[release_type_is_STD_mask])

    def posterior_synapse_post_excite_to_spine(self, spike_inds):
        posterior_synapse_mask = self.cortex["is_synapse"][spike_inds] > 0
        spike_inds = spike_inds[posterior_synapse_mask]
        spine_inds = self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
            spike_inds
        ].astype(int)
        self.cortex[SPINE_EXINFO["min_excite"]][
            spine_inds[self.cortex[SPINE_EXINFO["min_excite"]][spine_inds] == -np.inf]
        ] = np.inf
        np.minimum.at(
            self.cortex[SPINE_EXINFO["min_excite"]],
            spine_inds,
            self.cortex["excite"][spike_inds],
        )

    def axon_end_post_STP(self, spike_inds, spike_excite):
        release_type_is_STD_mask = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["STP"]
        )
        to_inds = self.cortex["post_ind"][spike_inds[release_type_is_STD_mask]]
        np.maximum.at(
            self.cortex["STP"], to_inds, spike_excite[release_type_is_STD_mask]
        )

    def post_marker(self, spike_inds, spike_excite):
        release_type_is_marker_mask = self.cortex["bool_util"][: len(spike_inds)]
        release_type_is_marker_mask[:] = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["marker"]
        ) * (
            self.cortex["is_active"][spike_inds] == 0
        )  # Only inactive synapses can transmit markers to ensure that they are only transmitted once per frame.
        np.add.at(
            self.cortex["marker_remain"],
            self.cortex["post_ind"][spike_inds[release_type_is_marker_mask]],
            spike_excite[release_type_is_marker_mask],
        )

        release_type_is_marker_multi_mask = self.cortex["bool_util"][: len(spike_inds)]
        release_type_is_marker_multi_mask[:] = (
            self.cortex["release_type"][spike_inds] == RELEASE_TYPE["marker_multi"]
        ) * (
            self.cortex["is_active"][spike_inds] == 0
        )  # Only the synapses that have not been active can transmit markers, ensuring that they are only transmitted once in a frame.
        np.maximum.at(
            self.cortex["marker_remain"],
            self.cortex["post_ind"][spike_inds[release_type_is_marker_multi_mask]],
            1,
        )
        np.multiply.at(
            self.cortex["marker_remain"],
            self.cortex["post_ind"][spike_inds[release_type_is_marker_multi_mask]],
            spike_excite[release_type_is_marker_multi_mask],
        )

    def reduce_Fa_on_cycle_start(self):
        self.cortex["Fa"][:] = 1
        self.cortex["anti_Fa"][:] = 1

    def weaken_synapse(self):
        if CORTEX_OPTS["enable_posterior_form"] == 0:
            return

        self.weaken_synapse_by_post_synaptic_resource_limitation()

        # After weakening, the synapses that have decreased to 0 in LTP need to be labeled as dead and related synapses.
        self.mark_died_synapse()

        self.write_cortex("weaken_synapse")

    def get_posterior_synapse_slice(self):
        return slice(self.cortex_static_nerve_slice.stop, self.new_ind_start)

    def update_post_synapse_LTP_sum(self):
        posterior_synapse_slice = self.get_posterior_synapse_slice()
        self.cortex["post_synapse_LTP_sum"][: self.new_ind_start] = 0
        np.add.at(
            self.cortex["post_synapse_LTP_sum"],
            self.cortex["post_ind"][posterior_synapse_slice],
            self.cortex["LTP"][posterior_synapse_slice],
        )

    def weaken_synapse_by_post_synaptic_resource_limitation(self):
        cortex = self.cortex
        weaken_synapse_inds = self.get_synapse_inds_on_active_spines()

        if not len(weaken_synapse_inds):
            return

        # Recalculate the total amount of LTP on the postsynaptic membrane of all posterior synapses. The synapses with a total amount exceeding the limit on the postsynaptic membrane are the ones that need to be weakened.
        self.update_post_synapse_LTP_sum()

        # each_post_synapse_resource_sum = np.minimum(
        #     POST_SYNAPSE_RESOURCE_SUM,
        #     self.get_resource_limit_of_synapse(weaken_synapse_inds),
        # )
        each_post_synapse_resource_sum = np.full(
            len(weaken_synapse_inds), POST_SYNAPSE_RESOURCE_SUM
        )
        weaken_inds_mask = (
            cortex["post_synapse_LTP_sum"][
                cortex["post_ind"][weaken_synapse_inds]
            ].astype(int)
            > each_post_synapse_resource_sum
        )
        weaken_synapse_inds = weaken_synapse_inds[weaken_inds_mask]
        each_post_synapse_resource_sum = each_post_synapse_resource_sum[
            weaken_inds_mask
        ]

        if not len(weaken_synapse_inds):
            # self.cortex['post_synapse_max_increased_LTP'][:self.
            #                                               new_ind_start] = 0
            return

        cortex["float_util"][: self.new_ind_start] = 0
        np.add.at(
            cortex["float_util"],
            cortex["post_ind"][weaken_synapse_inds],
            1 / cortex["LTP"][weaken_synapse_inds],
        )
        weaken_LTP = np.minimum(
            cortex["LTP"][weaken_synapse_inds],
            # The total amount of LTP that the postsynaptic membrane needs to reduce
            (
                cortex["post_synapse_LTP_sum"][cortex["post_ind"][weaken_synapse_inds]]
                - each_post_synapse_resource_sum
            )
            *
            # The proportion of LTP that needs to be reduced for each pre-synaptic membrane
            (
                (1 / cortex["LTP"][weaken_synapse_inds])
                / cortex["float_util"][cortex["post_ind"][weaken_synapse_inds]]
            ),
        )

        # Reduce the LTP at each synapse.
        self.cortex["LTP"][weaken_synapse_inds] -= weaken_LTP

        self.weaken_synapse_by_post_synaptic_resource_limitation()

    def adjust_LTP_limit_of_each_stable_circuit(
        self, resource_limit_of_each_synapse=None
    ):
        cortex = self.cortex
        self.update_post_synapse_LTP_sum()
        to_adjust_synapse_inds = self.get_all_synapse_inds_on_spines(
            self.get_spine_inds_of_nowa_num()
        )

        resource_limit_of_each_synapse = (
            self.get_resource_limit_of_synapse(to_adjust_synapse_inds)
            if resource_limit_of_each_synapse == None
            else np.full(len(to_adjust_synapse_inds), resource_limit_of_each_synapse)
        )

        cortex["LTP"][to_adjust_synapse_inds] *= (
            resource_limit_of_each_synapse
            / self.cortex["post_synapse_LTP_sum"][
                self.cortex["post_ind"][to_adjust_synapse_inds]
            ]
        )

    def get_resource_limit_of_synapse(self, synapse_inds):
        return self.get_resource_limit_of_spine(
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][synapse_inds].astype(int)
        )

    def get_resource_limit_of_spine(self, spine_inds):
        max_circuit_length = self.cortex["max_circuit_length"][spine_inds]
        max_circuit_length[max_circuit_length == 0] = 1
        return (
            np.power(STANDARD_PREDICT_EXCITE, 1 / max_circuit_length)
            / POSTERIOR_SYNAPSE_TRANSMITTER_SUM
            * POST_SYNAPSE_RESOURCE_SUM
        )

    def get_synapse_inds_on_active_and_stable_spines(self):
        cortex = self.cortex

        has_marker_remain_spine_inds_of_nowa_num = (
            self.get_has_marker_remain_spine_inds_of_nowa_num()
        )

        #
        stable_spine_inds = has_marker_remain_spine_inds_of_nowa_num[
            self.get_stable_spine_mask(has_marker_remain_spine_inds_of_nowa_num)
        ]
        stable_spine_mask = cortex["bool_util"]
        stable_spine_mask[:] = False
        stable_spine_mask[stable_spine_inds] = True
        posterior_synapse_slice = self.get_posterior_synapse_slice()
        return cortex["ind"][posterior_synapse_slice][
            stable_spine_mask[
                cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
                    posterior_synapse_slice
                ].astype(int)
            ]
        ]

    def get_synapse_inds_on_active_spines(self):
        return self.get_all_synapse_inds_on_spines(
            self.get_has_marker_remain_spine_inds_of_nowa_num()
        )

    def get_synapse_inds_on_stable_spines_of_nowa_num(self):
        spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return self.get_all_synapse_inds_on_spines(
            spine_inds_of_nowa_num[self.get_stable_spine_mask(spine_inds_of_nowa_num)]
        )

    def get_stable_spine_inds_of_nowa_num(self):
        spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return spine_inds_of_nowa_num[
            self.get_stable_spine_mask(spine_inds_of_nowa_num)
        ]

    def get_stable_spine_inds(self):
        spine_inds = self.get_all_spine_inds()
        return spine_inds[self.get_stable_spine_mask(spine_inds)]

    def get_stable_spine_mask(self, spine_inds):
        posterior_synapse_slice = self.get_posterior_synapse_slice()
        posterior_synapse_ind = self.cortex["ind"][posterior_synapse_slice][
            self.cortex["LTP"][posterior_synapse_slice] > 0
        ]
        synapse_sum_on_spines = self.cortex["float_util"]
        synapse_sum_on_spines[: self.new_ind_start] = 0
        np.add.at(
            synapse_sum_on_spines,
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
                posterior_synapse_ind
            ].astype(int),
            1,
        )
        self.cortex["ind"][posterior_synapse_slice][
            self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]][
                posterior_synapse_slice
            ].astype(int)
            == 4779
        ]
        return (
            synapse_sum_on_spines[spine_inds]
            == self.cortex["max_circuit_length"][spine_inds]
        ) * (self.cortex["max_circuit_length"][spine_inds] != 0)

    def get_active_and_stable_spine_inds_of_nowa_num(self):
        active_spine_inds_of_nowa_num = self.get_active_spine_inds_of_nowa_num()
        return active_spine_inds_of_nowa_num[
            self.get_stable_spine_mask(active_spine_inds_of_nowa_num)
        ]

    def get_active_and_stable_spine_inds_out_of_nowa_num(self):
        all_spine_inds_out_of_nowa_num = self.get_all_spine_inds(
            [num for num in np.arange(10) if num != self.controller.get_active_num()]
        )
        return all_spine_inds_out_of_nowa_num[
            self.get_active_spine_mask(all_spine_inds_out_of_nowa_num)
            * self.get_stable_spine_mask(all_spine_inds_out_of_nowa_num)
        ]

    def get_active_and_stable_spine_inds_of_all_num(self):
        active_spine_inds_of_all_num = self.get_active_spine_inds_of_all_num()
        return active_spine_inds_of_all_num[
            self.get_stable_spine_mask(active_spine_inds_of_all_num)
        ]

    def get_has_marker_remain_and_stable_spine_inds_of_nowa_num(self):
        has_marker_remain_spine_inds_of_nowa_num = (
            self.get_has_marker_remain_spine_inds_of_nowa_num()
        )
        return has_marker_remain_spine_inds_of_nowa_num[
            self.get_stable_spine_mask(has_marker_remain_spine_inds_of_nowa_num)
        ]

    def get_has_marker_remain_spine_inds_of_nowa_num(self):
        all_spine_inds_of_nowa_num = self.get_spine_inds_of_nowa_num()
        return all_spine_inds_of_nowa_num[
            self.cortex["marker_remain"][all_spine_inds_of_nowa_num] > 0
        ]

    def get_max_LTP_link_on_spine(self, spine_ind, synapse_inds_on_this_spine=[]):
        synapse_inds_on_this_spine = (
            synapse_inds_on_this_spine
            if len(synapse_inds_on_this_spine)
            else self.get_all_synapse_inds_on_a_spine(spine_ind)
        )

        pre_synapse_inds = synapse_inds_on_this_spine[
            self.cortex["post_ind"][synapse_inds_on_this_spine] == spine_ind
        ]

        if len(pre_synapse_inds) == 0:
            pre_synapse_ind = None
        elif len(pre_synapse_inds) == 1:
            pre_synapse_ind = pre_synapse_inds[0]
        else:
            pre_synapse_ind = pre_synapse_inds[
                np.argmax(self.cortex["LTP"][pre_synapse_inds])
            ]

        return (
            [
                pre_synapse_ind,
                *self.get_max_LTP_link_on_spine(
                    pre_synapse_ind, synapse_inds_on_this_spine
                ),
            ]
            if pre_synapse_ind != None
            else []
        )

    def get_all_synapse_inds_on_a_spine(self, spine_ind):
        all_posterior_synapse_slice = self.get_posterior_synapse_slice()
        return self.cortex["ind"][all_posterior_synapse_slice][
            (self.cortex["exinfo_1"][all_posterior_synapse_slice] == spine_ind)
            * (self.cortex["LTP"][all_posterior_synapse_slice] > 0)
        ]

    def get_all_synapse_inds_on_spines(self, spine_inds):
        spine_mask = self.cortex["bool_util"]
        spine_mask[: self.new_ind_start] = False
        spine_mask[spine_inds] = True

        all_synapse_inds_on_spines = self.cortex["ind"][
            spine_mask[self.cortex[POSTERIOR_SYNAPSE_EXINFO["spine_ind"]].astype(int)]
        ]
        all_synapse_inds_on_spines = all_synapse_inds_on_spines[
            self.cortex["LTP"][all_synapse_inds_on_spines] > 0
        ]

        return all_synapse_inds_on_spines

    def mark_died_synapse(self):
        cortex = self.cortex
        posterior_synapse_slice = slice(
            self.cortex_static_nerve_slice.stop, self.new_ind_start
        )

        died_synapse_ind = cortex["ind"][posterior_synapse_slice][
            (cortex["LTP"][posterior_synapse_slice] != 0)
            * (
                # If the self LTP is less than the threshold and not equal to 0, it needs to be set to 0.
                (cortex["LTP"][posterior_synapse_slice] < DIED_LTP_THRESHOLD)
                |
                # It means that these synapses may have lost their function.
                # It is necessary to set LTP to 0 if it is indicated that the effective connection object has been lost.
                (
                    (
                        cortex["is_synapse"][
                            cortex["post_ind"][posterior_synapse_slice]
                        ]
                        != 0
                    )
                    * (cortex["LTP"][cortex["post_ind"][posterior_synapse_slice]] == 0)
                )
            )
        ]

        if len(died_synapse_ind):
            cortex["LTP"][died_synapse_ind] = 0
            self.mark_died_synapse()

    def reduce_excite(self, reduce_inds, reduce_excite):
        self.cortex["excite"][reduce_inds] = np.maximum(
            self.cortex["excite"][reduce_inds] - reduce_excite,
            self.cortex["RP"][reduce_inds],
        )

    def reduce_excite_with_tick_spike_times(self, reduce_inds, spike_times=[]):
        can_reduce_inds = reduce_inds[
            (self.cortex["self_synapse"][reduce_inds] == 0)
            | (self.cortex["type"][reduce_inds] != TYPE["soma"])
        ]
        spike_times = (
            self.cortex["tick_spike_times"][can_reduce_inds]
            if not len(spike_times)
            else spike_times
        )
        self.cortex["excite"][can_reduce_inds] -= (
            spike_times * -self.cortex["RP"][can_reduce_inds]
        )

    def get_inds_by_type(self, part_type):
        return self.cortex["ind"][self.cortex["type"] == part_type]

    def get_excite_inds_by_type(self, part_type):
        if isinstance(part_type, int):
            part_type = [part_type]
        # As long as the potential is higher than the minimum threshold, pulses will be emitted.
        if len(part_type) > 1:
            return np.compress(
                (self.cortex["type"] >= part_type[0])
                * (self.cortex["type"] <= part_type[-1])
                * (self.cortex["excite"] >= ATP),
                self.cortex["ind"],
            )
        else:
            return np.compress(
                (self.cortex["type"] == part_type[0]) * (self.cortex["excite"] >= ATP),
                self.cortex["ind"],
            )

    def leak_nerves_excite_to_rest_potential(self):
        cortex_slice = slice(self.new_ind_start)
        leak_mask = self.cortex["bool_util"][cortex_slice]
        leak_mask[:] = (self.cortex["excite"][cortex_slice] < ATP) * (
            self.cortex["self_synapse"][cortex_slice] == 0
        )
        self.cortex["excite"][cortex_slice][leak_mask] = self.cortex["RP"][
            cortex_slice
        ][leak_mask]

    def set_spike_times_with_excite(self, inds):
        self.set(
            inds,
            "tick_spike_times",
            np.maximum(
                0,
                np.round(
                    (self.get(inds, "excite") - self.get(inds, "RP"))
                    / abs(self.get(inds, "RP"))
                ),
            ),
        )

        # Based on the calculated tick_spike_times, reset excite to filter out some of the excitement that can be rounded off.
        self.cortex["excite"][inds] = self.cortex["tick_spike_times"][inds] * abs(
            self.cortex["RP"][inds]
        ) + self.get(inds, "RP")

        # Record the highest number of pulses in history.
        np.maximum.at(
            self.cortex["history_tick_spike_times"],
            inds,
            self.cortex["tick_spike_times"][inds],
        )

    def get(self, inds, prop):
        return self.cortex[prop][inds]

    def set(self, inds, prop, vals):
        self.cortex[prop][inds] = vals

    def get_write_cortex_info(self):
        info = {
            "region": {info["region_no"]: info for info in REGION.values()},
            "nerve_props_keys_map": PART_PROPS_KEYS_MAP,
            "cortex_static_part_slice_stop": int(self.cortex_static_part_slice.stop),
            "cortex_static_nerves_slice_stop": int(self.cortex_static_nerve_slice.stop),
            "cortex_slice_stop": int(self.new_ind_start),
            "nerve_marker_map": self.nerve_marker_map,
        }
        return info

    def get_save_posterior_inds(self):
        return np.concatenate(
            (
                self.get_all_spine_inds(),
                np.arange(self.cortex_static_nerve_slice.stop, self.new_ind_start),
            )
        )

    def write_cortex(self, desc=""):
        is_save = desc in [
            "save",
            "save_posterior",
        ]
        write_mode = desc if is_save else "history"
        if is_save:
            pass
        elif not is_can_write(self, desc):
            return

        cortex_info = self.get_write_cortex_info()
        write_props = STATIC_PROP_NAMES if is_save else WRITE_PART_PROPS
        if is_save:
            write_slice = {
                "save": slice(self.cortex_static_nerve_slice.stop),
                "save_posterior": self.get_save_posterior_inds(),
            }[desc]
        else:
            write_slice = CORTEX_OPTS["write_slice_lambda"](
                self, self.cortex, get_soma_inds, REGION, TYPE
            )
        cortex_info["write_slice_static_ind_stop"] = self.cortex_static_nerve_slice.stop
        cortex_info["write_slice_length"] = (
            write_slice.stop - (write_slice.start or 0)
            if isinstance(write_slice, slice)
            else len(write_slice)
        )
        print("[write_slice_length]", cortex_info["write_slice_length"])

        if desc == "save":
            cortex_info["spine_inds"] = self.get_all_spine_inds().tolist()
        cortex_matrix_map = {
            write_prop: self.cortex[write_prop][write_slice]
            for write_prop in write_props
        }

        write_n_read_cortex.write_cortex(
            self,
            cortex_info,
            cortex_matrix_map,
            desc=desc,
            write_mode=write_mode,
            suffix=self.mock_file_name or self.mnist_name,
        )

        # When writing history, it is necessary to also record the information of post-synaptic neurons.
        if not is_save and CORTEX_OPTS["enable_posterior_form"] == 1:
            self.save_cortex("save_posterior")

        if not is_save:
            self.write_cortex_tick += 1

    def get_soma_name(self, soma_ind):
        region = [
            region
            for region in REGION.values()
            if region["region_no"] == self.cortex["region_no"][soma_ind]
        ][0]
        neuron = [
            neuron
            for neuron in region["neurons"].values()
            if neuron["neuron_no"] == self.cortex["neuron_no"][soma_ind]
        ][0]
        return neuron["name"]


if __name__ == "__main__":
    cortex = Cortex()
    cortex.init()
