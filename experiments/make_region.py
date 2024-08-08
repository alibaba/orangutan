from consts.base import LEN
from consts.nerve_props import TYPE


def update_neuron_2_map(
    neuron,
    neuron_ind,
    neuron_map,
    neuron_no,
    marker,
    region,
    mother_neuron_no=None,
    soma_neuron_no=None,
    soma_name=None,
    neuron_type='soma',
):
    if neuron_type == 'soma':
        soma_name = neuron['name']
    else:
        neuron['name'] = neuron['name'].replace('$', soma_name)
    feature = neuron.get('feature', {})
    region['feature_set'].update(feature.keys())
    neuron_type = feature.get('type', TYPE[neuron_type])
    neuron.update({
        'neuron_ind_in_col':
        neuron_no['neuron_no'],
        'neuron_no':
        neuron_no['neuron_no'] + LEN['neuron_no'],
        'mother_neuron_no':
        mother_neuron_no or neuron_no['neuron_no'] + LEN['neuron_no'],
        'soma_neuron_no':
        soma_neuron_no or neuron_no['neuron_no'] + LEN['neuron_no'],
        'type':
        neuron_type,
        'marker':
        marker['marker'],
        'soma_name':
        soma_name,
    })
    neuron_no['neuron_no'] += 1
    marker['marker'] += 1
    assert (neuron_map.get(
        neuron['name']) == None), f'神经突名称重复: {neuron["name"]}'
    neuron_map[neuron['name']] = neuron
    for dendrite in neuron.get('dendrites', []):
        dendrite['post_name'] = neuron['name']
        if 'neuron_in_pic_mask' in neuron:
            dendrite['neuron_in_pic_mask'] = neuron.get('neuron_in_pic_mask')
        update_neuron_2_map(
            dendrite,
            neuron_ind,
            neuron_map,
            neuron_no,
            marker,
            region,
            mother_neuron_no=neuron['neuron_no'],
            soma_neuron_no=neuron['soma_neuron_no'],
            soma_name=soma_name,
            neuron_type='dendrite_add',
        )
    for axon in neuron.get('axons', []):
        axon['pre_name'] = neuron['name']
        if 'neuron_in_pic_mask' in neuron:
            axon['neuron_in_pic_mask'] = neuron.get('neuron_in_pic_mask')
        update_neuron_2_map(
            axon,
            neuron_ind,
            neuron_map,
            neuron_no,
            marker,
            region,
            mother_neuron_no=neuron['neuron_no'],
            soma_neuron_no=neuron['soma_neuron_no'],
            soma_name=soma_name,
            neuron_type='axon',
        )


def get_all_hormones_in_regions_map(regions_map):
    all_hormones_map = {}
    hormone_ind = 1
    for region_name, region_info in regions_map.items():
        for neuron_info in region_info['neurons'].values():
            release_hormone = neuron_info.get('hormone',
                                              {}).get('release_hormone', None)
            if release_hormone:
                all_hormones_map[release_hormone['hormone_name']] = dict(
                    release_hormone,
                    **{
                        'hormone_ind_in_hormone_matrix': hormone_ind,
                    },
                )
                hormone_ind += 1
    return all_hormones_map


def make_regions_map_with_config(regions_config):
    regions_map = {}
    start_ind = 0
    regions = []
    marker = {'marker': 0}
    for region_config in regions_config:
        if isinstance(region_config, list):
            regions.extend(region_config)
        else:
            regions.append(region_config)

    for region_no, region in enumerate(regions, 1):
        region['raw_region_json'] = region.copy()
        region['region_no'] = region_no
        neuron_map = {}
        neuron_no = {'neuron_no': 0}
        region['feature_set'] = set()
        for neuron_ind, neuron in enumerate(region['neurons']):
            update_neuron_2_map(neuron, neuron_ind, neuron_map, neuron_no,
                                marker, region)
        region['neurons'] = neuron_map
        region_height, region_width, mini_col_sum_in_hyper_col = region[
            'region_shape']
        region['hyper_col_sum'] = region_height * region_width
        region['mini_col_sum_in_hyper_col'] = mini_col_sum_in_hyper_col
        region['mini_col_sum_in_region'] = region['hyper_col_sum'] * region[
            'mini_col_sum_in_hyper_col']
        region['static_part_sum_in_mini_col'] = len(region['neurons'])
        region['static_part_sum_in_region'] = region[
            'mini_col_sum_in_region'] * region['static_part_sum_in_mini_col']
        region['start_ind'] = start_ind
        region['end_ind'] = start_ind + region['static_part_sum_in_region']
        assert (regions_map.get(
            region['region_name']) == None), f'脑区名称重复: {region["region_name"]}'
        regions_map[region['region_name']] = region
        start_ind += region['static_part_sum_in_region']

        for neuron in neuron_map.values():
            neuron.update({
                'soma_ind_offset':
                neuron['neuron_no'] - neuron['soma_neuron_no'],
                'mother_ind_offset':
                neuron['neuron_no'] - neuron['mother_neuron_no'],
            })

    return regions_map