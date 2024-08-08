from .regions_index import regions_index
from ...make_region import make_regions_map_with_config
import numpy as np

REGION = make_regions_map_with_config(regions_index)
REGION_INDEX_MAP = {
    region['region_no']: region.copy()
    for region in REGION.values()
}
for region in REGION_INDEX_MAP.values():
    region['neurons'] = {
        neuron['neuron_no']: neuron
        for neuron in region['neurons'].values()
    }

SOMA_SLICE_MAP = {region_name: {} for region_name in REGION.keys()}

soma_slice_start = 1  # 第0个用来存放空soma
for region_name, region_info in REGION.items():
    region_name = region_info['region_name']
    region_shape = region_info['region_shape']
    region_row_sum, hyper_col_sum_per_row, mini_col_sum_in_hyper_col = region_shape
    hyper_col_sum = hyper_col_sum_per_row * region_row_sum
    col_sum = hyper_col_sum * mini_col_sum_in_hyper_col

    for neuron_name, neuron_info in region_info['neurons'].items():
        neuron_in_pic_mask = neuron_info.get(
            'neuron_in_pic_mask',
            np.full(col_sum, True)).repeat(mini_col_sum_in_hyper_col)
        neuron_sum = np.sum(neuron_in_pic_mask)
        soma_slice_stop = soma_slice_start + neuron_sum
        SOMA_SLICE_MAP[region_name][neuron_info['name']] = {
            'cortex_slice':
            slice(soma_slice_start, soma_slice_stop),
            **({
                'neuron_in_pic_mask': neuron_in_pic_mask,
            } if 'neuron_in_pic_mask' in neuron_info else {})
        }

        soma_slice_start = soma_slice_stop