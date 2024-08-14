import websocket
import json
import simplejson
from cortex import Cortex
import importlib
from experiments import REGION
from consts.experiment import EXPERIMENT_NAME, APP_MODE, CORTEX_OPTS
from util import print_time_delta
import re
from utils.write_n_read_cortex import Write_n_read_cortex
from utils.render_cortex import RenderCortex
from consts.nerve_params import ATP, SPINE_SUM_ON_A_DENDRITE
from consts.nerve_props import TYPE, DENDRITE_TYPE
from consts.feature import VISUAL_FIELD_WH, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ORIENTS, ANGLES, RECEPTIVE_FIELD_LEVELS, BOTH_SIDE_ORIENT_DESC, ORIENT_SUM, PIXEL_ORIENTS, ORIENT_SIDES, LINE_RECEPTIVE_FIELD_LEVELS, ORIENT_CONTOUR_SIDES, CONTOUR_CENTER_ORIENTS, CONTOUR_OPEN_ANGLES, CONTOUR_OPEN_ORIENT_MAP, CONTOUR_OPEN_LINE_MAP
import numpy as np
from experiments.util import get_soma_inds
import itertools

form_init_nerve_module = importlib.import_module(
    f'experiments.{EXPERIMENT_NAME}.form_process')
cortex = Cortex()
write_n_read_cortex_map = {}
render_cortex_map = {}


def on_message(ws, message):
    message = json.loads(message)
    message_type = message['type']
    message_data = message['data']
    h5_protocol = message['from_protocol']
    if message_type == 'readFile':
        print_time_delta()
        message_stage = message_data['stage']
        res_json = {}

        if message_stage == 'init':
            if not write_n_read_cortex_map.get(h5_protocol):
                url_params = message_data['urlParams']
                write_n_read_cortex_map[h5_protocol] = Write_n_read_cortex(
                    url_params.get('data_dir_suffix', ''))
                render_cortex_map[h5_protocol] = RenderCortex(
                    write_n_read_cortex_map[h5_protocol])
                write_n_read_cortex_map[h5_protocol].init_cortex_save_data()
                render_cortex_map[h5_protocol].update_render_range_and_pos()

            res_json['allFileName'] = write_n_read_cortex_map[
                h5_protocol].get_all_history_file_name()
            if message_data['fileName'] not in res_json['allFileName']:
                message_data['fileName'] = res_json['allFileName'][0]

        _res_json, cortex_matrix = write_n_read_cortex_map[
            h5_protocol].read_cortex_history(message['data'])
        res_json.update(_res_json)
        options = message_data['options']
        regionHighlightNeuronRegExp = options.get(
            'regionHighlightNeuronRegExp')
        options['highlightStaticPart'] = {
            region_name: [
                neuron['neuron_no'] for neuron_name, neuron in REGION.get(
                    region_name, {}).get('neurons', {}).items()
                if re.search(exp, str(neuron['name']))
            ]
            for region_name, exp in regionHighlightNeuronRegExp.items()
        }
        render_cortex_map[h5_protocol].update_frontend_options(options)
        # res_json['region_range'] = render_cortex_map[
        #     h5_protocol].region_range_map
        res_json['consts'] = {
            'cycle_r': render_cortex_map[h5_protocol].CYCLE_R,
            'nerve_w': render_cortex_map[h5_protocol].NERVE_W,
            'col_w': render_cortex_map[h5_protocol].col_w,
            'padding': render_cortex_map[h5_protocol].PADDING,
            'active_potential': ATP,
            'type': TYPE,
            'dendrite_type': DENDRITE_TYPE,
        }
        filtered_part_info = render_cortex_map[
            h5_protocol].slice_cortex_matrix_with_viewport(message_data)
        res_json.update(filtered_part_info)
        res_json['stage'] = message_stage
        if res_json.get('region'):
            region_no_set = set(res_json['somas']['region_no'])
            res_json['region'] = {}
            for _region_no, _region in _res_json.get('region').items():
                neuron_no_set = set(
                    np.concatenate(
                        (res_json['somas']['neuron_no'],
                         res_json['nerves']['neuron_no']))[np.concatenate((
                             res_json['somas']['region_no'],
                             res_json['nerves']['region_no']
                         )) == _region['region_no']])
                res_json['region'][_region_no] = {
                    'region_name': _region['region_name'],
                    'region_no': _region['region_no'],
                    'region_shape': _region['region_shape'],
                    'neurons': {
                        neuron_no: neuron
                        for neuron_no, neuron in _region.get(
                            'neurons').items()
                        if neuron['neuron_no'] in neuron_no_set
                    } if _region['region_no'] in region_no_set else {}
                }
        if res_json.get('nerve_marker_map'):
            del res_json['nerve_marker_map']

        res_json['search_nerve_result'] = search_nerve(options, h5_protocol)

        res_json['fileName'] = message_data['fileName']

        data_length = len(res_json['nerves']['type'])

        # if data_length > 500:
        #     for key, val in res_json['nerves'].items():
        #         res_json['nerves'][key] = val[:500]
        # send_message = {'type': 'readFileRes', 'data': res_json}

        send_message = {
            'type': 'readFileRes',
            'data': res_json
        } if data_length < 1500 else {
            'type': 'readFileResErr',
            'data': {
                'message': f'TOO_MUCH_DATA：{data_length}',
            },
        }

        send_message.update({'to_protocol': h5_protocol})
        ws.send(simplejson.dumps(
            send_message,
            ignore_nan=True,
        ))

        print_time_delta('readFile:end')


