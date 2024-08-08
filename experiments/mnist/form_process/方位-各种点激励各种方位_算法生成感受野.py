from consts.base import GRAY_IMG_PATH
from consts.feature import (
    ORIENT_SUM,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    global_axon_end_inds,
    ORIENT_SIDES,
)
from ...util import (
    get_soma_inds,
    save_axon_end_inds_with_new_nerves,
    get_around_and_center_hyper_col_inds_with_around_mask,
    get_orient_distance_matrix,
)
import numpy as np
import math
from ...form_nerve.form_nerve import form_nerve


def get_gray_matrix(orient, receptive_field_level):
    # matrix_shape = VISUAL_FIELD_WH + 1
    matrix_shape = (receptive_field_level, receptive_field_level)
    half_receptive_field_level = receptive_field_level // 2 + 1
    orient_range = 22.5
    base_axis = np.arange(-(matrix_shape[0] // 2), matrix_shape[0] // 2 + 1)

    orient_distance_ratio_matrix = get_orient_distance_matrix(
        orient, receptive_field_level, orient_range
    )

    receptive_field_level_matrix = np.array(
        [
            np.linalg.norm([x + np.sign(x), y + np.sign(y)])
            for y in base_axis[::-1]
            for x in base_axis
        ]
    ).reshape(matrix_shape)
    receptive_field_level_ratio_matrix = (
        np.maximum(
            0,
            half_receptive_field_level
            - np.abs(half_receptive_field_level - receptive_field_level_matrix),
        )
        / half_receptive_field_level
    )

    gray_matrix = orient_distance_ratio_matrix * receptive_field_level_ratio_matrix

    if half_receptive_field_level == 1:
        gray_matrix[matrix_shape[0] // 2, matrix_shape[0] // 2] = 1

    # # debug
    # gray_matrix = orient_distance_matrix
    # gray_matrix = receptive_field_level_matrix

    # gray_matrix[np.isnan(gray_matrix)] = 0
    return gray_matrix


gray_img_infos = {}
for orient_ind, orient in enumerate(ORIENTS):
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        gray_filefold_path = f"{GRAY_IMG_PATH}/d{receptive_field_level}"
        orient_img = math.ceil(orient) % 90 + 90
        rotate_time = orient // 90 - 1
        gray_img_path = f"{gray_filefold_path}/{orient_img}.jpg"
        gray_matrix = get_gray_matrix(orient, receptive_field_level)
        around_mask = gray_matrix > 0

        around_pos_inds, center_pos_inds, inrange_mother_pos_mask = (
            get_around_and_center_hyper_col_inds_with_around_mask(
                "点", f"方位-S{receptive_field_level}", around_mask
            )
        )

        # around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix = get_around_and_center_pos_inds_with_gray_img(
        #     '点',
        #     f'方位-S{receptive_field_level}',
        #     gray_img_path,
        #     gray_img_rotate_time=rotate_time)

        # 面向DAdd的axon_end_release_sum矩阵
        sum_gray_matrix = gray_matrix.astype(float)
        sum_gray_axon_end_release_sum_matrix = (
            sum_gray_matrix[np.newaxis, :, :]
            / 255
            * 65
            * inrange_mother_pos_mask.astype(int)
        )
        sum_gray_axon_end_mask = sum_gray_axon_end_release_sum_matrix > 0
        sum_gray_axon_end_release_sum = sum_gray_axon_end_release_sum_matrix[
            sum_gray_axon_end_mask
        ]

        # 面向DMax的axon_end_release_sum矩阵
        max_gray_matrix = gray_matrix.astype(float)
        # 把感知区域像素点的数值整体归一化到65
        max_gray_matrix *= 255 / np.max(max_gray_matrix)
        # 把感知区域像素点的数值整体归一化到65
        max_gray_axon_end_release_sum_matrix = (
            max_gray_matrix[np.newaxis, :, :]
            / 255
            * 65
            * inrange_mother_pos_mask.astype(int)
        )
        #
        max_gray_axon_end_release_sum = max_gray_axon_end_release_sum_matrix[
            max_gray_axon_end_release_sum_matrix > 0
        ]
        #
        gray_img_infos[(orient, receptive_field_level)] = (
            around_pos_inds,
            center_pos_inds,
            inrange_mother_pos_mask,
            gray_matrix,
            sum_gray_axon_end_release_sum,
            max_gray_axon_end_release_sum,
        )


def make激励轮廓方位(side):

    def 激励轮廓方位(cortex_obj):
        mother_inds, father_inds, axon_end_release_sums = [], [], []
        for orient_ind, orient in enumerate(ORIENTS):
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
                (
                    around_pos_inds,
                    center_pos_inds,
                    inrange_mother_pos_mask,
                    gray_matrix,
                    sum_gray_axon_end_release_sum,
                    max_gray_axon_end_release_sum,
                ) = gray_img_infos[(orient, receptive_field_level)]
                mother_orient = {
                    "内": ORIENTS[int((orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)],
                    "外": orient,
                }[side]
                mother_inds.extend(
                    get_soma_inds("点", f"{mother_orient}方向的边缘点", around_pos_inds)
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的{side}轮廓方位_DMax",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(max_gray_axon_end_release_sum)
        return form_nerve.make_new_nerve_packs(
            mother_inds,
            father_inds,
            cortex_obj,
            reset_nerve_props_matrix=np.array(
                axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
            ),
            new_nerve_callback=save_axon_end_inds_with_new_nerves(
                global_axon_end_inds, f"激励{side}轮廓方位"
            ),
        )

    return 激励轮廓方位


def 侧向边缘点末端抑制内轮廓方位(cortex_obj):
    """如果更大尺度上存在侧向边缘点，说明存在缺口，需要抑制这个内轮廓方位"""
    side = "内"
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level_ind, receptive_field_level in enumerate(
            RECEPTIVE_FIELD_LEVELS
        ):
            if receptive_field_level == RECEPTIVE_FIELD_LEVELS[-1]:
                continue
            (
                around_pos_inds,
                center_pos_inds,
                inrange_mother_pos_mask,
                gray_matrix,
                sum_gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
            ) = gray_img_infos[
                (orient, RECEPTIVE_FIELD_LEVELS[receptive_field_level_ind + 1])
            ]
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        "点",
                        f'{ORIENTS[int((orient_ind + {"左":-1,"右":1}[orient_side]*ORIENT_SUM  / 4) % ORIENT_SUM)]}方向的边缘点',
                        around_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的{side}轮廓方位_DMax抑制",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(max_gray_axon_end_release_sum)
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def 激励垂直方位(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            (
                around_pos_inds,
                center_pos_inds,
                inrange_mother_pos_mask,
                gray_matrix,
                sum_gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
            ) = gray_img_infos[(orient, receptive_field_level)]
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        "点",
                        f'{ORIENTS[int((orient_ind + {"左":-1,"右":1}[orient_side]*ORIENT_SUM  / 4) % ORIENT_SUM)]}方向的边缘点',
                        around_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的{orient_side}侧方位_DMax",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(max_gray_axon_end_release_sum)
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            global_axon_end_inds, "激励垂直方位"
        ),
    )


# def 内向边缘点末端抑制垂直方位(cortex_obj):
#     ''' 在将垂直方位用于感知缺口时，如果更大尺度上存在向内的边缘点，则说明这个缺口位于轮廓的内部，而不是一个真正的缺口 '''
#     ''' 这么做也会同时抑制住用于激励射线的垂直方位，可以改为在激励缺口直线时，用更大尺度的内轮廓方位来进行拮抗抑制 '''
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     for orient_ind, orient in enumerate(ORIENTS):
#         for receptive_field_level_ind,receptive_field_level in enumerate(RECEPTIVE_FIELD_LEVELS):
#             if receptive_field_level == RECEPTIVE_FIELD_LEVELS[-1]:
#                 continue
#             around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix, sum_gray_axon_end_release_sum, max_gray_axon_end_release_sum = gray_img_infos[
#                 (orient, RECEPTIVE_FIELD_LEVELS[receptive_field_level_ind+1])]
#             for orient_side in ORIENT_SIDES:
#                 mother_inds.extend(
#                     get_soma_inds(
#                         '点',
#                         f'{ORIENTS[int(
#                         (orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)]}方向的边缘点',
#                         around_pos_inds))
#                 father_inds.extend(
#                     get_soma_inds(f'方位-S{receptive_field_level}',
#                                   f'{orient}方向的{orient_side}侧方位_DMax抑制',
#                                       center_pos_inds))
#                 axon_end_release_sums.extend(max_gray_axon_end_release_sum)
#     return form_nerve.make_new_nerve_packs(
#         mother_inds,
#         father_inds,
#         cortex_obj,
#         reset_nerve_props_matrix=np.array(axon_end_release_sums,
#                                           dtype=[('transmitter_release_sum',
#                                                   'float')]),
#     )

# def 激励缺口方位(cortex_obj):
#     mother_inds, father_inds, axon_end_release_sums = [], [], []
#     for orient_ind, orient in enumerate(ORIENTS):
#         line_orient_ind = (orient_ind + ORIENT_SUM // 4) % (ORIENT_SUM // 2)
#         for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#             around_pos_inds, center_pos_inds, inrange_mother_pos_mask, gray_matrix, sum_gray_axon_end_release_sum, max_gray_axon_end_release_sum = gray_img_infos[
#                 (orient, receptive_field_level)]
#             for line_receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#                 mother_inds.extend(
#                     get_soma_inds(
#                         f'线_轮廓直线-S{line_receptive_field_level}',
#                         f'{BOTH_SIDE_ORIENT_DESC[line_orient_ind]}方向_内轮廓直线',
#                         around_pos_inds))
#                 father_inds.extend(
#                     get_soma_inds(f'方位-S{receptive_field_level}',
#                                   f'{orient}方位的缺口_DMax', center_pos_inds))
#                 ''' TODO 由于内轮廓直线受到尺度的影响，较小尺度的内轮廓直线的兴奋会更低，会进而削弱缺口方位的兴奋。
#                     为了消除这种影响，需要对axon_end_release_sum进行相应的反向的增强
#                 '''
#                 enlarge_axon_end_release_sum_ratio = 65 / min(
#                     65, 65 * ((line_receptive_field_level * 2) /
#                               RECEPTIVE_FIELD_LEVELS[-1]))
#                 axon_end_release_sums.extend(
#                     max_gray_axon_end_release_sum *
#                     enlarge_axon_end_release_sum_ratio)
#     return form_nerve.make_new_nerve_packs(
#         mother_inds,
#         father_inds,
#         cortex_obj,
#         reset_nerve_props_matrix=np.array(axon_end_release_sums,
#                                           dtype=[('transmitter_release_sum',
#                                                   'float')]),
#         new_nerve_callback=save_axon_end_inds_with_new_nerves(
#             global_axon_end_inds, '激励缺口方位'),
#     )


def 激励缺口方位(cortex_obj):
    """同时感知缺口处左右两侧的侧向边缘点，来表征缺口"""
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            (
                around_pos_inds,
                center_pos_inds,
                inrange_mother_pos_mask,
                gray_matrix,
                sum_gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
            ) = gray_img_infos[(orient, receptive_field_level)]
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        "点",
                        f'{ORIENTS[int((orient_ind + {"左":-1,"右":1}[orient_side]*ORIENT_SUM  / 4) % ORIENT_SUM)]}方向的边缘点',
                        around_pos_inds,
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        #   f'{orient}方位的缺口_DMax{orient_side}侧',
                        f"{orient}方位的缺口_DMax{orient_side}侧",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(max_gray_axon_end_release_sum)
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
        # new_nerve_callback=save_axon_end_inds_with_new_nerves(
        #     global_axon_end_inds, '激励缺口方位'),
    )


def 更大尺度的内向边缘点方位末端抑制缺口方位(cortex_obj):
    """同时感知缺口处左右两侧的侧向边缘点，来表征缺口"""
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            (
                around_pos_inds,
                center_pos_inds,
                inrange_mother_pos_mask,
                gray_matrix,
                sum_gray_axon_end_release_sum,
                max_gray_axon_end_release_sum,
            ) = gray_img_infos[(orient, receptive_field_level)]
            dot_orient_ind = int((orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)
            mother_inds.extend(
                get_soma_inds(
                    "点",
                    f"{ORIENTS[dot_orient_ind]}方向的边缘点",
                    around_pos_inds,
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}",
                    f"{orient}方位的缺口_DMax抑制",
                    center_pos_inds,
                )
            )
            axon_end_release_sums.extend(max_gray_axon_end_release_sum)
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


# def 更小尺度外轮廓方位抑制各种方位(cortex_obj):
#     mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
#     INNER_LOWER_LEVEL_SUM = 2
#     for orient in ORIENTS:
#         for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
#             ''' 由于对边缘方位的感知的机制，可能导致一种情况：
#                 某个感受野刚好处于一个较小的夹角内，例如2下部的角，使得外轮廓方位和内轮廓方位尺度刚好相等
#                 但此时向外的轮廓方位也应该算作更小尺度的方位，来抑制内轮廓直线
#             '''
#             inhibit_side = '外'
#             lower_levels = [
#                 receptive_field_level,
#                 *([
#                     level for level in RECEPTIVE_FIELD_LEVELS
#                     if level < receptive_field_level and level > 1
#                 ][-INNER_LOWER_LEVEL_SUM:]),
#             ]
#             for lower_level in lower_levels:
#                 mother_inds.extend(
#                     get_soma_inds(
#                         f'方位-S{lower_level}',
#                         [
#                             f'{ORIENTS[orient_ind]}方向的{inhibit_side}轮廓方位_A抑制',
#                         ] * 5,
#                     ))
#                 father_inds.extend(
#                     get_soma_inds(
#                         f'方位-S{receptive_field_level}',
#                         [
#                             f'{orient}方向的内轮廓方位',
#                             f'{orient}方向的外轮廓方位',
#                             f'{orient}方位的像素点',
#                             f'{orient}方位的缺口',
#                             f'{orient}方位的锐角',
#                         ],
#                     ))
#     return form_nerve.make_new_nerve_packs(mother_inds, father_inds,
#                                            cortex_obj)


def form_init_nerve():
    return [
        make激励轮廓方位("内"),
        侧向边缘点末端抑制内轮廓方位,
        make激励轮廓方位("外"),
        激励垂直方位,
        # 内向边缘点末端抑制垂直方位,
        # 激励缺口方位,
        # 更大尺度的内向边缘点方位末端抑制缺口方位,
        # 更小尺度外轮廓方位抑制各种方位,
    ]
