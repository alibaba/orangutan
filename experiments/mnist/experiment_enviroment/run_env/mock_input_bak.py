# import os
# import json
# import math
# import itertools
# import numpy as np
# from util import print_exe_timecost
# from ...regions import REGION
# from consts.feature import CONTOUR_CENTER_ORIENTS, VISUAL_FIELD_WH, ANGLE_NAMES, CONTOUR_CENTER_NAMES, ORIENTS, COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES, ANGLES, NUM_EXCITE
# from consts.nerve_props import TYPE, SYNAPSE_TYPE
# from consts.base import IMG_PATH
# from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS
# from consts.nerve_params import SPINE_SUM_ON_A_DENDRITE, SRP, ATP
# from PIL import Image
# from .controller.mock_feature_and_cal_props_controller import start_mock_feature_and_cal_props
# from experiments.util import get_soma_inds
# from .mock_globals import POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, NOWA_FEATURE_GRID_INDS, ANCHOR_FEATURE_GRID_INDS, WHOLE_CENTER_GRID_INDS, SINGLE_ABSTRACT_APPEAR_INDS, PREDICT_INDS, PREDICT_SUPRISE_INDS, PREDICT_BIAS_INDS, ACCUMULATE_PREDICT_INDS, APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs

# cortex_obj = None
# cortex = None
# # get_soma_inds = None

# num_input = None  # 6
# mnist = None  # 6_1
# origin_mnist = None  # 6_1
# feature_name = None  # 6_1;0
# all_feature_names = []
# replay_feature_names = []
# mnist_input_list_index = -1

# anchor_feature_excite_map = {}

# mnist_input_matrix = None
# pixel_occupy_matrix = None
# contour_center_matrix = None
# corner_matrix = None
# center_matrix_y_slice = None
# center_matrix_x_slice = None
# out_contour_center_matrix = None
# input_matrix_y_slice = None
# input_matrix_x_slice = None
# anchor_pos_excites = None

# observe_mnist_input_tick = 0
# OBSERVE_A_FEATURE_TICK_SUM = 18
# mock_mnist_tick_count = -1

# score_board = {}
# record_grid_excites = []
# record_props_count = 0

# mock_feature_ind = None
# will_mnist_change = False
# will_feature_change = False

# props_disappear_tick_spike_times = None


# def load_next_mnist():
#     global mnist_input_list_index, mnist, num_input, mnist_input_matrix, mock_mnist_tick_count
#     global all_feature_names, replay_feature_names
#     global cortex_obj

#     mnist_input_list_index += 1
#     mock_mnist_tick_count = -1

#     if mnist_input_list_index >= len(CORTEX_OPTS['MNIST_INPUTS_LIST']):
#         return 'NO_MORE_MNIST'

#     mnist, num_input = CORTEX_OPTS['MNIST_INPUTS_LIST'][mnist_input_list_index]
#     cortex_obj.mnist_name = mnist

#     if CORTEX_OPTS['IS_MOCK_RECORD_PROPS'] == 0:
#         # INPUT_FOLDER_NAME = 'd28_mnist'
#         # INPUT_FOLDER_NAME = 'd28_mnist_printing'
#         # INPUT_FOLDER_NAME = 'd28_mnist_select'
#         INPUT_FOLDER_NAME = 'd28_mnist_select_0n2'
#         # INPUT_FOLDER_NAME = 'test'
#         I = Image.open(f'{IMG_PATH}/input/{INPUT_FOLDER_NAME}/{mnist}.bmp')
#         L = I.convert('L')  # 转化为灰度图
#         mnist_input_matrix = np.asarray(L, np.int32)

#         # 放大兴奋
#         mnist_input_matrix *= 100

#     all_feature_names = get_all_mock_abstract_feature_names([mnist])
#     replay_feature_names = all_feature_names.copy()


# def mock_mnist():
#     global mnist_input_matrix, center_matrix_y_slice, center_matrix_x_slice

#     input_soma_inds = get_soma_inds('点', 'raw_input')
#     cortex['excite'][input_soma_inds] = mnist_input_matrix.ravel(
#     ) + cortex['RP'][input_soma_inds]

#     cortex_obj.vary_soma_inds.update(
#         input_soma_inds[cortex['excite'][input_soma_inds] >= ATP])


# def mock_数字():
#     global num_input
#     global cortex_obj, cortex
#     if num_input == None or num_input < 0: return

#     inds_数字 = get_soma_inds('数字', 'input', num_input)
#     cortex['excite'][inds_数字] = NUM_EXCITE