def search_nerve(options, h5_protocol):
    search_nerve_expressions = [
        expr.get('content', '')
        for expr in options.get('searchNerveExpressions', [])
    ]
    return_list = []
    for search_nerve_expression in search_nerve_expressions:
        cortex = write_n_read_cortex_map[h5_protocol].cortex
        search_nerve_expression_returns = {
            'search_nerve_inds': np.array([], int),
            'search_nerve_prop_names': [],
        }
        search_nerve_prop_values = {}
        exec_local_vars = {
            'cortex': cortex,
            'returns': search_nerve_expression_returns,
            'VISUAL_FIELD_WH': VISUAL_FIELD_WH,
            'get_soma_inds': get_soma_inds,
            'SPINE_SUM_ON_A_DENDRITE': SPINE_SUM_ON_A_DENDRITE,
            'COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES':
            COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES,
            'ORIENTS': ORIENTS,
            'ANGLES': ANGLES,
            'RECEPTIVE_FIELD_LEVELS': RECEPTIVE_FIELD_LEVELS,
            'LINE_RECEPTIVE_FIELD_LEVELS': LINE_RECEPTIVE_FIELD_LEVELS,
            'BOTH_SIDE_ORIENT_DESC': BOTH_SIDE_ORIENT_DESC,
            'ORIENT_SUM': ORIENT_SUM,
            'PIXEL_ORIENTS': PIXEL_ORIENTS,
            'ORIENT_SIDES': ORIENT_SIDES,
            'ORIENT_CONTOUR_SIDES': ORIENT_CONTOUR_SIDES,
            'itertools': itertools,
            'np': np,
            'IS_MOCK_RECORD_PROPS': CORTEX_OPTS['IS_MOCK_RECORD_PROPS'],
            'REGION': REGION,
            'CONTOUR_CENTER_ORIENTS': CONTOUR_CENTER_ORIENTS,
            'CONTOUR_OPEN_ANGLES': CONTOUR_OPEN_ANGLES,
            'CONTOUR_OPEN_ORIENT_MAP': CONTOUR_OPEN_ORIENT_MAP,
            'CONTOUR_OPEN_LINE_MAP': CONTOUR_OPEN_LINE_MAP,
        }
        print('[exec]', search_nerve_expression.split('\n')[0])
        exec(search_nerve_expression or "''", None, exec_local_vars)

        search_nerve_inds = np.asarray(
            search_nerve_expression_returns['search_nerve_inds'], int)
        search_nerve_prop_names = search_nerve_expression_returns[
            'search_nerve_prop_names']
        search_result_limit = search_nerve_expression_returns.get(
            'search_nerve_result_limit', 150)

        if len(search_nerve_inds) == 0:
            search_result_message = 'NO_RESULT'
        elif len(search_nerve_inds) > search_result_limit:
            search_result_message = f'TOO_MUCH_RESULT ({len(search_nerve_inds)})'
            search_nerve_inds = np.array([], int)
        else:
            search_result_message = f'SUCC ({len(search_nerve_inds)})'
            search_nerve_prop_values = {
                prop_name: cortex[prop_name][search_nerve_inds].tolist()
                for prop_name in search_nerve_prop_names
            }

        search_nerve_names = [
            list(list(REGION.values())[region_no -
                                       1]['neurons'].values())[neuron_no -
                                                               100]['name']
            if region_no != -1 and neuron_no != -1 else 'none'
            for region_no, neuron_no in zip(
                cortex['region_no'][search_nerve_inds], cortex['neuron_no']
                [search_nerve_inds])
        ]

        return_list.append({
            'search_nerve_inds':
            search_nerve_inds.tolist(),
            'search_nerve_names':
            search_nerve_names,
            'search_nerve_types':
            cortex['type'][search_nerve_inds].tolist(),
            'search_nerve_region_nos':
            cortex['region_no'][search_nerve_inds].tolist(),
            'search_nerve_prop_values':
            search_nerve_prop_values,
            'message':
            search_result_message,
        })

    return return_list


def on_error(ws, error):
    print(ws)
    print(error)


# def send_all_file_name_message(state, h5_protocol):
#     ws.send(
#         json.dumps({
#             'type': 'allFileName',
#             'data': {
#                 'allFileName':
#                 write_n_read_cortex_map[h5_protocol].get_all_history_file_name(
#                 ),
#                 'appMode':
#                 APP_MODE,
#                 'state':
#                 state,
#             },
#             'to_protocol': h5_protocol,
#         }))

if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        "ws://localhost:8888",
        subprotocols=['python'],
        on_message=on_message,
        on_error=on_error)
    print('ws started')
    ws.run_forever()