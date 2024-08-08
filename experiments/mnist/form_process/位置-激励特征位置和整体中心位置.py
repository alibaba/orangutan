from consts.feature import (
    ANGLE_NAMES,
    FEATURE_TYPES,
)
from ...util import (
    get_soma_inds,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def 归纳特征激励特征位置和整体中心位置(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type in FEATURE_TYPES:
        for feature_name in {
            "角": ANGLE_NAMES,
            "轮廓中心": ["内轮廓中心", "外轮廓中心"],
        }[feature_type]:
            this_mother_inds = get_soma_inds(
                feature_type, f"{feature_name}的注意力竞争结果"
            )
            mother_inds.extend(np.tile(this_mother_inds, 2))
            father_region_name = (
                "位置_整体中心" if feature_name == "外轮廓中心" else "位置_当前特征"
            )
            father_inds.extend(
                get_soma_inds(
                    father_region_name,
                    [
                        f"{y}"
                        for y in (
                            cortex_obj.cortex["region_row_no"][this_mother_inds] - 1
                        )
                    ],
                    0,
                )
            )
            father_inds.extend(
                get_soma_inds(
                    father_region_name,
                    [
                        f"{x}"
                        for x in (
                            cortex_obj.cortex["region_hyper_col_no"][this_mother_inds]
                            - 1
                        )
                    ],
                    1,
                )
            )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        归纳特征激励特征位置和整体中心位置,
    ]
