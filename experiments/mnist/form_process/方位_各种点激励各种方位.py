from consts.feature import (
    ORIENT_SUM,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    global_axon_end_inds,
    ORIENT_SIDES,
    BOTH_SIDE_ORIENT_DESC,
    LINE_RECEPTIVE_FIELD_LEVELS,
)
from ...util import (
    get_soma_inds,
    save_axon_end_inds_with_new_nerves,
    REGION,
    get_around_and_center_hyper_col_inds_with_around_mask,
    get_orient_distance_matrix,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def get_gray_matrix(
    orient, receptive_field_level, orient_range=None, receptive_field_level_range=None
):

    if orient_range == None:
        orient_range = 25
    if receptive_field_level_range == None:
        receptive_field_level_range = 2

    matrix_shape = (receptive_field_level, receptive_field_level)
    half_receptive_field_level = receptive_field_level // 2 + 1
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
            receptive_field_level_range
            - np.abs(half_receptive_field_level - receptive_field_level_matrix),
        )
        / receptive_field_level_range
    )

    ratio_matrix = orient_distance_ratio_matrix * receptive_field_level_ratio_matrix
    # ratio_matrix = orient_distance_ratio_matrix # 生成连续尺度的感受野

    # 对尺度为1的灰度图要做特殊处理，灰度默认设为1
    if half_receptive_field_level == 1:
        ratio_matrix[matrix_shape[0] // 2, matrix_shape[0] // 2] = 1

    gray_matrix = 255 * ratio_matrix
    max_gray_matrix = 255 * gray_matrix / np.max(gray_matrix)
    sum_gray_matrix = 255 * gray_matrix / np.sum(gray_matrix)

    return gray_matrix, max_gray_matrix, sum_gray_matrix


# matrix_list = [
#     get_gray_matrix(
#         orient,
#         receptive_field_level,
#         # orient_range=45,
#         # receptive_field_level_range=5,
#     )[0].tolist() for orient_ind, orient in enumerate(ORIENTS)
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS[1:]
# ]

# matrix_list = [
#     get_gray_matrix(
#         orient,
#         receptive_field_level,
#     )[2].tolist() for orient_ind, orient in enumerate(ORIENTS)
#     for receptive_field_level in [3]
# ]

# matrix_list = [
#     get_gray_matrix(
#         orient,
#         receptive_field_level,
#     )[0].tolist() for orient in [45]
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS
# ]


def filter_matrix(matrix):
    matrix[matrix <= 255 / 2] = 0
    return matrix


def fix_size(matrix, targ_size):
    new_matrix = np.full((targ_size, targ_size), 0)
    matrix_size = matrix.shape[0]
    start_pos = (targ_size - matrix_size) // 2
    new_matrix[
        start_pos : start_pos + matrix_size, start_pos : start_pos + matrix_size
    ] = matrix
    return new_matrix


# # 生成方位感受野数据
# matrix_list = {
#     str(receptive_field_level): {
#         str(orient):
#             get_gray_matrix(
#                 orient,
#                 receptive_field_level,
#                 # orient_range=45,
#                 # receptive_field_level_range=2,
#             )[1].tolist()
#         for orient in ORIENTS[8:12]
#         # for orient in ORIENTS
#     }
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS[7:8]
#     # for receptive_field_level in RECEPTIVE_FIELD_LEVELS
# }

# # 生成射线感受野数据
# matrix_list = {
#     str(receptive_field_level): {
#         str(orient): functools.reduce(
#             lambda a, b: np.maximum(a, b),
#             [
#                     fix_size(
#                         get_gray_matrix(
#                             orient,
#                             level,
#                         )[0],
#                         15) for level in RECEPTIVE_FIELD_LEVELS
#                 if level <= receptive_field_level
#             ]).tolist()
#         for orient in ORIENTS[8:12]
#         # for orient in ORIENTS
#     }
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS[7:8]
#     # for receptive_field_level in RECEPTIVE_FIELD_LEVELS
# }

# # 生成内轮廓直线感受野数据
# matrix_list = {
#     str(receptive_field_level): {
#         str(orient): np.maximum(
#             get_gray_matrix(
#                 orient,
#                 receptive_field_level,
#             )[1],
#             get_gray_matrix(
#                 (orient + 180) % 360.,
#                 receptive_field_level,
#             )[1],
#         ).tolist()
#         for orient in ORIENTS[8:12]
#         # for orient in ORIENTS
#     }
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS[7:8]
#     # for receptive_field_level in RECEPTIVE_FIELD_LEVELS
# }

# # 生成角的感受野数据
# matrix_list = {
#     str(receptive_field_level): {
#         str(orient): np.maximum(
#             functools.reduce(
#             lambda a, b: np.maximum(a, b),
#             [
#                     fix_size(
#                         get_gray_matrix(
#                             orient,
#                             level,
#                         )[0],
#                         21) for level in RECEPTIVE_FIELD_LEVELS
#                 if level <= receptive_field_level
#             ]),
#             functools.reduce(
#             lambda a, b: np.maximum(a, b),
#             [
#                     fix_size(
#                         get_gray_matrix(
#                             (orient+angle)%360.,
#                             level,
#                         )[0],
#                         21) for level in RECEPTIVE_FIELD_LEVELS
#                 if level <= receptive_field_level
#             ]),
#         ).tolist()
#         for orient, angle in zip(ORIENTS[8:12], ANGLES[1:5])
#         # for orient in ORIENTS
#     }
#     for receptive_field_level in RECEPTIVE_FIELD_LEVELS[10:]
#     # for receptive_field_level in RECEPTIVE_FIELD_LEVELS
# }

# # 生成圆弧感受野数据
# matrix_list = {
#     str(orient): {
#         str(receptive_field_level):
#         functools.reduce(lambda a, b: np.maximum(a, b), [
#             fix_size(get_gray_matrix(
#                 ori,
#                 level,
#             )[1], receptive_field_level) for ori in ORIENTS
#             for level in RECEPTIVE_FIELD_LEVELS
#             if level <= receptive_field_level
#         ]).tolist()
#         for receptive_field_level in RECEPTIVE_FIELD_LEVELS[7:11]
#     }
#     for orient in ORIENTS[0:1]
# }

# fo = open(
#     "/Users/laola/CodeProject/Orangutan/vue_server/src/data/orient_receptive.json",
#     "w")
# fo.write(json.dumps(matrix_list))
# fo.close()


def get_gray_axon_end_release_sum(
    gray_matrix, max_gray_matrix, sum_gray_matrix, inrange_mother_pos_mask
):
    gray_axon_end_release_sum_matrix = (
        gray_matrix[np.newaxis, :, :] / 255 * 65 * inrange_mother_pos_mask.astype(int)
    )
    gray_axon_end_release_sum = gray_axon_end_release_sum_matrix[
        gray_axon_end_release_sum_matrix > 0
    ]

    max_gray_axon_end_release_sum_matrix = (
        max_gray_matrix[np.newaxis, :, :]
        / 255
        * 65
        * inrange_mother_pos_mask.astype(int)
    )
    max_gray_axon_end_release_sum = max_gray_axon_end_release_sum_matrix[
        max_gray_axon_end_release_sum_matrix > 0
    ]

    sum_gray_axon_end_release_sum_matrix = (
        sum_gray_matrix[np.newaxis, :, :]
        / 255
        * 65
        * inrange_mother_pos_mask.astype(int)
    )
    sum_gray_axon_end_release_sum = sum_gray_axon_end_release_sum_matrix[
        sum_gray_axon_end_release_sum_matrix > 0
    ]

    return (
        gray_axon_end_release_sum,
        max_gray_axon_end_release_sum,
        sum_gray_axon_end_release_sum,
    )


def get_receptive_field_infos(
    orient, receptive_field_level, orient_range=None, receptive_field_level_range=None
):
    gray_matrix, max_gray_matrix, sum_gray_matrix = get_gray_matrix(
        orient,
        receptive_field_level,
        orient_range=orient_range,
        receptive_field_level_range=receptive_field_level_range,
    )
    around_pos_inds, center_pos_inds, inrange_mother_pos_mask = (
        get_around_and_center_hyper_col_inds_with_around_mask(
            "点", f"方位-S{receptive_field_level}", max_gray_matrix > 255 / 2
        )
    )
    (
        gray_axon_end_release_sum,
        max_gray_axon_end_release_sum,
        sum_gray_axon_end_release_sum,
    ) = get_gray_axon_end_release_sum(
        gray_matrix, max_gray_matrix, sum_gray_matrix, inrange_mother_pos_mask
    )
    return (
        around_pos_inds,
        center_pos_inds,
        gray_axon_end_release_sum,
        max_gray_axon_end_release_sum,
        sum_gray_axon_end_release_sum,
    )


def 激励轮廓方位(side):

    def 激励函数(cortex_obj):
        mother_inds, father_inds, axon_end_release_sums = [], [], []
        for orient_ind, orient in enumerate(ORIENTS):
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
                (
                    around_pos_inds,
                    center_pos_inds,
                    gray_axon_end_release_sum,
                    _,
                    _,
                ) = get_receptive_field_infos(orient, receptive_field_level)

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
                axon_end_release_sums.extend(gray_axon_end_release_sum)
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

    return 激励函数


def 激励轮廓方位_求和(side):

    def 激励函数(cortex_obj):
        mother_inds, father_inds, axon_end_release_sums = [], [], []
        for orient_ind, orient in enumerate(ORIENTS):
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:

                (
                    around_pos_inds,
                    center_pos_inds,
                    gray_axon_end_release_sum,
                    _,
                    _,
                ) = get_receptive_field_infos(orient, receptive_field_level)

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
                        f"{orient}方向的{side}轮廓方位_求和",
                        center_pos_inds,
                    )
                )
                axon_end_release_sums.extend(gray_axon_end_release_sum)
        return form_nerve.make_new_nerve_packs(
            mother_inds,
            father_inds,
            cortex_obj,
            reset_nerve_props_matrix=np.array(
                axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
            ),
        )

    return 激励函数