#     cortex_obj.vary_soma_inds.update(inds_数字)

#     return inds_数字


# def mock_anchor_pos():
#     global anchor_pos_excites
#     global cortex_obj, cortex
#     anchor_pos_inds = get_soma_inds(
#         '位置_锚点特征', [f'{x_or_y}' for x_or_y in range(VISUAL_FIELD_WH[0])])
#     cortex['excite'][anchor_pos_inds] = anchor_pos_excites

#     cortex_obj.vary_soma_inds.update(anchor_pos_inds)


# def mock_perception_input():
#     mock_mnist()
#     mock_数字()

#     # if is_conclude:
#     #     cortex_obj.init_calculate_inds()


# def mock_input(_cortex_obj, get_soma_inds_func):
#     global get_soma_inds, anchor_feature_excite_map, mnist, num_input
#     global pixel_occupy_matrix, contour_center_matrix
#     global mock_mnist_tick_count, feature_name
#     global record_props_count, record_grid_excites
#     global POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS, SINGLE_ABSTRACT_APPEAR_INDS
#     global cortex_obj, cortex

#     if not cortex_obj:
#         cortex_obj = _cortex_obj
#         cortex = cortex_obj.cortex
#         # get_soma_inds = get_soma_inds_func
#         # init_global_vars()

#     if CORTEX_OPTS['IS_MOCK_RECORD_PROPS'] == 0:
#         # 忽略兴奋太小的特征，直接重置兴奋
#         excite_feature_inds = np.concatenate(
#             tuple([
#                 get_soma_inds(feature_type, f'{feature_name}-注意力竞争结果出现')
#                 for feature_type in ['角', '轮廓中心'] for feature_name in {
#                     '角': ANGLE_NAMES,
#                     '轮廓中心': CONTOUR_CENTER_NAMES,
#                 }[feature_type]
#             ]))
#         cortex['excite'][excite_feature_inds[
#             cortex['excite'][excite_feature_inds] < 10000]] = -65

#         # 如果碰巧有多个特征兴奋完全一样，它们都会赢得注意力竞争，需要强制只留下某一个特征
#         onehot_feature_inds = np.concatenate(
#             tuple([
#                 get_soma_inds(feature_type, f'{feature_name}-注意力竞争结果出现')
#                 for feature_type in ['角', '轮廓中心'] for feature_name in {
#                     '角': ANGLE_NAMES,
#                     '轮廓中心': CONTOUR_CENTER_NAMES,
#                 }[feature_type]
#             ]))
#         excite_onehot_feature_inds = onehot_feature_inds[
#             cortex['excite'][onehot_feature_inds] > -65]
#         if len(excite_onehot_feature_inds) > 1:
#             cortex['excite'][excite_onehot_feature_inds[1:]] = -65

#     # 预测+mock属性模式
#     if CORTEX_OPTS['name'] == 'predict' and CORTEX_OPTS['IS_MOCK_RECORD_PROPS']:
#         start_with_mock_predict_mode()

#     # 预测
#     elif CORTEX_OPTS['name'] == 'predict':
#         start_without_mock_predict_mode()

#     # 训练
#     elif CORTEX_OPTS['name'] == 'train':
#         pass

#     # 训练
#     elif CORTEX_OPTS['name'] == 'mock_feature_and_cal_props':
#         start_mock_feature_and_cal_props(_cortex_obj)


# def start_with_mock_predict_mode():
#     ''' 1. 按照正向的顺序，每帧回放一个特征，执行一次cortex_cycle，直到第forward_replay_feature_ind_stop个特征为止
#         2. 在第forward_replay_feature_ind_stop个特征所在帧，让且只让这个特征与潜在目标建立后验突触
#         3. 重复执行以上两步操作，每次让forward_replay_feature_ind_stop减一，直到feature_ind_stop=0时，不再重复
#     '''
#     global will_mnist_change, will_feature_change, mock_feature_ind
#     global mock_mnist_tick_count, all_feature_names, replay_feature_names
#     global props_disappear_tick_spike_times
#     global APPEAR_NERVE_SUFFIXs, DISAPPEAR_NERVE_SUFFIXs
#     synapse_slice = slice(cortex_obj.cortex_static_nerve_slice.stop,
#                           cortex_obj.new_ind_start)
#     # 是第一个、完整的序列回放
#     is_first_full_replay = mock_feature_ind == len(all_feature_names) - 1

#     if will_feature_change:
#         cortex_obj.write_cortex('mock_feature_cycle_end')

