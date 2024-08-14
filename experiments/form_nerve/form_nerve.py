import numpy as np
from consts.nerve_props import PART_PROPS_MATRIX, TYPE, RELEASE_TYPE, SYNAPSE_TYPE, SPINE_EXINFO, POSTERIOR_SYNAPSE_EXINFO
from consts.nerve_params import LEARNING_RATE
from consts.feature import COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES
from experiments import REGION
import json


class FormNerve():

    def __init__(self):
        pass

    def make_new_nerve_packs(self,
                             mother_inds,
                             father_inds,
                             cortex_obj,
                             reset_nerve_props_lambda=None,
                             reset_nerve_props_matrix=[],
                             new_nerve_callback=None):
        self.spring_nerve_packs_in_common_way(
            cortex_obj,
            mother_inds,
            father_inds,
            new_nerve_callback=new_nerve_callback,
            reset_nerve_props_lambda=reset_nerve_props_lambda,
            reset_nerve_props_matrix=reset_nerve_props_matrix
            if len(reset_nerve_props_matrix) else [],
            is_posterior=0)

    def spring_nerve_packs_by_marker(self,
                                     mother_marker_inds,
                                     father_marker_inds,
                                     cortex_obj,
                                     synapse_type,
                                     pair_mask='all_pair',
                                     new_nerve_callback=None,
                                     reset_nerve_props_lambda=None,
                                     add_LTP_lambda=None,
                                     is_posterior=1):
        cortex = cortex_obj.cortex

        # Obtain the index of pre/post-synaptic cells.
        if pair_mask == 'all_pair':
            pair_mask = np.full(
                (len(mother_marker_inds), len(father_marker_inds)), True)
        pair_marker_inds_list = np.array(np.where(pair_mask))
        mother_inds = mother_marker_inds[pair_marker_inds_list[0]]
        father_inds = father_marker_inds[pair_marker_inds_list[1]]

        # Enhance existing synapses.
        new_nerves_existed_mask, new_nerves_existed_inds = self.get_existed_nerves_mask_with_new_nerves(
            cortex_obj, mother_inds, father_inds)
        firmed_existed_nerve_inds = self.firm_existed_nerves(
            cortex_obj,
            new_nerves_existed_inds,
            mother_inds[new_nerves_existed_mask],
            father_inds[new_nerves_existed_mask],
            new_nerve_callback=new_nerve_callback)

        # Create non-existing synapses.
        new_nerve_slice = self.spring_nerve_packs_in_common_way(
            cortex_obj,
            mother_inds[~new_nerves_existed_mask]
            if len(new_nerves_existed_mask) else mother_inds,
            father_inds[~new_nerves_existed_mask]
            if len(new_nerves_existed_mask) else father_inds,
            new_nerve_callback=new_nerve_callback,
            reset_nerve_props_lambda=reset_nerve_props_lambda,
            is_posterior=is_posterior,
            synapse_type=synapse_type)

        form_and_firm_nerve_inds = np.concatenate(
            (cortex['ind'][new_nerve_slice],
             firmed_existed_nerve_inds)).astype(int)

        cortex['is_synapse'][form_and_firm_nerve_inds] = 2

        # Allocate presynaptic resources, increase Long-Term Potentiation (LTP)
        if callable(add_LTP_lambda):
            add_LTP_lambda(cortex['ind'][new_nerve_slice],
                           firmed_existed_nerve_inds)

        # Updating the marker_remain of newly added and strengthened synapses.
        self.update_synapse_marker_remain(cortex_obj, form_and_firm_nerve_inds)

        is_STP_nerve_mask = cortex['release_type'][
            form_and_firm_nerve_inds] == RELEASE_TYPE['STP']
        is_STP_nerve_inds = form_and_firm_nerve_inds[is_STP_nerve_mask]

        # # The maximum increment of STP synaptic membrane LTP.
        # np.maximum.at(cortex['post_synapse_max_increased_LTP'],
        #               cortex['post_ind'][is_STP_nerve_inds],
        #               cortex['increased_LTP'][is_STP_nerve_inds])

        # is_not_STP_nerve_inds = form_and_firm_nerve_inds[~is_STP_nerve_mask]

        # # The maximum increment of synaptic membrane LTP.
        # np.maximum.at(cortex['post_synapse_max_increased_LTP'],
        #               cortex['post_ind'][is_not_STP_nerve_inds],
        #               cortex['increased_LTP'][is_not_STP_nerve_inds])

        # If after strengthening the synapse, there is a group or multiple groups of synapses with the exact same LTP at the same point, add 1 to the LTP of the first synapse in each group, giving it a weak competitive advantage.
        max_LTP_on_each_post_nerve = cortex['float_util']
        posterior_synapse_inds = cortex['ind'][
            cortex_obj.get_posterior_synapse_slice()]
        posterior_synapse_inds = posterior_synapse_inds[
            cortex['LTP'][posterior_synapse_inds] > 0]
        cortex['ind'][cortex['synapse_type'] > SYNAPSE_TYPE['static']]
        np.maximum.at(max_LTP_on_each_post_nerve,
                      cortex['post_ind'][posterior_synapse_inds],
                      cortex['LTP'][posterior_synapse_inds])
        max_LTP_posterior_synapse_inds = posterior_synapse_inds[
            cortex['LTP'][posterior_synapse_inds] ==
            max_LTP_on_each_post_nerve[cortex['post_ind']
                                       [posterior_synapse_inds]]]
        # Synapses that have conflicting prime numbers cannot be incremented by 1.
        # If the marker_exinfo of a synapse can be divided by the marker_exinfo of its own soma more than once, it means that there is a prime number conflict at the synapse.
        max_LTP_posterior_synapse_inds = max_LTP_posterior_synapse_inds[(
            cortex['exinfo_0'][max_LTP_posterior_synapse_inds] % np.power(
                cortex['exinfo_0'][cortex['soma_ind']
                                   [max_LTP_posterior_synapse_inds]], 2)) != 0]
        # Only if there are multiple identical maximum values, the first maximum value will be incremented by 1.
        _, unique_inds, unique_counts = np.unique(
            cortex['post_ind'][max_LTP_posterior_synapse_inds],
            return_index=True,
            return_counts=True)
        unique_inds = unique_inds[unique_counts > 1]
        unique_max_LTP_posterior_synapse_inds = max_LTP_posterior_synapse_inds[
            unique_inds]
        if len(unique_max_LTP_posterior_synapse_inds):
            cortex['LTP'][unique_max_LTP_posterior_synapse_inds] += 1

        return new_nerve_slice, firmed_existed_nerve_inds

    # Allocate presynaptic resources to strengthen or create new synapses.
    def add_LTP_with_form_and_firm_nerve_inds(self, cortex_obj,
                                              form_and_firm_nerve_inds,
                                              appear_or_disappear):
        cortex_obj.write_cortex('before_add_LTP')
        cortex = cortex_obj.cortex
        form_and_firm_nerve_inds = np.asarray(form_and_firm_nerve_inds, int)

        # Synapses that already have similar abstract cells (prime number conflict) on the link cannot obtain an increase in LTP.
        can_add_LTP_mask = (np.maximum(
            1, cortex['exinfo_0'][cortex['post_ind'][form_and_firm_nerve_inds]]
        ).astype(int) % cortex['exinfo_0'][
            cortex['soma_ind'][form_and_firm_nerve_inds]].astype(int) != 0) | (
                cortex['exinfo_0'][cortex['pre_ind'][form_and_firm_nerve_inds]]
                == 0)

        nerve_LTPs = cortex['LTP'][form_and_firm_nerve_inds]

        # Synapses of prime number conflicts, when competing for resources before the synaptic contest, need to borrow LTP from the postsynaptic object to increase their competitiveness due to their own LTP being 0.
        # Synapses with prime number conflicts must participate in competition, but in the end they will not actually increase LTP.
        # nerve_LTPs[~can_add_LTP_mask] = cortex['LTP'][cortex['post_ind'][form_and_firm_nerve_inds[~can_add_LTP_mask]]]
        nerve_LTPs[~can_add_LTP_mask] = 1
        # Synapses with LTP below HELP_COMPETITION_MIN_LTP cannot benefit from their own LTP in synaptic resource competition.
        HELP_COMPETITION_MIN_LTP = 50
        nerve_LTPs = np.maximum(
            1, np.round(nerve_LTPs / HELP_COMPETITION_MIN_LTP, 5))

        # # Translation: Calculate the competitive strength of each synapse for presynaptic resources = marker_remain of postsynaptic object * its own LTP * the activity of dendritic spines in the corresponding pathway.
        # synapse_competition_force = cortex['dopamine_remain'][
        #     cortex['post_ind'][form_and_firm_nerve_inds]] * nerve_LTPs
        # if appear_or_disappear == 'appear':
        #     spine_active = np.power(
        #         cortex['dopamine_remain'][cortex['exinfo_1'][
        #             form_and_firm_nerve_inds].astype(int)], 2)
        #     synapse_competition_force *= spine_active
        # # / (
        # #     max_pre_synapse_LTP_on_post_synapse_nerve /
        # #     cortex['LTP'][form_and_firm_nerve_inds])
        # ''' TODO If a point already has strong synapses, the probability of obtaining WTA for other synapses is smaller, so more synaptic resources should be allocated.
        #     Moving to smaller point positions of competition is a smarter move for each cell, and overall it can also accelerate the speed of establishing synaptic connections.
        # '''
        # # / np.maximum(
        # #     np.power(
        # #         (max_pre_synapse_LTP_on_post_synapse_nerve -
        # #          cortex['LTP'][form_and_firm_nerve_inds]) *
        # #         (max_pre_synapse_LTP_on_post_synapse_nerve >
        # #          100),  # When there are adjacent synapses with LTP greater than 100, the resistance to the enhanced LTP and the difference with the maximum LTP received are directly proportional.
        # #         1 / 3),
        # #     1)
        # # synapse_competition_force = np.power(synapse_competition_force, 1.5)
        # synapse_competition_force = np.power(synapse_competition_force, 3)

        # # Translate: transfer the dopamine_remain of the postsynaptic object + its own LTP to the presynaptic cell.
        # pre_synapse_source_competition_stress = cortex['float_util']
        # pre_synapse_source_competition_stress[:] = 0
        # np.add.at(
        #     pre_synapse_source_competition_stress,
        #     # The competition is for resources on the same cell, so it needs to be directed towards soma_ind.
        #     cortex['soma_ind'][form_and_firm_nerve_inds],
        #     synapse_competition_force,
        # )

        # The synaptic resources allocated to each synapse = (its own LTP + dopamine_remain of the postsynaptic object) proportion of the total presynaptic competitive pressure * total amount of presynaptic resources
        # synapse_competition_force_ratio = synapse_competition_force / pre_synapse_source_competition_stress[
        #     cortex['soma_ind'][form_and_firm_nerve_inds]]
        # debug
        synapse_competition_force_ratio = 1
        ENLARGE_ADD_LTP_RATIO = 100
        add_LTP_value = ENLARGE_ADD_LTP_RATIO * cortex['marker_remain'][
            cortex['pre_ind']
            [form_and_firm_nerve_inds]] * synapse_competition_force_ratio
        max_add_LTP_value = cortex['float_util']
        np.maximum.at(max_add_LTP_value,
                      cortex['post_ind'][form_and_firm_nerve_inds],
                      add_LTP_value)
        MAX_ADD_LTP_VALUE = 100
        add_LTP_ratio = cortex['float_util']
        add_LTP_ratio[
            cortex['post_ind'][form_and_firm_nerve_inds]] = np.minimum(
                1, MAX_ADD_LTP_VALUE /
                max_add_LTP_value[cortex['post_ind'][form_and_firm_nerve_inds]]
            )
        # Reduce the increment of STP synapses, so that stable STP synapses are at a disadvantage when competing with stable facilitation synapses, and can only outcompete unstable facilitation synapses.
        synapse_is_STP_mask = cortex['exinfo_1'][
            cortex['pre_ind'][form_and_firm_nerve_inds]] == SYNAPSE_TYPE['STP']
        add_LTP_ratio[cortex['post_ind'][form_and_firm_nerve_inds]
                      [synapse_is_STP_mask]] /= 2
        cortex['LTP'][
            form_and_firm_nerve_inds] += add_LTP_value * add_LTP_ratio[
                cortex['post_ind'][form_and_firm_nerve_inds]]

        # Finally, the LTP of the synapses that cannot be strengthened will be forcibly set to 0.
        cortex['LTP'][form_and_firm_nerve_inds[~can_add_LTP_mask]] = 0

        cortex_obj.write_cortex('add_LTP')

    def get_existed_nerves_mask_with_new_nerves(self, cortex_obj, mother_inds,
                                                father_inds):
        cortex = cortex_obj.cortex
        all_dynamic_nerves_slice = slice(
            cortex_obj.cortex_static_nerve_slice.stop,
            cortex_obj.new_ind_start)

        # Conduct a floating utility analysis.
        cortex['float_util'][all_dynamic_nerves_slice] = 0.

        # Translation: Synapse +1 for active pre-synaptic object
        cortex['bool_util'][:] = False
        cortex['bool_util'][mother_inds] = True
        cortex['float_util'][all_dynamic_nerves_slice][cortex['bool_util'][
            cortex['pre_ind'][all_dynamic_nerves_slice]] == True] += 1.

        # Translation: Synapse +1 for the active post-synaptic object
        cortex['bool_util'][:] = False
        cortex['bool_util'][father_inds] = True
        cortex['float_util'][all_dynamic_nerves_slice][cortex['bool_util'][
            cortex['post_ind'][all_dynamic_nerves_slice]] == True] += 1.

        # The final count of synapses with a final count of 2 is a pre-existing synapse.
        new_nerves_existed_inds = cortex['ind'][all_dynamic_nerves_slice][
            cortex['float_util'][all_dynamic_nerves_slice] == 2.]
        new_nerves_existed_inds = new_nerves_existed_inds[
            cortex['LTP'][new_nerves_existed_inds] != 0]

        unique_mother_inds = np.unique(mother_inds)
        unique_father_inds = np.unique(father_inds)
        cortex['int_util'][unique_mother_inds] = np.arange(
            len(unique_mother_inds))
        cortex['float_util'][unique_father_inds] = np.arange(
            len(unique_father_inds))
        new_nerves_existed_inds_matrix = np.zeros(
            (len(unique_mother_inds), len(unique_father_inds)), int)
        new_nerves_existed_inds_matrix[
            cortex['int_util'][cortex['pre_ind'][new_nerves_existed_inds]],
            cortex['float_util'][cortex['post_ind'][new_nerves_existed_inds]].
            astype(int)] = new_nerves_existed_inds
        new_nerves_existed_inds_list = new_nerves_existed_inds_matrix[
            cortex['int_util'][mother_inds],
            cortex['float_util'][father_inds].astype(int)]
        new_nerves_existed_mask = new_nerves_existed_inds_list != 0
        new_nerves_existed_inds = new_nerves_existed_inds_list[
            new_nerves_existed_mask]

        form_or_firm_nerves_sum = len(mother_inds)
        form_nerve_sum = np.sum(~new_nerves_existed_mask)
        firm_nerve_sum = len(new_nerves_existed_inds)
        assert form_or_firm_nerves_sum == form_nerve_sum + firm_nerve_sum, f'[get_existed_nerves_mask_with_new_nerves][nerve length error] {form_or_firm_nerves_sum} {form_nerve_sum} {firm_nerve_sum}'

        return new_nerves_existed_mask, new_nerves_existed_inds

    def firm_existed_nerves(self,
                            cortex_obj,
                            new_nerves_existed_inds,
                            mother_inds,
                            father_inds,
                            new_nerve_callback=None):
        if not len(new_nerves_existed_inds):
            return []

        cortex = cortex_obj.cortex
        new_nerves_existed_inds = np.asarray(new_nerves_existed_inds)

        # The only enhancing unpotentiated synapses.
        can_be_firm_nerve_mask = cortex['is_synapse'][
            new_nerves_existed_inds] == 1
        new_nerves_existed_inds = new_nerves_existed_inds[
            can_be_firm_nerve_mask]
        mother_inds = mother_inds[can_be_firm_nerve_mask]
        father_inds = father_inds[can_be_firm_nerve_mask]

        # Record the marker_remain before the reinforcement, for future calculations of the increment of marker_remain.
        self.update_synapse_marker_remain(cortex_obj, new_nerves_existed_inds)

        if callable(new_nerve_callback):
            new_nerve_callback(new_nerves_existed_inds, cortex_obj)

        return new_nerves_existed_inds

    def get_form_or_firm_LTP_values(self, cortex_obj, mother_inds, father_inds,
                                    form_or_firm_nerve_inds):
        cortex = cortex_obj.cortex

        # marker_exinfo1 contains the index of each synapse targeted by a number.
        form_or_firm_LTP_values = LEARNING_RATE * cortex['marker_remain'][
            mother_inds] * (cortex['dopamine_remain'][
                cortex['exinfo_1'][form_or_firm_nerve_inds].astype(int)])

        return form_or_firm_LTP_values

    def update_synapse_marker_remain(self, cortex_obj, synapse_inds):
        cortex = cortex_obj.cortex
        cortex['tick_spike_times'][synapse_inds] = cortex['tick_spike_times'][
            cortex['pre_ind'][synapse_inds]]
        cortex_obj.add_marker_remain(synapse_inds)

        cortex['dopamine_remain'][synapse_inds] = cortex['marker_remain'][
            synapse_inds]

    def spring_nerve_packs_in_common_way(
        self,
        cortex_obj,
        mother_inds,
        father_inds,
        new_nerve_callback=None,
        reset_nerve_props_lambda=None,
        reset_nerve_props_matrix=[],
        is_posterior=0,
        synapse_type=SYNAPSE_TYPE['static'],
    ):
        mother_inds = np.asarray(mother_inds)
        father_inds = np.asarray(father_inds)
        cortex = cortex_obj.cortex
        avaliable_parents_mask = (mother_inds != 0) * (father_inds != 0)
        # mother_inds = mother_inds[avaliable_inds_mask]
        # father_inds = father_inds[avaliable_inds_mask]

        # if not len(mother_inds) or not len(father_inds):
        #     return []
        assert len(mother_inds) == len(father_inds) and len(mother_inds)>0

        new_nerve_inds = self.get_new_nerve_inds(cortex_obj, is_posterior,
                                                 mother_inds, father_inds,
                                                 avaliable_parents_mask)

        cortex_obj.new_ind_start += np.sum(new_nerve_inds != 0)

        inherit_props_from_mother = [
            'region_no',
            'col_no',
            'region_row_no',
            'region_hyper_col_no',
            'hyper_col_ind',
            'mini_col_ind',
            'neuron_no',
            'RP',
            'transmitter_release_sum',
            'post_sign',
            'release_type',
            'all_or_none',
            'refractory',
            'mother_neuron_no',
            'spontaneous_firing',
            'soma_ind',
        ]

        for prop in PART_PROPS_MATRIX.dtype.names:
            cortex[prop][new_nerve_inds] = cortex[prop][
                mother_inds] if prop in inherit_props_from_mother else PART_PROPS_MATRIX[
                    prop][TYPE['axon_end']]
        # The pre-ind and post-ind of the synapse directly connected to the parent source are the ind of the parent source.
        cortex['pre_ind'][new_nerve_inds] = cortex['ind'][mother_inds]
        cortex['post_ind'][new_nerve_inds] = cortex['ind'][father_inds]
        cortex['mother_type'][new_nerve_inds] = cortex['type'][mother_inds]
        cortex['father_type'][new_nerve_inds] = cortex['type'][father_inds]
        cortex['ind'][new_nerve_inds] = new_nerve_inds
        cortex['father_region_no'][new_nerve_inds] = cortex['region_no'][
            father_inds]
        cortex['produce_marker_per_spike'][new_nerve_inds] = cortex[
            'child_produce_marker_per_spike'][mother_inds]

        parent_markers = np.unique(np.asarray(
            [cortex['marker'][mother_inds], cortex['marker'][father_inds]]).T,
                                   axis=0)
        for parent_marker in parent_markers:
            parent_marker = str(list(parent_marker))
            if not cortex_obj.nerve_marker_map.get(parent_marker):
                cortex_obj.nerve_marker_map[
                    parent_marker] = cortex_obj.new_marker_start
                cortex_obj.new_marker_start += 1
        cortex['marker'][new_nerve_inds] = [
            cortex_obj.nerve_marker_map[str([mother_marker, father_marker])]
            for mother_marker, father_marker in zip(
                cortex['marker'][mother_inds], cortex['marker'][father_inds])
        ]

        if len(reset_nerve_props_matrix):
            # reset_nerve_props_matrix = np.asarray(
            #     reset_nerve_props_matrix)[avaliable_inds_mask]
            reset_nerve_props_matrix = np.asarray(reset_nerve_props_matrix)
            reset_props = reset_nerve_props_matrix.dtype.names
            for reset_prop in reset_props:
                cortex[reset_prop][new_nerve_inds] = reset_nerve_props_matrix[
                    reset_prop]

        if callable(reset_nerve_props_lambda):
            reset_nerve_props_lambda(cortex_obj, new_nerve_inds, mother_inds,
                                     father_inds)

        # According to the fundamental theorem of arithmetic, the product of the marker_exinfo primes of the presynaptic and postsynaptic cells is used to accumulate the information of all synapses on this pathway, thus avoiding the formation of a cycle loop.
        if is_posterior == 2:
            ''' marker_exinfo can only be accumulated in the easy linkage, it cannot be used to prevent the establishment of STP synapse.
                Therefore, the newly established STP synapse cannot use the multiplication of the marker_remain of the presynaptic object and the marker_remain of the postsynaptic object as its own marker_remain.
            '''
            new_nerve_is_not_link_start_inds = new_nerve_inds[
                cortex['exinfo_0'][cortex['pre_ind'][new_nerve_inds]] == 1]
            cortex['exinfo_0'][new_nerve_inds] = cortex['exinfo_0'][
                cortex['soma_ind'][mother_inds]]
            cortex['exinfo_0'][new_nerve_is_not_link_start_inds] *= np.maximum(
                1, cortex['exinfo_0'][cortex['post_ind']
                                      [new_nerve_is_not_link_start_inds]])

            self.set_new_synapse_ind_in_circuit(cortex, new_nerve_inds)

        cortex['synapse_type'][new_nerve_inds] = synapse_type

        if callable(new_nerve_callback):
            new_nerve_callback(new_nerve_inds, cortex_obj)

        print('[form_nerve]', len(new_nerve_inds))

        return new_nerve_inds

    def get_new_nerve_inds(self, cortex_obj, is_posterior, mother_inds,
                           father_inds, avaliable_parents_mask):
        cortex = cortex_obj.cortex

        if is_posterior > 0:
            posterior_synapse_slice = slice(
                cortex_obj.cortex_static_nerve_slice.stop,
                cortex_obj.new_ind_start)
            new_nerves_sum = len(mother_inds)
            died_synapse_inds = cortex['ind'][posterior_synapse_slice][
                cortex['LTP'][posterior_synapse_slice] == 0][:new_nerves_sum]
            dying_synapse_sum = len(died_synapse_inds)
            new_nerves_sum = max(0, len(mother_inds) - dying_synapse_sum)
            new_nerve_slice_stop = cortex_obj.new_ind_start + new_nerves_sum
            new_nerve_inds = np.array([
                *died_synapse_inds,
                *range(cortex_obj.new_ind_start, new_nerve_slice_stop),
            ])
        else:
            # When one parent is absent (ind=0), their synapses also do not exist, and ind is also 0
            new_nerve_inds = np.zeros(len(mother_inds))
            new_nerve_inds[avaliable_parents_mask] = np.arange(
                cortex_obj.new_ind_start,
                cortex_obj.new_ind_start + np.sum(avaliable_parents_mask))

        return new_nerve_inds.astype(int)

    def set_new_synapse_ind_in_circuit(self, cortex, new_nerve_slice):
        new_nerve_inds = cortex['ind'][new_nerve_slice]
        post_nerve_is_synapse_mask = cortex['synapse_type'][
            cortex['post_ind'][new_nerve_slice]] > 1
        cortex[POSTERIOR_SYNAPSE_EXINFO['ind_in_circuit']][
            new_nerve_inds[post_nerve_is_synapse_mask]] = cortex[
                POSTERIOR_SYNAPSE_EXINFO['ind_in_circuit']][cortex['post_ind'][
                    new_nerve_inds[post_nerve_is_synapse_mask]]] + 1
        cortex[POSTERIOR_SYNAPSE_EXINFO['ind_in_circuit']][
            new_nerve_inds[~post_nerve_is_synapse_mask]] = 1


form_nerve = FormNerve()
