form_data = [
    (0, [
        ('类型', '轮廓中心'),
        ('相对整体的方位', None),
        ('相对锚点的方位', None),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', '15'),
        ('相对整体中心的距离', 1),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', '0.1'),
    ]),
    # (-0.1, [
    #     ('类型', '轮廓中心'),
    #     ('相对整体的方位', '360.0-泛化'),
    #     ('朝向', '45.0-泛化'),
    #     ('尺度', '13'),
    # ]),
    # (-0.1, [
    #     ('类型', '角'),
    #     ('相对整体的方位', '270.0-泛化'),
    #     ('朝向', '45.0-泛化'),
    #     ('尺度', '13'),
    # ]),
    # (1, [
    #     ('类型', '角'),
    #     ('朝向', '90.0'),
    #     ('角度', '157.5'),
    #     ('尺度', '19-泛化'),
    #     ('相对整体中心的距离', '3'),
    #     ('相对整体中心的距离相对整体尺度的比例', '0.1'),
    # ]),
    # (1, [
    #     ('类型', '角'),
    #     ('朝向', '270.0'),
    #     ('角度', '157.5'),
    #     ('尺度', '19-泛化'),
    #     ('相对整体中心的距离', '3'),
    #     ('相对整体中心的距离相对整体尺度的比例', '0.1'),
    # ]),
    # (2, [
    #     ('相对_相对整体的方位_的朝向', '225.0'),
    #     ('角度', '67.5-泛化'),
    #     ('相对整体中心的距离', '7'),
    #     ('相对整体中心的距离相对整体尺度的比例', '0.3'),
    # ], [
    #     ('相对_相对整体的方位_的朝向', '225.0'),
    #     ('角度', '67.5-泛化'),
    #     ('相对整体中心的距离', '7'),
    #     ('相对整体中心的距离相对整体尺度的比例', '0.3'),
    # ]),
    # (
    #     3,
    #     [
    #         ('相对整体的方位', '180.0-泛化'),
    #         ('相对锚点的方位', '180.0-泛化'),
    #         # ('朝向', '315.0'),
    #         ('相对_相对整体的方位_的朝向', '112.5-泛化'),
    #         ('相对_相对锚点的方位_的朝向', '112.5-泛化'),
    #         ('角度', '67.5'),
    #         # ('尺度', '11'),
    #         ('相对整体中心的距离', '5-泛化'),
    #         ('相对整体中心的距离相对整体尺度的比例', '0.2-泛化'),
    #     ],
    #     [
    #         ('相对整体的方位', '360.0-泛化'),
    #         # ('朝向', '225.0'),
    #         ('相对_相对整体的方位_的朝向', '247.5-泛化'),
    #         ('角度', '67.5'),
    #         # ('尺度', '11'),
    #         ('相对整体中心的距离', '5-泛化'),
    #         ('相对整体中心的距离相对整体尺度的比例', '0.2-泛化'),
    #     ]),
    # (
    #     3,
    #     [
    #         ('相对整体的方位', '360.0-泛化'),
    #         ('相对锚点的方位', '360.0-泛化'),
    #         # ('朝向', '225.0'),
    #         ('相对_相对整体的方位_的朝向', '247.5-泛化'),
    #         ('相对_相对锚点的方位_的朝向', '247.5-泛化'),
    #         ('角度', '67.5'),
    #         # ('尺度', '11'),
    #         ('相对整体中心的距离', '5-泛化'),
    #         ('相对整体中心的距离相对整体尺度的比例', '0.2-泛化'),
    #     ],
    #     [
    #         ('相对整体的方位', '180.0-泛化'),
    #         # ('朝向', '315.0'),
    #         ('相对_相对整体的方位_的朝向', '112.5-泛化'),
    #         ('角度', '67.5'),
    #         # ('尺度', '11'),
    #         ('相对整体中心的距离', '5-泛化'),
    #         ('相对整体中心的距离相对整体尺度的比例', '0.2-泛化'),
    #     ]),
    # (
    #     4,
    #     [
    #         ('类型', '轮廓中心'),
    #         ('相对锚点的方位', '360.0-泛化'),
    #         ('朝向', '360.0-泛化'),
    #         ('相对_相对锚点的方位_的朝向', '360.0-泛化'),
    #         ('尺度', '9'),
    #         ('相对整体中心的距离', '3'),
    #         ('相对锚点的距离', '7'),
    #         ('相对整体中心的距离相对整体尺度的比例', '0.2'),
    #     ],
    #     [
    #         # TODO
    #         ('相对_相对整体的方位_的朝向', '45.0'),
    #     ]),
    # (4, [
    #     ('相对_相对整体的方位_的朝向', '45.0'),
    # ], [
    #     ('相对_相对整体的方位_的朝向', '22.5'),
    # ]),
    # (5, [
    #     ('相对_相对整体的方位_的朝向', '135.0'),
    # ], [
    #     ('相对_相对整体的方位_的朝向', '135.0'),
    # ]),

    # 上弧-下圆
    ((6, -0.1), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0'),
        ('相对锚点的方位', None),
        ('朝向', '45.0'),
        ('相对_相对整体的方位_的朝向', '45.0'),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', '67.5'),
        ('尺度', 11),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', 7),
        ('相对整体中心的距离相对整体尺度的比例', '0.2'),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0'),
        ('相对锚点的方位', '180.0'),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', 15),
        ('相对整体中心的距离', 7),
        ('相对锚点的距离', 11),
        ('相对整体中心的距离相对整体尺度的比例', '0.3'),
    ]),
    # 下圆-上弧
    ((6, -0.1), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0'),
        ('相对锚点的方位', None),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0'),
        ('相对锚点的方位', '360.0'),
        ('朝向', '45.0'),
        ('相对_相对整体的方位_的朝向', '45.0'),
        ('相对_相对锚点的方位_的朝向', '45.0'),
        ('角度', None),
        ('尺度', '13'),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ]),
    ((6, -0.1), [
        ('类型', '角'),
        ('相对整体的方位', '270.0'),
        ('朝向', '45.0'),
        ('尺度', '13'),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0'),
        ('相对锚点的方位', '135.0'),
        ('朝向', '无'),
    ]),
    ((6, -0.1), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('朝向', '无'),
    ], [
        ('类型', '角'),
        ('相对整体的方位', '270.0-泛化'),
        ('相对锚点的方位', '315.0-泛化'),
        ('朝向', '45.0-泛化'),
        ('相对_相对整体的方位_的朝向', '135.0-泛化'),
        ('相对_相对锚点的方位_的朝向', '90.0-泛化'),
        ('尺度', '13'),
    ]),
    # (7, [
    #     ('相对_相对整体的方位_的朝向', '225.0'),
    # ]),
    # (-7, [
    #     ('朝向', '45.0'),
    #     ('相对整体中心的距离相对整体尺度的比例', '0.3'),
    # ]),
    # 上圆-叉-下圆
    ((8, -0.1, -6), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0-泛化'),
        ('相对锚点的方位', None),
        ('朝向', None),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '叉'),
        ('相对整体的方位', None),
        ('相对锚点的方位', '180.0-泛化'),
        ('朝向', '90.0'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', '270.0'),
        ('角度', '90.0'),
        ('尺度', None),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', 5),
        ('相对整体中心的距离相对整体尺度的比例', .2),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('相对锚点的方位', '180.0-泛化'),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ]),
    # 上圆-下圆-叉
    ((8, -0.1, -6), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0-泛化'),
        ('相对锚点的方位', None),
        ('朝向', None),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('相对锚点的方位', '180.0-泛化'),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '叉'),
        ('相对整体的方位', None),
        ('相对锚点的方位', '360.0-泛化'),
        ('朝向', '90.0'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', '90.0'),
        ('角度', '90.0'),
        ('尺度', None),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', 5),
        ('相对整体中心的距离相对整体尺度的比例', .2),
    ]),
    # 叉-上圆-下圆
    ((8, -0.1, -6), [
        ('类型', '叉'),
        ('相对整体的方位', None),
        ('相对锚点的方位', None),
        ('朝向', '90.0'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', '90.0'),
        ('尺度', None),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', .2),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0-泛化'),
        ('相对锚点的方位', '360.0-泛化'),
        ('朝向', None),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('相对锚点的方位', '180.0-泛化'),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ]),
    # 叉-下圆-上圆
    ((8, -0.1, -6), [
        ('类型', '叉'),
        ('相对整体的方位', None),
        ('相对锚点的方位', None),
        ('朝向', '90.0'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', '90.0'),
        ('尺度', None),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', .2),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('相对锚点的方位', '180.0-泛化'),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0-泛化'),
        ('相对锚点的方位', '360.0-泛化'),
        ('朝向', None),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ]),
    # 下圆-上圆-叉
    ((8, -0.1, -6), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('相对锚点的方位', None),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0-泛化'),
        ('相对锚点的方位', '360.0-泛化'),
        ('朝向', None),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '叉'),
        ('相对整体的方位', None),
        ('相对锚点的方位', '180.0-泛化'),
        ('朝向', '90.0'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', '270.0'),
        ('角度', '90.0'),
        ('尺度', None),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', .2),
    ]),
    # 下圆-叉-上圆
    ((8, -0.1, -6), [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '180.0-泛化'),
        ('相对锚点的方位', None),
        ('朝向', '无'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ], [
        ('类型', '叉'),
        ('相对整体的方位', None),
        ('相对锚点的方位', '360.0-泛化'),
        ('朝向', '90.0'),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', '90.0'),
        ('角度', '90.0'),
        ('尺度', None),
        ('相对整体中心的距离', 3),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', .2),
    ], [
        ('类型', '轮廓中心'),
        ('相对整体的方位', '360.0-泛化'),
        ('相对锚点的方位', '360.0-泛化'),
        ('朝向', None),
        ('相对_相对整体的方位_的朝向', None),
        ('相对_相对锚点的方位_的朝向', None),
        ('角度', None),
        ('尺度', None),
        ('相对整体中心的距离', None),
        ('相对锚点的距离', None),
        ('相对整体中心的距离相对整体尺度的比例', None),
    ]),
    # (9, [
    #     ('相对_相对整体的方位_的朝向', '无'),
    # ], [
    #     ('相对_相对整体的方位_的朝向', '45.0'),
    # ]),
    # (9, [
    #     ('相对_相对整体的方位_的朝向', '45.0'),
    # ], [
    #     ('相对_相对整体的方位_的朝向', '无'),
    # ]),
]