#     # 在第forward_replay_feature_ind_stop个特征所在帧，让且只让这个特征与潜在目标建立后验突触
#     if will_mnist_change and CORTEX_OPTS['enable_posterior_form'] == 1:

#         # 如果是第一个、完整的序列回放完了，需要mock多巴胺和血清素的浓度
#         if is_first_full_replay:
#             cal_and_mock_predict_error()

#         # # 如果当前特征的ind为0，说明它前面没有锚点特征，需要将SPINE_IND_MAPS里的锚点相关的spine的marker_remain置零
#         # # 如果当前特征的ind为1，说明它前面有锚点特征，需要将SPINE_IND_MAPS里的非锚点相关的spine的marker_remain置零
#         # reset_spine_ind_map = SPINE_IND_MAPS[1 if mock_feature_ind == 0 else 0]
#         # cortex_obj.reset_cortex_props_to_initial_state(
#         #     reset_inds=list(
#         #         itertools.chain(*[
#         #             get_soma_inds('数字', f'前馈预测_DMax_棘{spine_ind}')
#         #             for spine_ind in reset_spine_ind_map.values()
#         #         ])),
#         #     include_props=['marker_remain'])

#         # 在数字上模拟marker_remain
#         mock_number_hormone_concentration()

#         # 存在预测偏差时，进行学习
#         if (cortex['marker_remain'][PREDICT_SUPRISE_INDS] > 0).any():

#             # 如果不是第一次完整的回放，说明这次回放的最后一个特征在实际特征序列里有后续的特征，那么它的消失就可以去stp它的下一个特征
#             if not is_first_full_replay:
#                 # 模拟这一组属性消失的突触的脉冲次数和marker_remain
#                 # 用当前出现的属性，来模拟这组属性的消失细胞的marker_remain
#                 nowa_props_disappear_inds = mock_abstract_nerves_prop(
#                     DISAPPEAR_NERVE_SUFFIXs, 'tick_spike_times',
#                     cortex['tick_spike_times'][POPU_ABSTRACT_APPEAR_INDS])
#                 cortex_obj.add_marker_remain(nowa_props_disappear_inds)
#                 # 用当前属性的消失细胞的marker_remain，来模拟属性消失的突触的脉冲次数和marker_remain
#                 cortex['bool_util'][:] = False
#                 cortex['bool_util'][nowa_props_disappear_inds] = True
#                 nowa_props_disappear_synapse_inds = cortex['ind'][
#                     synapse_slice][cortex['bool_util'][cortex['pre_ind'][[
#                         synapse_slice
#                     ]]]]
#                 cortex['tick_spike_times'][
#                     nowa_props_disappear_synapse_inds] = cortex[
#                         'tick_spike_times'][cortex['pre_ind'][
#                             nowa_props_disappear_synapse_inds]]
#                 cortex_obj.add_marker_remain(nowa_props_disappear_synapse_inds)

#             # 模拟上一组属性消失的神经突的脉冲次数和marker_remain
#             prev_props_disappear_inds = mock_abstract_nerves_prop(
#                 DISAPPEAR_NERVE_SUFFIXs, 'tick_spike_times',
#                 props_disappear_tick_spike_times)
#             cortex_obj.add_marker_remain(prev_props_disappear_inds)

#             # 如果有必要，创建新的树突棘
#             cortex_obj.create_new_spine_if_need()

#             # 建立、强化突触
#             cortex_obj.write_cortex('before_form_synapse')
#             cortex_obj.form_synapse()
#             cortex_obj.write_cortex('after_form_synapse')

#             # 建立突触后，进行树突棘竞争
#             competition_spine_inds = PREDICT_INDS[
#                 cortex['marker_remain'][PREDICT_INDS] > 0]
#             # 树突棘弱化的效果和最大的excite成正比，因为希望在一开始大家都没有形成较稳定回路时，弱化这种树突棘竞争关系的作用，避免在早期marker_remain对回路形成过程的影响过大
#             spine_weaken_effect = np.maximum(
#                 0, np.minimum(1,
#                               cortex['excite'][competition_spine_inds] / 10))

