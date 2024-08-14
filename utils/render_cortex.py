import numpy as np
from experiments import REGION
from consts.nerve_props import TYPE, STATIC_TYPES, PART_PROPS, DENDRITE_TYPE
from consts.experiment import CORTEX_OPTS


class RenderCortex():

    def __init__(self, write_n_read_cortex):
        self.write_n_read_cortex = write_n_read_cortex
        self.frontend_options = {}
        self.old_frontend_options = {}
        self.CYCLE_R = 3
        self.REGION_SPACE_Y = 100
        self.set_frontend_layout_with_options()
        self.NERVE_W = 1
        self.PADDING = {
            'top': 100,
            'bottom': 100,
            'left': 400,
            'right': 1000,
        }
        self.OUT_OF_VIEWPORT_Y_POS = -999999

    def slice_matrix(self, matrix_map, slice_or_inds):
        return {
            prop: matrix_map[prop][slice_or_inds]
            for prop in matrix_map.keys()
        }

    def set_frontend_layout_with_options(self):
        if self.frontend_options.get('layoutSize') == 'small':
            self.col_w = 20
            self.neuron_space_y = 20
            self.col_space_y = 20
            self.col_space_x = int(self.col_w * 1.2)
            self.hyper_col_space_x = int(self.col_space_x * 1.5)
        elif self.frontend_options.get('layoutSize') == 'extreme_small':
            self.col_w = 5
            self.neuron_space_y = 5
            self.col_space_y = 5
            self.col_space_x = self.col_w
            self.hyper_col_space_x = self.col_space_x
        else:
            self.col_w = 40
            self.neuron_space_y = 40
            self.col_space_y = 40
            self.col_space_x = int(self.col_w * 1.2)
            self.hyper_col_space_x = int(self.col_space_x * 1.5)

    def update_frontend_options(self, options):
        if options == self.frontend_options: return
        self.old_frontend_options = self.frontend_options
        self.frontend_options = options
        # 1
        self.set_frontend_layout_with_options()
        # 2
        self.update_render_range_and_pos()

    def update_render_range_and_pos(self):
        if self.frontend_options.get('isShowPinnedSomaCircuit') == True:
            self.pinned_circuit_somas = self.get_pinned_circuit_somas()
        # self.update_region_range_info()
        # self.update_all_static_part_pos_matrix(self.write_n_read_cortex.cortex)

    def update_region_range_info(self):
        self.region_range_matrix, self.region_range_map = self.get_region_range_matrix(
        )

    def update_all_static_part_pos_matrix(self, cortex):
        cortex_info = self.write_n_read_cortex.cortex_info
        all_static_part = {
            prop: cortex[prop][:cortex_info['cortex_static_part_slice_stop']]
            for prop in PART_PROPS.keys()
        }
        self.all_static_part_pos_matrix = self.get_static_part_pos_with_matrix(
            all_static_part)

    def get_region_range_matrix(self):
        region_range_matrix = []
        region_range_map = {}
        region_pos_start_y = 0
        matrix_dtype = [('x_start', 'int'), ('x_end', 'int'),
                        ('y_start', 'int'), ('y_end', 'int'), ('col_h', 'int'),
                        ('hyper_col_w', 'int')]
        region_offset_x = 0

        for region in REGION.values():
            if self.frontend_options.get('isShowPinnedSomaCircuit'):
                is_hide_this_region = (
                    region['region_no']
                    not in self.pinned_circuit_somas['region_no']) | (
                        region['region_name'] in self.frontend_options.get(
                            'hideRegions', []))
                option_neuron_nos = self.pinned_circuit_somas['neuron_no'][
                    self.pinned_circuit_somas['region_no'] ==
                    region['region_no']]
                col_h = len(option_neuron_nos) * self.neuron_space_y
            else:
                is_hide_this_region = (region['region_name']
                                       in self.frontend_options.get(
                                           'hideRegions', []))
                option_neuron_nos = self.frontend_options.get(
                    'highlightStaticPart', {}).get(region['region_name'], [])
                col_h = (len(option_neuron_nos)
                         or region['static_part_sum_in_mini_col']
                         ) * self.neuron_space_y
            h, w, ww = region['region_shape']
            hyper_col_w = ww * self.col_w + (ww - 1) * self.col_space_x
            region_pos_end_y = region_pos_start_y + h * col_h + (
                h - 1) * self.col_space_y
            region_range_keys = [v[0] for v in matrix_dtype]
            x_for_each_hyper_col = [
                int((col_i * (hyper_col_w + self.hyper_col_space_x) +
                     self.PADDING['left']) + region_offset_x)
                for col_i in range(w)
            ]
            y_for_each_row = [
                int(region_pos_start_y + row_i * (col_h + self.col_space_y) +
                    self.PADDING['top']) for row_i in range(h)
            ] if not is_hide_this_region else [self.OUT_OF_VIEWPORT_Y_POS] * h
            region_range_vals = (
                x_for_each_hyper_col[0],  # x_start
                x_for_each_hyper_col[-1] + hyper_col_w,  # x_end
                y_for_each_row[0],  # y_start
                y_for_each_row[-1] + col_h,  # y_end
                col_h,  # col_h
                hyper_col_w,  # hyper_col_w
            )
            region_range_matrix.append(region_range_vals)
            region_range_map[region['region_name']] = dict(
                {
                    key: val
                    for key, val in zip(region_range_keys, region_range_vals)
                }, **{
                    'x_for_each_hyper_col': x_for_each_hyper_col,
                    'y_for_each_row': y_for_each_row,
                })
            if not is_hide_this_region:
                region_pos_start_y = region_pos_end_y + self.REGION_SPACE_Y
                region_offset_x *= 2
        region_range_matrix = np.array(region_range_matrix).T
        region_range_matrix = {
            prop: np.array(region_range_matrix[ind], dtype)
            for ind, (prop, dtype) in enumerate(matrix_dtype)
        }
        return region_range_matrix, region_range_map

    def get_static_part_pos_with_matrix(self, static_part_matrix):
        region_range_matrix = {
            prop:
            self.region_range_matrix[prop][static_part_matrix['region_no'] - 1]
            for prop in self.region_range_matrix.keys()
        }
        pos_matrix = np.zeros(len(static_part_matrix['type']),
                              dtype=[('x', 'int'), ('y', 'int')])
        pos_matrix['x'] = region_range_matrix['x_start']
        pos_matrix['x'] += (static_part_matrix['region_hyper_col_no'] - 1) * (
            region_range_matrix['hyper_col_w'] + self.hyper_col_space_x)
        pos_matrix['x'] += (static_part_matrix['mini_col_ind'] -
                            1) * (self.col_space_x + self.col_w)
        pos_matrix['y'] = region_range_matrix['y_start']
        pos_matrix['y'] += (static_part_matrix['region_row_no'] -
                            1) * region_range_matrix['col_h']
        pos_matrix['y'] += (static_part_matrix['region_row_no'] -
                            1) * self.col_space_y
        for region in REGION.values():
            this_region_neuron_inds = static_part_matrix['ind'][
                static_part_matrix['region_no'] == region['region_no']]
            all_neuron_nos = np.array(
                [neuron['neuron_no'] for neuron in region['neurons'].values()])
            if self.frontend_options.get('isShowPinnedSomaCircuit'):
                option_neuron_nos = self.pinned_circuit_somas['neuron_no'][
                    self.pinned_circuit_somas['region_no'] ==
                    region['region_no']]
                can_render_neuron_mask = np.isin(
                    all_neuron_nos,
                    option_neuron_nos) if len(option_neuron_nos) else np.full(
                        len(region['neurons']), False)
            else:
                option_neuron_nos = self.frontend_options.get(
                    'highlightStaticPart', {}).get(region['region_name'], [])
                can_render_neuron_mask = np.isin(
                    all_neuron_nos,
                    option_neuron_nos) if len(option_neuron_nos) else np.full(
                        len(region['neurons']), True)
            render_neuron_ind = np.arange(np.sum(can_render_neuron_mask))
            can_render_neuron_inds = this_region_neuron_inds[tuple([
                np.tile(can_render_neuron_mask,
                        region['mini_col_sum_in_region'])
            ])]
            pos_matrix['x'][can_render_neuron_inds] += self.col_w * (np.tile(
                render_neuron_ind, region['mini_col_sum_in_region']) % 2)
            pos_matrix['y'][can_render_neuron_inds] += np.tile(
                render_neuron_ind,
                region['mini_col_sum_in_region']) * self.neuron_space_y
            ''' By setting the coordinates of the neurons that do not need to be rendered directly outside the viewport, rendering filtering can be indirectly implemented. '''
            pos_matrix['y'][this_region_neuron_inds[tuple([
                np.tile(~can_render_neuron_mask,
                        region['mini_col_sum_in_region'])
            ])]] = self.OUT_OF_VIEWPORT_Y_POS
        return pos_matrix

    def get_static_part_pos_with_inds(self, static_part_inds):
        return self.all_static_part_pos_matrix[static_part_inds]

    def get_nerve_pos_matrix(self, nerve_inds, slice_cortex_matrix):
        cortex = self.write_n_read_cortex.cortex

        pos_matrix = {
            prop: np.zeros(len(nerve_inds), dtype)
            for prop, dtype in [
                ('from_x', 'int'),
                ('from_y', 'int'),
                ('to_x', 'int'),
                ('to_y', 'int'),
                ('x', 'int'),
                ('y', 'int'),
            ]
        }

        father_is_static_part_mask = np.isin(cortex['father_type'][nerve_inds],
                                             STATIC_TYPES)

        pos_matrix = self.init_from_and_to_pos_with_parents(
            pos_matrix, nerve_inds, slice_cortex_matrix,
            father_is_static_part_mask)
        pos_matrix = self.set_nerve_from_and_to_pos_with_cycle_r(
            pos_matrix, father_is_static_part_mask)
        pos_matrix = self.set_nerve_pos_with_from_and_to_pos(pos_matrix)

        return pos_matrix

    def init_from_and_to_pos_with_parents(self, pos_matrix, nerve_inds,
                                          slice_cortex_matrix,
                                          father_is_static_part_mask):
        cortex = self.write_n_read_cortex.cortex

        # The location of the presynaptic cell serves as the starting point.
        mother_inds = cortex['pre_ind'][nerve_inds]
        mother_pos = self.get_static_part_pos_with_inds(mother_inds)
        pos_matrix['from_x'][:] = mother_pos['x']
        pos_matrix['from_y'][:] = mother_pos['y']

        # The position of the postsynaptic cell serves as the endpoint.
        soma_father_inds = cortex['post_ind'][nerve_inds][
            father_is_static_part_mask].astype(int)
        soma_father_pos = self.get_static_part_pos_with_inds(soma_father_inds)
        pos_matrix['to_x'][father_is_static_part_mask] = soma_father_pos['x']
        pos_matrix['to_y'][father_is_static_part_mask] = soma_father_pos['y']

        # The location of the postsynaptic membrane serves as the endpoint.
        father_is_axon_end_mask = np.isin(
            cortex['father_type'][nerve_inds],
            [TYPE['axon_end'], TYPE['spine_connect']])
        nerve_father_inds = cortex['post_ind'][nerve_inds][
            father_is_axon_end_mask]
        if len(slice_cortex_matrix['type'][nerve_father_inds]):
            nerve_father_pos = self.get_nerve_pos_matrix(
                nerve_father_inds, slice_cortex_matrix)
            pos_matrix['to_x'][father_is_axon_end_mask] = nerve_father_pos['x']
            pos_matrix['to_y'][father_is_axon_end_mask] = nerve_father_pos['y']

        return pos_matrix

    def set_nerve_from_and_to_pos_with_cycle_r(self, pos_matrix,
                                               father_is_static_part_mask):
        x_delta = pos_matrix['to_x'] - pos_matrix['from_x']
        y_delta = pos_matrix['to_y'] - pos_matrix['from_y']
        z_delta = np.hypot(x_delta, y_delta)
        z_delta[z_delta == 0] = np.nan
        reciprocal_z_delta = 1 / z_delta
        reciprocal_z_delta[np.isnan(reciprocal_z_delta)] = 0
        cycle_r = self.CYCLE_R
        offset_x = (-(y_delta * reciprocal_z_delta) * cycle_r +
                    cycle_r).astype(np.int)
        offset_y = ((x_delta * reciprocal_z_delta) * cycle_r + cycle_r).astype(
            np.int)
        pos_matrix['from_x'] += offset_x
        pos_matrix['from_y'] += offset_y
        pos_matrix['to_x'][father_is_static_part_mask] += offset_x[
            father_is_static_part_mask]
        pos_matrix['to_y'][father_is_static_part_mask] += offset_y[
            father_is_static_part_mask]

        return pos_matrix

    def set_nerve_pos_with_from_and_to_pos(self, pos_matrix):
        pos_matrix['x'] = (pos_matrix['from_x'] + pos_matrix['to_x']) / 2
        pos_matrix['y'] = (pos_matrix['from_y'] + pos_matrix['to_y']) / 2

        return pos_matrix

    def filter_can_render_nerves_with_pinned_soma(self, nerve_inds, cortex,
                                                  options):
        showPinnedSomaNerveType = options.get('showPinnedSomaNerveType', 'in')
        father_or_mother = {
            'out': 'father',
            'in': 'mother',
            'all': ['father', 'mother'],
        }[showPinnedSomaNerveType]
        pinnedSomaShowMaxCircuitLengthMap = options.get(
            'pinnedSomaShowMaxCircuitLengthMap', {})

        # ind equals to id
        pinned_soma_inds = options.get('pinnedSomaInds', [])
        pinned_nerve_inds = options.get('pinnedNerveInds', [])
        if len(pinned_nerve_inds) and options.get('isOnlyShowPinnedNerves'):
            pinned_inds = pinned_nerve_inds
        else:
            pinned_inds = pinned_soma_inds

        showMaxCircuitLengthList = cortex['float_util']
        showMaxCircuitLengthList[:] = -1
        showMaxCircuitLengthList[pinned_inds] = 0
        showCircuitLengthList = cortex['int_util']
        showCircuitLengthList[:] = 0
        for nerve_ind in pinned_inds:
            showMaxCircuitLengthList[int(nerve_ind)] = float(
                pinnedSomaShowMaxCircuitLengthMap.get(str(nerve_ind), np.inf))

        if father_or_mother == 'mother':
            can_render_nerve_inds_list = [
                *self.get_father_or_mother_nerves_of_nerves(
                    pinned_inds, cortex, father_or_mother, debug=True),
                np.asarray(pinned_nerve_inds),
            ]
        elif father_or_mother == 'father':
            can_render_nerve_inds_list = [
                np.asarray(pinned_nerve_inds),
                *self.get_father_or_mother_nerves_of_nerves(
                    pinned_inds, cortex, father_or_mother),
            ]
        else:
            can_render_nerve_inds_list = [
                *self.get_father_or_mother_nerves_of_nerves(
                    pinned_inds, cortex, 'mother'),
                np.asarray(pinned_nerve_inds),
                *self.get_father_or_mother_nerves_of_nerves(
                    pinned_inds, cortex, 'father'),
            ]

        # only_show_top_n_synapses = int(
        #     self.frontend_options.get('onlyShowTopNSynapses', 0))
        # if only_show_top_n_synapses > 0 and len(pinned_nerve_inds) == 0:
        #     can_render_nerve_inds = np.concatenate(
        #         tuple(can_render_nerve_inds_list)).astype(int) if len(
        #             can_render_nerve_inds_list) else np.asarray([], int)

        #     # Translate: Only render synapses with LTP as top N.
        #     cannot_render_nerve_inds = can_render_nerve_inds
        #     for i in range(only_show_top_n_synapses):
        #         cortex['float_util'][:] = 0
        #         np.maximum.at(cortex['float_util'],
        #                       cortex['post_ind'][cannot_render_nerve_inds],
        #                       cortex['LTP'][cannot_render_nerve_inds])
        #         if i < only_show_top_n_synapses - 1:
        #             cannot_render_nerve_inds = can_render_nerve_inds[
        #                 cortex['LTP'][can_render_nerve_inds] <
        #                 cortex['float_util'][cortex['post_ind']
        #                                      [can_render_nerve_inds]]]
        #     # First, get the synapse after oneself for the topN synapses of the postsynaptic object.
        #     can_render_nerve_inds = can_render_nerve_inds[(
        #         cortex['LTP'][can_render_nerve_inds] >=
        #         cortex['float_util'][cortex['post_ind'][can_render_nerve_inds]]
        #     )]
        #     # Get the complete circuit.
        #     cortex['bool_util'][:] = False
        #     cortex['bool_util'][pinned_inds] = True
        #     cortex['bool_util'][can_render_nerve_inds] = True
        #     while True:
        #         post_nerve_can_render_mask = cortex['bool_util'][
        #             cortex['post_ind'][can_render_nerve_inds]]

        #         # When all post-synaptic objects of nerve_ind can be rendered, end the loop.
        #         if post_nerve_can_render_mask.all():
        #             break
        #         else:
        #             # Mark the neurons where postsynaptic objects are not rendered as false.
        #             cortex['bool_util'][can_render_nerve_inds[
        #                 ~post_nerve_can_render_mask]] = False

        #             # Leave a nerve that can be rendered after the synapse.
        #             can_render_nerve_inds = can_render_nerve_inds[
        #                 post_nerve_can_render_mask]

        # else:
        # Calculate the length of the circuit and assign the length of each circuit to each synapse above.
        cortex['int_util'][:] = 0
        for can_render_nerve_inds_ind, can_render_nerve_inds in enumerate(
                can_render_nerve_inds_list):
            circuit_length = len(
                can_render_nerve_inds_list) - can_render_nerve_inds_ind

            if len(can_render_nerve_inds):
                self.add_nerve_circuit_length(cortex, can_render_nerve_inds,
                                              circuit_length)

        can_render_nerve_inds = np.concatenate(
            tuple(can_render_nerve_inds_list)).astype(int) if len(
                can_render_nerve_inds_list) else np.asarray([], int)

        # # Filter out circuits with a length too short
        # min_circuit_length = int(
        #     self.frontend_options.get('minCircuitLength', 0))
        # if min_circuit_length > 0:
        #     can_render_nerve_inds = can_render_nerve_inds[
        #         cortex['int_util'][can_render_nerve_inds] >=
        #         min_circuit_length]

        # # Filter out loops with excessively large lengths.
        # max_circuit_length = int(
        #     self.frontend_options.get('maxCircuitLength', 0))
        # if max_circuit_length > 0:
        #     can_render_nerve_inds = can_render_nerve_inds[
        #         cortex['int_util'][can_render_nerve_inds] <=
        #         max_circuit_length]

        # # Filter out synapses with low LTP.
        # can_render_nerve_inds = can_render_nerve_inds[
        #     cortex['LTP'][can_render_nerve_inds] >= (
        #         int(self.frontend_options.get('minLTPThreshold', 1)) or 1)]

        # Filter out duplicate ind
        unique_nerve_inds = np.unique(cortex['ind'][can_render_nerve_inds],
                                      return_index=True)[1]
        can_render_nerve_inds = can_render_nerve_inds[unique_nerve_inds]

        # # Filter out the synapses that are newly created after this frame.
        # if CORTEX_OPTS['enable_posterior_form'] == 1:
        #     can_render_nerve_inds = can_render_nerve_inds[
        #         cortex['synapse_form_tick'][can_render_nerve_inds] <=
        #         self.write_n_read_cortex.history_write_cortex_tick]

        return self.slice_matrix(cortex, can_render_nerve_inds)

    def add_nerve_circuit_length(self, cortex, can_render_nerve_inds,
                                 circuit_length):

        # Self+circuit_length
        cortex['int_util'][can_render_nerve_inds] += circuit_length

        # Increase all downstream nerves of it by +1, and set circuit_length to 1.
        father_inds = cortex['post_ind'][can_render_nerve_inds]
        father_inds = father_inds[cortex['type'][father_inds] ==
                                  TYPE['axon_end']]
        if len(father_inds):
            self.add_nerve_circuit_length(cortex, father_inds, 1)

    def get_father_or_mother_nerves_of_nerves(self,
                                              nerve_inds,
                                              cortex,
                                              father_or_mother,
                                              debug=False):
        nerve_inds = np.asarray(nerve_inds, int)
        showMaxCircuitLengthList = cortex['float_util']
        showCircuitLengthList = cortex['int_util']
        parent_axon_end_ind = []

        if father_or_mother == 'father':
            soma_or_axon_inds = nerve_inds[np.isin(
                cortex['type'][nerve_inds], [TYPE['soma'], TYPE['axon']])]
            axon_end_inds = nerve_inds[np.isin(
                cortex['type'][nerve_inds],
                [TYPE['axon_end'], TYPE['spine_connect']])]
            cortex['bool_util'][:] = False
            cortex['bool_util'][soma_or_axon_inds] = True
            parent_axon_end_ind = np.concatenate((
                cortex['ind'][cortex['bool_util'][cortex['pre_ind']]],
                cortex['post_ind'][axon_end_inds],
            ))

            parent_axon_end_pre_ind = np.concatenate(
                (cortex['pre_ind'][cortex['bool_util'][cortex['pre_ind']]],
                 axon_end_inds))
            showMaxCircuitLengthList[
                parent_axon_end_ind] = showMaxCircuitLengthList[
                    parent_axon_end_pre_ind]
            showCircuitLengthList[parent_axon_end_ind] = showCircuitLengthList[
                parent_axon_end_pre_ind] + 1

        elif father_or_mother == 'mother':
            cortex['bool_util'][:] = False
            cortex['bool_util'][nerve_inds] = True
            post_ind_in_cortex_range_mask = (cortex['post_ind'] < len(
                cortex['bool_util'])) * (cortex['post_ind'] != -1)
            parent_axon_end_ind = cortex['ind'][
                post_ind_in_cortex_range_mask *
                cortex['bool_util'][cortex['post_ind']]]

            parent_axon_end_post_ind = cortex['post_ind'][
                post_ind_in_cortex_range_mask *
                cortex['bool_util'][cortex['post_ind']]]
            showMaxCircuitLengthList[
                parent_axon_end_ind] = showMaxCircuitLengthList[
                    parent_axon_end_post_ind]
            showCircuitLengthList[parent_axon_end_ind] = showCircuitLengthList[
                parent_axon_end_post_ind] + 1

        parent_axon_end_ind = parent_axon_end_ind[(np.isin(
            cortex['type'][parent_axon_end_ind],
            [TYPE['axon_end'], TYPE['spine_connect'], *DENDRITE_TYPE.values()
             ])) * (showCircuitLengthList[parent_axon_end_ind] <=
                    showMaxCircuitLengthList[parent_axon_end_ind])]

        if not len(parent_axon_end_ind):
            return []

        if debug:
            ''' Translation: There is too much inner content, so special filtering logic needs to be applied to the inner content that needs to be observed.
            '''
            parent_axon_end_ind = parent_axon_end_ind[np.logical_or(
                (cortex['type'][parent_axon_end_ind] == TYPE['axon_end']) *
                (cortex['region_row_no'][parent_axon_end_ind] == 16) *
                (cortex['region_hyper_col_no'][parent_axon_end_ind] == 18)
                # (cortex['region_no'][parent_axon_end_ind] == REGION['antipodal_points']['region_no'])]
                ,
                (cortex['type'][parent_axon_end_ind] == TYPE['dendrite_max']))]

        grandparent_axon_end_inds_list = self.get_father_or_mother_nerves_of_nerves(
            parent_axon_end_ind, cortex, father_or_mother,debug)

        return [parent_axon_end_ind, *grandparent_axon_end_inds_list]
        # return {
        #     'mother': [parent_axon_end_ind, *grandparent_axon_end_inds_list],
        #     'father': [*grandparent_axon_end_inds_list, parent_axon_end_ind]
        # }[father_or_mother]

    def get_in_viewport_range_static_part_mask(self, static_part_inds,
                                               viewport_range):
        static_part_pos_matrix = self.get_static_part_pos_with_inds(
            static_part_inds)
        return (static_part_pos_matrix['x'] > viewport_range['x0']) * (
            static_part_pos_matrix['x'] < viewport_range['x1']) * (
                static_part_pos_matrix['y'] > viewport_range['y0']) * (
                    static_part_pos_matrix['y'] < viewport_range['y1'])

    def get_pinned_circuit_somas(self):
        cortex_info = self.write_n_read_cortex.cortex_info
        cortex = self.write_n_read_cortex.cortex
        all_soma_inds = cortex[
            'ind'][:cortex_info['cortex_static_part_slice_stop']]
        all_nerve_inds = cortex[
            'ind'][cortex_info['cortex_static_part_slice_stop']:
                   cortex_info['history_cortex_slice_stop']]
        nerve_matrix = self.filter_can_render_nerves_with_pinned_soma(
            all_nerve_inds,
            self.slice_matrix(cortex,
                              slice(cortex_info['history_cortex_slice_stop'])),
            self.frontend_options)
        soma_mask = np.zeros(
            len(cortex['type']
                [:cortex_info['cortex_static_part_slice_stop']])).astype(bool)
        soma_mask[(np.array(
            self.frontend_options['pinnedSomaInds'])).astype(int)] = True
        soma_mask[nerve_matrix['pre_ind']] = True
        soma_mask[nerve_matrix['post_ind'][np.isin(nerve_matrix['father_type'],
                                                   STATIC_TYPES)]] = True
        soma_matrix = self.slice_matrix(cortex, all_soma_inds[soma_mask])
        return soma_matrix

    def slice_cortex_matrix_with_viewport(self, req_data):
        cortex_info = self.write_n_read_cortex.cortex_info
        cortex = self.write_n_read_cortex.cortex
        all_soma_inds = cortex[
            'ind'][:cortex_info['cortex_static_part_slice_stop']]
        all_nerve_inds = cortex[
            'ind'][cortex_info['cortex_static_part_slice_stop']:
                   cortex_info['history_cortex_slice_stop']]
        all_parts = self.slice_matrix(
            cortex, slice(cortex_info['history_cortex_slice_stop']))
        viewport_range = req_data.get('viewPortRange')
        #
        nerve_matrix = self.filter_can_render_nerves_with_pinned_soma(
            all_nerve_inds, all_parts, req_data.get('options', {}))
        # nerve_pos_matrix = self.get_nerve_pos_matrix(nerve_matrix['ind'],
        #                                              cortex)
        #
        # soma_mask = self.get_in_viewport_range_static_part_mask(
        #     all_soma_inds, viewport_range)
        soma_mask = cortex[
            'bool_util'][:cortex_info['cortex_static_part_slice_stop']]
        soma_mask[:] = False
        # soma_mask[all_soma_inds] = True
        #
        soma_mask[nerve_matrix['pre_ind']] = True
        #
        pinned_soma_inds = req_data.get('options',
                                        {}).get('pinnedSomaInds', [])
        soma_mask[pinned_soma_inds] = True
        #
        soma_matrix = self.slice_matrix(cortex, all_soma_inds[soma_mask])
        # soma_pos_matrix = self.get_static_part_pos_with_inds(
        #     soma_matrix['ind']).T
        return {
            'somas':
            {prop: soma_matrix[prop].tolist()
             for prop in soma_matrix.keys()},
            # 'soma_pos': soma_pos_matrix.tolist(),
            'nerves': {
                prop: nerve_matrix[prop].tolist()
                for prop in nerve_matrix.keys()
            },
            # 'nerve_pos': {
            #     prop: nerve_pos_matrix[prop].tolist()
            #     for prop in nerve_pos_matrix.keys()
            # },
            'marker': []
        }