def 汇总内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            if receptive_field_level == 1:
                continue
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}", f"{orient}方向的内轮廓方位"
                )
            )
            father_inds.extend(
                get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_DMax")
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总尺度为1的内轮廓方位(cortex_obj):
    """
    角点处存在尺度为1的轮廓中心，不希望被模型注意到
    同时一些内径较小的圆圈处也存在尺度为1的轮廓中心，希望被模型注意到
    因此需要单独汇总尺度为1的内轮廓方位，并用该位置上的射线细胞对其进行抑制
    """
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        mother_inds.extend(get_soma_inds(f"方位-S1", f"{orient}方向的内轮廓方位"))
        father_inds.extend(get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_DMax"))
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            global_axon_end_inds, "汇总尺度为1的内轮廓方位"
        ),
    )


def 汇总所有方向的射线的最大值(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"线_射线-S{receptive_field_level}",
                        f"{orient}方向{orient_side}侧的射线_A步长2的激励",
                    )
                )
                father_inds.extend(
                    get_soma_inds(f"线_射线", f"汇总所有射线的最大值_DMax")
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励并维持汇总所有射线自突触(cortex_obj):
    mother_inds, father_inds = [], []
    mother_inds.extend(
        get_soma_inds(
            f"线_射线",
            [
                f"汇总所有射线的最大值_A步长0的激励",  # 步长2是为了等射线兴奋稳定了再激励自突触细胞
                f"汇总所有射线的最大值_自突触",
            ],
        )
    )
    father_inds.extend(
        get_soma_inds(f"线_射线", [f"汇总所有射线的最大值_自突触_DMax"] * 2)
    )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 所有射线抑制汇总尺度为1的内轮廓方位_自突触(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        mother_inds.extend(
            get_soma_inds(f"线_射线", f"汇总所有射线的最大值_自突触_A抑制")
        )
    father_inds = global_axon_end_inds["汇总尺度为1的内轮廓方位"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总对侧内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    side = "内"
    for orient_ind in range(ORIENT_SUM // 2):
        mother_inds.extend(
            get_soma_inds(
                f"方位",
                [
                    f"汇总{ORIENTS[orient_ind]}方向的{side}轮廓方位",
                    f"汇总{ORIENTS[(orient_ind+ORIENT_SUM//2)%ORIENT_SUM]}方向的{side}轮廓方位",
                ],
            )
        )
        father_inds.extend(
            get_soma_inds(
                f"方位",
                [
                    f"汇总{BOTH_SIDE_ORIENT_DESC[orient_ind]}方向的内轮廓方位_DMax",
                ]
                * 2,
            )
        )

    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
    )


def 激励内轮廓方位复杂细胞(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            for sub_receptive_field_level in [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if abs(level - receptive_field_level) <= 2
            ]:
                """
                用指数来计算兴奋比例会导致方差太大，不利于鲁棒性
                """
                receptive_field_level_ratio = (
                    max(
                        0,
                        receptive_field_level
                        - abs(receptive_field_level - sub_receptive_field_level),
                    )
                    / receptive_field_level
                )
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{sub_receptive_field_level}",
                        f"{orient}方向的内轮廓方位",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的内轮廓方位_复杂细胞_DMax",
                    )
                )
                axon_end_release_sums.extend(
                    [65 * receptive_field_level_ratio]
                    * REGION[f"方位-S{receptive_field_level}"]["hyper_col_sum"]
                )
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
                gray_axon_end_release_sum,
                _,
                _,
            ) = get_receptive_field_infos(orient, receptive_field_level)

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
                axon_end_release_sums.extend(gray_axon_end_release_sum)
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


def 更小尺度外轮廓方位抑制内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    inhibit_side = "外"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            """最小抑制尺度要大于1，不然会出现9_1中那样，【方位-S13】90.0方向的内轮廓方位被尺度1的外轮廓抑制的情况，见下图
            file:///Users/laola/CodeProject/Orangutan/vue_server/src/assets/imgs/screenshot/Snipaste_2023-07-29_09-34-53.png
            """
            """ 抑制方位需要包括同尺度的外轮廓方位，因为外轮廓方位是由更低一级感受野的像素点激励的，而内轮廓方位是由更高一级的感受野激励的，
                所以同级的内外轮廓方位之间，其实存在隔了一级的像素点
            """
            lower_levels = [
                lower_level
                for lower_level in RECEPTIVE_FIELD_LEVELS
                if lower_level <= receptive_field_level and lower_level > 1
            ]
            for lower_level in lower_levels:
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{lower_level}",
                        f"{orient}方向的{inhibit_side}轮廓方位_自突触",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的内轮廓方位_DMax抑制",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 更小尺度内轮廓方位抑制内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    inhibit_side = "内"
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            lower_levels = [
                lower_level
                for lower_level in RECEPTIVE_FIELD_LEVELS
                if lower_level
                < (
                    receptive_field_level - 2
                )  # 在某些case下(3_8,Arc_{y=22,x=16})，尺度为1的内轮廓方位对于抑制更大尺度的内轮廓方位有关键作用，不能将其排除在外
                #   2) and lower_level > 1
            ]
            for lower_level in lower_levels:
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{lower_level}",
                        f"{orient}方向的{inhibit_side}轮廓方位_自突触",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"{orient}方向的内轮廓方位_DMax内轮廓抑制",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总尺度内的内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
        for orient in ORIENTS:
            for level in [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if level <= receptive_field_level
            ]:
                mother_inds.extend(
                    get_soma_inds(f"方位-S{level}", f"{orient}方向的内轮廓方位")
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"汇总{orient}方向尺度内的内轮廓方位_DMax",
                    )
                )
                #
                mother_inds.extend(
                    get_soma_inds(f"方位-S{level}", f"{orient}方向的内轮廓方位_求和")
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        f"汇总{orient}方向尺度内的内轮廓方位_求和_DMax",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def STD激励内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, _, _, _, _ = get_receptive_field_infos(
                orient, receptive_field_level
            )
            mother_orient = ORIENTS[int((orient_ind + ORIENT_SUM // 2) % ORIENT_SUM)]
            mother_inds.extend(
                get_soma_inds(
                    "点", f"{mother_orient}方向的边缘点_反馈_ASTD", around_pos_inds
                )
            )
    father_inds = global_axon_end_inds[f"激励内轮廓方位"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def STD激励垂直方位(cortex_obj):
    mother_inds, father_inds = [], []
    for orient_ind, orient in enumerate(ORIENTS):
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            around_pos_inds, _, _, _, _ = get_receptive_field_infos(
                orient, receptive_field_level
            )
            for orient_side in ORIENT_SIDES:
                mother_orient = ORIENTS[
                    int(
                        (orient_ind + {"左": -1, "右": 1}[orient_side] * ORIENT_SUM / 4)
                        % ORIENT_SUM
                    )
                ]
                mother_inds.extend(
                    get_soma_inds(
                        "点", f"{mother_orient}方向的边缘点_反馈_ASTD", around_pos_inds
                    )
                )
    father_inds = global_axon_end_inds[f"激励垂直方位"]
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励并维持自突触轮廓方位(side):

    def 激励函数(cortex_obj):
        mother_inds, father_inds = [], []
        for orient in ORIENTS:
            for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
                mother_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        [
                            # 轮廓方位一有兴奋的时候就激励自突触，此时自突触保存的是最一开始没有受到抑制的内轮廓方位兴奋，可以如实地反应相关内轮廓边缘点的分布情况
                            f"{orient}方向的{side}轮廓方位_A步长0的激励",
                            f"{orient}方向的{side}轮廓方位_自突触",
                        ],
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"方位-S{receptive_field_level}",
                        [f"{orient}方向的{side}轮廓方位_自突触_DMax"] * 2,
                    )
                )
        return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)

    return 激励函数


def 激励并维持自突触汇总内轮廓方位(cortex_obj):
    mother_inds, father_inds = [], []
    for orient in ORIENTS:
        for receptive_field_level in RECEPTIVE_FIELD_LEVELS:
            if receptive_field_level == 1:
                continue
            mother_inds.extend(
                get_soma_inds(
                    f"方位-S{receptive_field_level}", f"{orient}方向的内轮廓方位_自突触"
                )
            )
            father_inds.extend(
                get_soma_inds(f"方位", f"汇总{orient}方向的内轮廓方位_自突触_DMax")
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        # ''' 激励圆弧相关的方位 '''
        激励轮廓方位("内"),
        激励轮廓方位("外"),
        激励轮廓方位_求和("内"),
        # 激励轮廓方位_求和("外"),
        # ''' 汇总 '''
        激励内轮廓方位复杂细胞,
        汇总内轮廓方位,
        汇总对侧内轮廓方位,
        汇总尺度内的内轮廓方位,
        # ''' 特殊逻辑：单独汇总和抑制尺度为1的内轮廓方位 '''
        汇总尺度为1的内轮廓方位,
        汇总所有方向的射线的最大值,
        激励并维持汇总所有射线自突触,
        所有射线抑制汇总尺度为1的内轮廓方位_自突触,
        # 抑制作用
        更小尺度外轮廓方位抑制内轮廓方位,
        更小尺度内轮廓方位抑制内轮廓方位,
        激励并维持自突触轮廓方位("内"),
        激励并维持自突触轮廓方位("外"),
        激励并维持自突触汇总内轮廓方位,
        # ''' 负反馈调节 '''
        STD激励内轮廓方位,
        # ''' 垂直方位 '''
        激励垂直方位,
        STD激励垂直方位,
    ]