#             competition_spine_mask = cortex['bool_util']
#             competition_spine_mask[:] = False
#             competition_spine_mask[competition_spine_inds] = True
#             spine_connect_inds = cortex['ind'][
#                 (cortex['type'] == TYPE['spine_connect']) *
#                 (competition_spine_mask[cortex['pre_ind']])]
#             spine_connect_competition_force = cortex['excite'][cortex[
#                 'pre_ind'][spine_connect_inds]] * cortex['marker_remain'][
#                     cortex['pre_ind'][spine_connect_inds]] * cortex[
#                         'transmitter_release_sum'][spine_connect_inds]
#             cortex['exinfo_0'][
#                 spine_connect_inds] = spine_connect_competition_force
#             spine_competition_stress = cortex['float_util']
#             spine_competition_stress[:] = 0
#             np.maximum.at(
#                 spine_competition_stress,
#                 cortex['post_ind'][spine_connect_inds],
#                 spine_connect_competition_force,
#             )
#             cortex['exinfo_0'][competition_spine_inds] = np.maximum(
#                 1,
#                 (spine_competition_stress[competition_spine_inds] /
#                  np.maximum(1,
#                             (cortex['marker_remain'][competition_spine_inds] *
#                              cortex['excite'][competition_spine_inds]))) *
#                 spine_weaken_effect)
#             need_weaken_synapse_inds = cortex['ind'][
#                 (competition_spine_mask[cortex['post_ind']]) *
#                 (cortex['is_synapse'] != 0)]
#             cortex['LTP'][need_weaken_synapse_inds] /= cortex['exinfo_0'][
#                 cortex['post_ind'][need_weaken_synapse_inds]]

#             cortex_obj.write_cortex('spine_competition')

#         # 如果还可以往前回溯，就重新正向回放更短的特征序列
#         if len(replay_feature_names) > 1:

#             cortex_obj.weaken_synapse()

#             # 每次从头回放特征，都把回放截止的特征索引减一
#             replay_feature_names = replay_feature_names[:-1]

#             # 重置当前mnist的tick，从头开始回放特征
#             mock_mnist_tick_count = -1

#             # 从头回放新的序列时，需要重置部分细胞属性
#             reserve_marker_remain_inds = [

#                 # 保留预测编码细胞的marker_remain，用于后续的特征与之建立预测突触
#                 *PREDICT_SUPRISE_INDS,
#                 *PREDICT_BIAS_INDS,

#                 # # 保留所有本次特征序列生成或增强的突触的marker_remain，用于下次特征序列的属性细胞与之建立stp突触
#                 # *cortex['ind'][cortex['is_synapse'] == 2],
#                 *cortex['ind'][np.isin(
#                     cortex['synapse_type'],
#                     [SYNAPSE_TYPE['STP'], SYNAPSE_TYPE['Fa_STP']])],
#             ]
#             reserve_marker_remain = cortex['marker_remain'][
#                 reserve_marker_remain_inds]
#             cortex_obj.reset_cortex_props_to_initial_state()
#             cortex['marker_remain'][
#                 reserve_marker_remain_inds] = reserve_marker_remain

#         # 如果没有更短的序列可以回放，则结束对这个mnist的回放
#         else:

#             # 特征序列结束后，弱化数字细胞相关的突触
#             cortex_obj.weaken_synapse()

#             cortex_obj.write_cortex('mnist_end')

#             # 一个mnist结束后，需要重置属性
#             cortex_obj.reset_cortex_props_to_initial_state()

#         cortex['is_synapse'][cortex['is_synapse'] == 2] = 1

#     # 模拟下一个特征的属性
#     [
#         mock_feature_ind,
#         is_feature_changed,
#         is_mnist_changed,
#         will_feature_change,
#         will_mnist_change,
#     ] = mock_next_feature()

#     # # 如果mnist变了，需要创建新的计分对象
#     # if is_mnist_changed == True:
#     #     score_board[mnist] = score_board.get(mnist, [])
#     #     score_board[mnist].append({})

#     if is_feature_changed:

#         # # 记录关键帧数信息
#         # record_key_ticks_to_score_board()

#         # # 记录特征变化帧数信息
#         # record_feature_changed_ticks_to_score_board()

#         # # 每次切换特征，都把之前在数字树突棘上积累的的marker_remain翻倍，使得先被观察到的特征对环境以及树突棘活化的影响更大
#         # cortex['marker_remain'][PREDICT_INDS] *= 2

#         # 每次切换特征，都把之前在数字树突棘上积累的的marker_remain除以2，使得后被观察到的特征对环境以及树突棘活化的影响更大
#         cortex['marker_remain'][PREDICT_INDS] /= 2

#     if is_mnist_changed == 'LIST_END':
#         raise ValueError('LIST_END')


# def get_is_conclude_in_without_mock_predict_mode():
#     global observe_mnist_input_tick

