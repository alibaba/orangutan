# from consts.base import GRAY_IMG_PATH
# from consts.feature import ORIENT_SUM, ORIENTS, RECEPTIVE_FIELD_LEVELS, global_axon_end_inds, CONTOUR_SIDES, ORIENT_SIDES, ORIENT_CONTOUR_SIDES, BOTH_SIDE_ORIENT_DESC
# from ...util import get_soma_inds, get_around_and_center_pos_inds_with_gray_img, save_axon_end_inds_with_new_nerves
# import numpy as np
# import itertools
# import math
# from ...form_nerve.form_nerve import form_nerve

# gray_img_infos = {}
# for orient_ind, orient in enumerate(ORIENTS):
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#         gray_filefold_path = f'{GRAY_IMG_PATH}/d{receptive_field_level}'
#         orient_img = math.ceil(orient) % 90 + 90
#         rotate_time = orient // 90 - 1
#         gray_img_path = f'{gray_filefold_path}/{orient_img}.jpg'
#         around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = get_around_and_center_pos_inds_with_gray_img(
#             '点',
#             f'方位-S{receptive_field_level}',
#             gray_img_path,
#             gray_img_rotate_time=rotate_time)
#         #
#         sum_gray_matrix = gray_matrix.astype(np.float)
#         sum_gray_axon_end_release_sum_matrix = sum_gray_matrix[
#             np.newaxis, :, :] / 255 * 65 * inrange_mother_pos_mask.astype(int)
#         sum_gray_axon_end_mask = sum_gray_axon_end_release_sum_matrix > 0
#         sum_gray_axon_end_release_sum = sum_gray_axon_end_release_sum_matrix[
#             sum_gray_axon_end_mask]
#         #
#         max_gray_matrix = gray_matrix.astype(np.float)
#         max_gray_matrix *= 255 / np.max(max_gray_matrix)
#         max_gray_axon_end_release_sum_matrix = max_gray_matrix[
#             np.newaxis, :, :] / 255 * 65 * inrange_mother_pos_mask.astype(int)
#         max_gray_axon_end_mask = max_gray_axon_end_release_sum_matrix > 0
#         max_gray_axon_end_release_sum = max_gray_axon_end_release_sum_matrix[
#             max_gray_axon_end_mask]
#         gray_img_infos[(orient, receptive_field_level)] = (
#             around_pos_inds, center_pos_inds, inrange_mother_pos_mask,
#             gray_matrix, sum_gray_axon_end_release_sum,
#             max_gray_axon_end_release_sum)


# def 激励各个尺度各个方位的像素点(cortex_obj):
#     mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
#     for orient_ind, orient in enumerate(ORIENTS):
#         for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#             around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix, sum_gray_axon_end_release_sum, max_gray_axon_end_release_sum = gray_img_infos[
#                 (orient, receptive_field_level)]
#             mother_inds.extend(get_soma_inds('点', 'input', around_pos_inds))
#             father_inds.extend(
#                 get_soma_inds(f'方位-S{receptive_field_level}',
#                               f'{orient}方位的像素点_DMax', center_pos_inds))
#             reset_nerve_props_matrix.extend(max_gray_axon_end_release_sum)
#     return form_nerve.make_new_nerve_packs(mother_inds,
#                                            father_inds,
#                                            cortex_obj,
#                                            reset_nerve_props_matrix=np.array(
#                                                reset_nerve_props_matrix,
#                                                dtype=[('transmitter_release_sum',
#                                                        'float')]))


# def form_init_nerve():
#     return [
#         激励各个尺度各个方位的像素点,
#     ]
