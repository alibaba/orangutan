# from ..regions import REGION
# from consts.feature import ORIENTS, ORIENT_SUM, PIXEL_ORIENTS, ORIENT_SIDES, RECEPTIVE_FIELD_LEVELS
# from ...util import get_soma_inds, get_around_and_center_hyper_col_inds_with_around_mask, save_axon_end_inds_with_new_nerves, get_around_and_center_hyper_col_inds_with_around_mask
# import numpy as np
# import itertools
# import math
# from ...form_nerve.form_nerve import form_nerve

# axon_end_inds = {}


# def 原始input激励input(cortex_obj):
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     mother_inds.extend(get_soma_inds('点', 'input锐化'))
#     father_inds.extend(get_soma_inds('点', f'input'))
#     return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
#                                            cortex_obj)


# # def 原始input激励input限制(cortex_obj):
# #     mother_inds, father_inds, axon_end_release_sums = [], [], []
# #     for rotate_time in range(4):
# #         orient = rotate_time + 1
# #         mother_inds.extend(get_soma_inds('点', 'input锐化'))
# #         father_inds.extend(
# #             get_soma_inds('点', f'input_DAdd{orient*90}方位上的直线中心的兴奋'))
# #     return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
# #                                            cortex_obj)


# def 原始input直线激励input(cortex_obj):
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     gray_matrix = np.array([
#         [0, 1, 0],
#         [0, 1, 0],
#         [0, 1, 0],
#     ]).astype(bool)
#     # [
#     #     [0, 0, 0, 0, 0],
#     #     [0, 0, 0, 0, 0],
#     #     [0, 0, 0, 0, 1],
#     #     [0, 0, 0, 1, 0],
#     #     [0, 0, 1, 0, 0],
#     # ]
#     for rotate_time in range(4):
#         orient = rotate_time + 1
#         this_gray_matrix = np.rot90(gray_matrix, -rotate_time)
#         around_pos_inds, center_pos_inds, _ = get_around_and_center_hyper_col_inds_with_around_mask(
#             '点', '点', this_gray_matrix)
#         mother_inds.extend(get_soma_inds('点', 'input锐化', around_pos_inds))
#         father_inds.extend(
#             get_soma_inds('点', f'input_DAdd{orient*90}方位上的直线的兴奋平均值',
#                           center_pos_inds))
#         axon_end_release_sums.extend([65 / np.sum(this_gray_matrix)] *
#                                      center_pos_inds.size)
#     return form_nerve.make_new_nerve_packs(mother_inds,
#                                            father_inds,
#                                            cortex_obj,
#                                            reset_nerve_props_matrix=np.array(
#                                                axon_end_release_sums,
#                                                dtype=[('transmitter_release_sum',
#                                                        'float')]))


# def 四周相邻点的最大值抑制input(cortex_obj):
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     gray_matrix = np.array([
#         [0, 0, 1],
#         [0, 0, 1],
#         [0, 0, 1],
#     ]).astype(bool)
#     for rotate_time in range(4):
#         orient = rotate_time + 1
#         this_gray_matrix = np.rot90(gray_matrix, -rotate_time)
#         around_pos_inds, center_pos_inds, _ = get_around_and_center_hyper_col_inds_with_around_mask(
#             '点', '点', this_gray_matrix)
#         mother_inds.extend(get_soma_inds('点', 'input锐化', around_pos_inds))
#         father_inds.extend(
#             get_soma_inds('点', f'input_DAdd{orient*90}方位上的直线抑制激励点',
#                           center_pos_inds))
#         axon_end_release_sums.extend([65 / np.sum(this_gray_matrix)] *
#                                      center_pos_inds.size)
#     return form_nerve.make_new_nerve_packs(mother_inds,
#                                            father_inds,
#                                            cortex_obj,
#                                            reset_nerve_props_matrix=np.array(
#                                                axon_end_release_sums,
#                                                dtype=[('transmitter_release_sum',
#                                                        'float')]))


# def 四周相邻点的最大值解抑input(cortex_obj):
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     gray_matrix = np.array([
#         [1, 0, 0],
#         [1, 0, 0],
#         [1, 0, 0],
#     ]).astype(bool)
#     for rotate_time in range(4):
#         orient = rotate_time + 1
#         this_gray_matrix = np.rot90(gray_matrix, -rotate_time)
#         around_pos_inds, center_pos_inds, _ = get_around_and_center_hyper_col_inds_with_around_mask(
#             '点', '点', this_gray_matrix)
#         mother_inds.extend(get_soma_inds('点', 'input锐化_A抑制', around_pos_inds))
#         father_inds.extend(
#             get_soma_inds('点', f'input_DAdd{orient*90}方位上的直线抑制激励点',
#                           center_pos_inds))
#         axon_end_release_sums.extend([65 / np.sum(this_gray_matrix)] *
#                                      center_pos_inds.size)
#     return form_nerve.make_new_nerve_packs(mother_inds,
#                                            father_inds,
#                                            cortex_obj,
#                                            reset_nerve_props_matrix=np.array(
#                                                axon_end_release_sums,
#                                                dtype=[('transmitter_release_sum',
#                                                        'float')]))


# def form_init_nerve():
#     return [
#         原始input激励input,
#         # 原始input激励input限制,
#         原始input直线激励input,
#         四周相邻点的最大值抑制input,
#         四周相邻点的最大值解抑input,
#     ]