#     # debug
#     return cortex_obj.tick % 15 == 0
#     # return cortex_obj.tick % 3 == 0

#     # 如果到了位置细胞开始活跃的那一帧，所有位置细胞都没有活跃，那么就认为没有新的特征被观察到，就可以得出结论了
#     is_tick_at_pos_cell_start_to_active = max(
#         -1, observe_mnist_input_tick - OBSERVE_A_FEATURE_TICK_SUM) % 5 == 0
#     is_pos_cell_all_in_resting_potential = (cortex['excite'][get_soma_inds(
#         '位置_当前特征',
#         [f'{x_or_y}' for x_or_y in range(VISUAL_FIELD_WH[0])])] == SRP).all()
#     is_conclude = is_tick_at_pos_cell_start_to_active and is_pos_cell_all_in_resting_potential

#     return is_conclude


# def start_without_mock_predict_mode():
#     global observe_mnist_input_tick, record_props_count
#     global record_grid_excites

#     # 得出结论
#     is_conclude = get_is_conclude_in_without_mock_predict_mode()
#     if is_conclude:
#         conclude_in_without_mock_predict_mode()

#     # 初始化
#     if cortex_obj.tick == 0 or is_conclude:

#         # 清理细胞属性
#         cortex_obj.reset_cortex_props_to_initial_state()
#         # 清理细胞属性后，需要重新初始化可计算的神经，保证自突触的神经元可以在下一个样本中参与计算
#         cortex_obj.init_calculate_inds()

#         record_grid_excites = []
#         load_next_mnist_error = load_next_mnist()
#         assert load_next_mnist_error == None, load_next_mnist_error
#         record_props_count = 0
#         observe_mnist_input_tick = 1

#         mock_perception_input()

#     # 扫视
#     is_saccade = eye_saccade(True)

#     if is_saccade:
#         print('[eye_saccade]', cortex_obj.tick)

#         # 记录属性
#         record_props()

#         cortex_obj.write_cortex('eye_saccade')

#         # # 记录关键帧数信息
#         # record_key_ticks_to_score_board()

#         # 记录当前属性作为锚点属性
#         record_anchor_feature_excite_map()

#         #
#         ''' 在第10帧的时候，注意力竞争结果首次出现，在第18(OBSERVE_A_FEATURE_TICK_SUM)帧进行第一次扫视，此后每隔8帧进行一次扫视活动
#         '''
#         clear_excite_when_saccade_in_predict_mode()

#         mock_anchor_pos()

#     # record_feature_changed_ticks_to_score_board()

#     observe_mnist_input_tick += 1


# def conclude_in_without_mock_predict_mode():
#     global cortex_obj, cortex

#     # # 记录预测结果
#     # record_predict_result_to_score_board()


# def record_predict_result_to_score_board():
#     global cortex_obj, cortex
#     global score_board, mnist

#     # 记录预测结果并输出
#     predict_num = np.argmax(cortex['excite'][get_soma_inds('数字', '累积前馈预测')])
#     all_num_predict_excite = cortex['excite'][get_soma_inds('数字', '累积前馈预测')]
#     score_info = score_board[mnist][-1]
#     score_info.update({
#         'predict_num': int(predict_num),
#         'is_pred_succ': bool(predict_num == num_input),
#         'all_num_predict_excite': list(all_num_predict_excite),
#     })
#     if score_info.get('key_ticks'):
#         # score_info['key_ticks'] = [*score_info['key_ticks'], cortex_obj.tick]
#         score_info.update({
#             'is_perception_ok': {
#                 True: 'ok',
#                 False: 'not_ok',
#             }[len(score_info['feature_change_ticks']) ==
#               len(score_info['key_ticks']) - 1]
#         })

#     # print('[score_board]', score_board)
#     print('[conclude]', predict_num)

#     # # 保存计分板数据
#     # with open(f'{HISTORY_DIR}/score.json', mode='w') as file:
#     #     file.write(json.dumps(score_board))


# def record_key_ticks_to_score_board():
#     global anchor_feature_excite_map, score_board, mnist, record_grid_excites
#     global cortex_obj, cortex
#     score_info = score_board[mnist][-1]

#     # 记录关键帧数
#     score_info['key_ticks'] = score_info.get('key_ticks', [])
#     score_info['key_ticks'].append(cortex_obj.tick)


# # 记录当前属性作为锚点属性
# def record_anchor_feature_excite_map():
#     global cortex_obj, cortex
#     global anchor_feature_excite_map, score_board, mnist, record_grid_excites

