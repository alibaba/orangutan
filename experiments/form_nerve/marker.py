import numpy as np

MARKER_REMAIN_THRESHOLD = 1


class Marker():

    def __init__(self, REGION):
        self.REGION = REGION

    def get(self, region_name, neuron_name):
        return self.REGION[region_name]['neurons'][neuron_name]['marker']

    def join(self, marker_info_tuple1, marker_info_tuple2):
        return int(
            f'{self.get(*marker_info_tuple1)}{self.get(*marker_info_tuple2)}')

    def filter(self, cortex_obj, filter_markers):
        if not isinstance(filter_markers, list):
            filter_markers = [filter_markers]
        filter_mask = np.isin(
            cortex_obj.cortex['marker'][cortex_obj.all_marker_inds],
            filter_markers)
        return cortex_obj.all_marker_inds[filter_mask]