#     anchor_feature_excite_map = {
#         (abstract_type, abstract_name):
#         cortex['excite'][get_soma_inds(f'属性-{abstract_type}',
#                                        f'{abstract_name}-个体编码')]
#         for abstract_type, abstract_values in
#         COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
#         if abstract_type in ['朝向', '角度', '类型']
#         for abstract_name, _ in abstract_values
#     }


# def record_feature_changed_ticks_to_score_board():
#     global cortex_obj, cortex
#     global anchor_feature_excite_map, score_board, mnist, record_grid_excites
#     global NOWA_FEATURE_GRID_INDS
#     score_info = score_board[mnist][-1]
#     score_info['feature_change_ticks'] = score_info.get(
#         'feature_change_ticks', [])

#     # 网格细胞的兴奋变化意味着特征兴奋的变化，需要进行记录
#     grid_excites = cortex['excite'][NOWA_FEATURE_GRID_INDS]
#     is_grid_excites_changed = (grid_excites >= ATP).any() and (
#         len(record_grid_excites) == 0 or
#         (grid_excites != record_grid_excites).any())
#     if is_grid_excites_changed:
#         score_info['feature_change_ticks'].append(cortex_obj.tick)
#         record_grid_excites = grid_excites


# def mock_number_hormone_concentration():
#     global cortex_obj, cortex
#     global ACCUMULATE_PREDICT_INDS, num_input

#     # mock多巴胺浓度
#     # 将有预测意外的数字的树突棘上的marker_remain赋值给dopamine_remain
#     cortex['dopamine_remain'][PREDICT_INDS] = cortex['marker_remain'][
#         np.repeat(PREDICT_SUPRISE_INDS, SPINE_SUM_ON_A_DENDRITE)] * (
#             cortex['marker_remain'][PREDICT_INDS] / 100)

#     # 将dopamine_remain归一化，把树突棘的marker_remain水平拉到和预测回路上的突触一个水平
#     MAX_DOPAMINE_REMAIN = 1.5
#     max_dopamine_remain = np.max(cortex['dopamine_remain'][PREDICT_INDS])
#     cortex['dopamine_remain'][PREDICT_INDS] *= MAX_DOPAMINE_REMAIN / (
#         max_dopamine_remain or MAX_DOPAMINE_REMAIN)

#     # mock血清素浓度
#     cortex['seretonin_remain'][PREDICT_INDS] = cortex['marker_remain'][
#         np.repeat(PREDICT_BIAS_INDS, SPINE_SUM_ON_A_DENDRITE)] * 2000

#     # marker_remain不归一化，但是要把没有多巴胺的marker_remain置为0
#     cortex['marker_remain'][PREDICT_INDS[cortex['dopamine_remain']
#                                          [PREDICT_INDS] == 0]] = 0


# def cal_and_mock_predict_error():
#     global cortex_obj, cortex

#     mock_数字()

#     # mock预测偏差兴奋
#     num_input_excites = cortex['excite'][get_soma_inds('数字', 'input')]
#     # cortex['excite'][PREDICT_SUPRISE_INDS] = np.maximum( SRP, num_input_excites - cortex['excite'][ACCUMULATE_PREDICT_INDS] + SRP)
#     # debug 先不考虑实际预测兴奋，直接固定一个预测偏差
#     cortex['excite'][PREDICT_SUPRISE_INDS] = num_input_excites

#     cortex['excite'][PREDICT_BIAS_INDS] = np.maximum(
#         SRP,
#         cortex['excite'][ACCUMULATE_PREDICT_INDS] - num_input_excites + SRP)

#     # mock预测偏差的marker_remain
#     cortex_obj.set_spike_times_with_excite(PREDICT_SUPRISE_INDS)
#     cortex_obj.set_spike_times_with_excite(PREDICT_BIAS_INDS)
#     cortex_obj.add_marker_remain(PREDICT_SUPRISE_INDS)
#     cortex_obj.add_marker_remain(PREDICT_BIAS_INDS)

#     cortex_obj.write_cortex('cal_and_mock_predict_error')


# def clear_excite_when_saccade_in_predict_mode():
#     global cortex_obj, cortex
#     clear_excite_inds = [
#         *get_soma_inds('全局调控', '注意力竞争兴奋汇总'),
#         *get_soma_inds(
#             '轮廓中心',
#             [f'朝向{orient}的内轮廓中心-注意力竞争' for orient in CONTOUR_CENTER_ORIENTS]),
#         *get_soma_inds('轮廓中心', [
#             f'朝向{orient}的内轮廓中心-注意力竞争结果出现' for orient in CONTOUR_CENTER_ORIENTS
#         ]),
#         *get_soma_inds('角', [
#             f'方位{orient}和{(orient+angle)%360 or 360.0}的角-注意力竞争'
#             for orient in ORIENTS for angle in ANGLES
#         ]),
#         *get_soma_inds('角', [
#             f'方位{orient}和{(orient+angle)%360 or 360.0}的角-注意力竞争结果出现'
#             for orient in ORIENTS for angle in ANGLES
#         ]),
#         *get_soma_inds('数字', '累积前馈预测onehot'),
#         #
#         *itertools.chain(*[
#             get_soma_inds(f'属性-{abstract_type}', f'{abstract_name}-个体编码')
#             for abstract_type, abstract_values in
#             COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
#             for abstract_name, _ in abstract_values
#         ]),
#         *itertools.chain(*[
#             get_soma_inds(f'属性-{abstract_type}', f'{abstract_name}-个体编码出现')
#             for abstract_type, abstract_values in
#             COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()
#             for abstract_name, _ in abstract_values
#         ]),
#         *NOWA_FEATURE_GRID_INDS,
#     ]
#     clear_excite_inds = np.compress(cortex['excite'][clear_excite_inds] != SRP,
#                                     clear_excite_inds)
#     cortex['excite'][clear_excite_inds] = SRP
#     cortex_obj.vary_soma_inds.update(clear_excite_inds)

#     # 扫视后重置全局调控限制属性出现时机的current_step
#     公用调控兴奋_A限制属性出现时机_ind = get_soma_inds('全局调控', '公用调控兴奋_A限制属性出现时机')[0]
#     公用调控兴奋_A限制属性出现时机_axon_end_inds = cortex['ind'][cortex['pre_ind'] ==
#                                                    公用调控兴奋_A限制属性出现时机_ind]
#     cortex['current_step'][公用调控兴奋_A限制属性出现时机_axon_end_inds] = 7
#     cortex_obj.vary_axon_end_inds.update(公用调控兴奋_A限制属性出现时机_axon_end_inds)

#     公用调控兴奋_A限制激励数字预测onehot的最大值_ind = get_soma_inds(
#         '全局调控', '公用调控兴奋_A限制激励数字预测onehot的最大值')[0]
#     公用调控兴奋_A限制激励数字预测onehot的最大值_axon_end_ind = cortex['ind'][
#         cortex['pre_ind'] == 公用调控兴奋_A限制激励数字预测onehot的最大值_ind]
#     cortex['current_step'][公用调控兴奋_A限制激励数字预测onehot的最大值_axon_end_ind] = 17
#     cortex_obj.vary_axon_end_inds.update(
#         公用调控兴奋_A限制激励数字预测onehot的最大值_axon_end_ind)


# def record_props():
#     global POPU_ABSTRACT_APPEAR_INDS, SINGLE_ABSTRACT_APPEAR_INDS
#     global mnist, record_props_count, record_grid_excites
#     ''' 写入input会自动覆盖，但如果老的序列比新序列长，那么多出来的节点就不会被清除，在mock的时候依然会被读取，导致结果有偏差
#         所以写入前需要清理这个mnist相关的全部的文件，保证所有文件都是这次写入的
#     '''
#     if record_props_count == 0:
#         remove_paths = [
#             feature_name for feature_name in os.listdir(INPUT_DIR)
#             if feature_name.startswith(mnist)
#         ]
#         for remove_path in remove_paths:
#             os.remove(f'{INPUT_DIR}/{remove_path}')

#     save_input_path = f'{INPUT_DIR}/{mnist}_{record_props_count}'

#     # 记录抽象细胞兴奋
#     np.save(f'{save_input_path};excite',
#             cortex['excite'][POPU_ABSTRACT_APPEAR_INDS],
#             allow_pickle=False)

#     # 记录抽象细胞tick_spike_times
#     np.save(f'{save_input_path};tick_spike_times',
#             cortex['tick_spike_times'][POPU_ABSTRACT_APPEAR_INDS],
#             allow_pickle=False)

#     # 记录网格细胞兴奋
#     np.save(f'{save_input_path};grid',
#             cortex['excite'][NOWA_FEATURE_GRID_INDS],
#             allow_pickle=False)
#     #
#     np.save(f'{save_input_path};whole_center_grid',
#             cortex['excite'][WHOLE_CENTER_GRID_INDS],
#             allow_pickle=False)

#     record_props_count += 1


# def mock_props_disappear(before_feature_name):
#     global POPU_ABSTRACT_DISAPPEAR_INDS, POPU_ABSTRACT_APPEAR_INDS

#     before_abstract_excites = np.load(
#         f'{INPUT_DIR}/{before_feature_name};excite.npy', allow_pickle=False)
#     cortex['excite'][POPU_ABSTRACT_DISAPPEAR_INDS] = before_abstract_excites
#     cortex_obj.vary_soma_inds.update(POPU_ABSTRACT_DISAPPEAR_INDS)

#     cortex['excite'][POPU_ABSTRACT_APPEAR_INDS] = cortex['RP'][
#         POPU_ABSTRACT_APPEAR_INDS]
#     cortex_obj.vary_soma_inds.update(POPU_ABSTRACT_APPEAR_INDS)


# def mock_props_appear(feature_name):
#     global POPU_ABSTRACT_APPEAR_INDS, POPU_ABSTRACT_DISAPPEAR_INDS

#     # mock属性
#     cortex['excite'][POPU_ABSTRACT_APPEAR_INDS] = np.load(
#         f'{INPUT_DIR}/{feature_name};excite.npy', allow_pickle=False)
#     cortex_obj.vary_soma_inds.update(POPU_ABSTRACT_APPEAR_INDS)

#     # mock网格位置
#     cortex['excite'][NOWA_FEATURE_GRID_INDS] = np.load(
#         f'{INPUT_DIR}/{feature_name};grid.npy', allow_pickle=False)
#     cortex_obj.vary_soma_inds.update(NOWA_FEATURE_GRID_INDS)
#     #
#     cortex['excite'][WHOLE_CENTER_GRID_INDS] = np.load(
#         f'{INPUT_DIR}/{feature_name};whole_center_grid.npy',
#         allow_pickle=False)
#     cortex_obj.vary_soma_inds.update(WHOLE_CENTER_GRID_INDS)

#     # mock属性出现的同时，要清除掉上一组属性的消失
#     clear_before_abstract_inds = np.compress(
#         cortex['excite'][POPU_ABSTRACT_DISAPPEAR_INDS] !=
#         cortex['RP'][POPU_ABSTRACT_DISAPPEAR_INDS],
#         POPU_ABSTRACT_DISAPPEAR_INDS)
#     cortex['excite'][clear_before_abstract_inds] = cortex['RP'][
#         clear_before_abstract_inds]
#     cortex_obj.vary_soma_inds.update(clear_before_abstract_inds)


# def mock_reverse_replay_number_spine_marker_remain(feature_name):
#     global cortex_obj, cortex

#     # mock属性转运marker_remain的轴突的excite
#     abstract_excite = np.load(f'{INPUT_DIR}/{feature_name};excite.npy',
#                               allow_pickle=False)
#     # mock_abstract_nerve_inds = mock_abstract_nerves_prop(['群体编码出现_A转运标记物'], 'excite', abstract_excite)
#     mock_abstract_nerve_inds = mock_abstract_nerves_prop(['群体编码出现'], 'excite',
#                                                          abstract_excite)

#     # 将之前的特征在数字树突棘上积累的marker_remain先弱化一下
#     # cortex['marker_remain'][PREDICT_INDS] /= 2
#     cortex['marker_remain'][PREDICT_INDS] = 0  # TODO debug

#     # mock传递marker_remain的过程
#     cortex_obj.vary_axon_inds.update(mock_abstract_nerve_inds)
#     cortex_obj.spike()


# def eye_saccade(is_saccade_2_next_feature):
#     global input_matrix_y_slice, input_matrix_x_slice, center_matrix_y_slice, center_matrix_x_slice
#     global mnist_input_matrix, contour_center_matrix, corner_matrix, out_contour_center_matrix
#     global observe_mnist_input_tick, anchor_pos_excites, OBSERVE_A_FEATURE_TICK_SUM
#     global NOWA_FEATURE_GRID_INDS
#     is_saccade_2_next_feature = is_saccade_2_next_feature if is_saccade_2_next_feature != None else max(
#         -1, observe_mnist_input_tick - OBSERVE_A_FEATURE_TICK_SUM) % 11 == 0

#     if is_saccade_2_next_feature:

#         # 记录当前特征位置，用于mock锚点特征位置
#         anchor_pos_excites = cortex['excite'][NOWA_FEATURE_GRID_INDS]

#     return is_saccade_2_next_feature