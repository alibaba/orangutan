from consts.feature import (
    ANGLE_NAMES,
    CONTOUR_SIDES,
)
from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs
LOOP_PROPS = [
    (feature_type, feature_name)
    for feature_type in ["角", "轮廓中心"]
    for feature_name in {
        "角": ANGLE_NAMES,
        "轮廓中心": [f"{side}轮廓中心" for side in CONTOUR_SIDES],
    }[feature_type]
]


def 激励注意力竞争(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(
            get_soma_inds(
                feature_type,
                f"{feature_name}",
            )
        )
        father_inds.extend(get_soma_inds(feature_type, f"{feature_name}的注意力竞争"))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 注意力竞争兴奋汇总(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(get_soma_inds(feature_type, f"{feature_name}的注意力竞争"))
        father_inds.extend(
            np.tile(
                get_soma_inds(
                    "全局调控",
                    f"注意力竞争兴奋汇总{'-外轮廓中心' if feature_name == '外轮廓中心' else ''}_DMax",
                ),
                REGION[feature_type]["hyper_col_sum"],
            )
        )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 控制注意力竞争开始时机(cortex_obj):
    """为什么要控制时机？为了避免竞争兴奋汇总后马上就抑制住了还在积累步长的竞争细胞"""
    mother_inds, father_inds = [], []
    mother_inds.extend(
        get_soma_inds(f"全局调控", f"公用调控兴奋_A控制注意力竞争开始时机")
    )
    father_inds.extend(get_soma_inds("全局调控", f"注意力竞争兴奋汇总_DMin"))
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励注意力竞争结果(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(
            get_soma_inds(
                feature_type,
                f'{feature_name}_A步长{({ "轮廓中心":2, "角":3, }[feature_type])+2}的激励',
            )
        )
        father_inds.extend(
            get_soma_inds(feature_type, f"{feature_name}的注意力竞争结果")
        )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "激励注意力竞争结果"
        ),
    )


def 禁止激励注意力竞争结果(cortex_obj):
    mother_inds, father_inds = [], []
    for feature_type, feature_name in LOOP_PROPS:
        mother_inds.extend(
            np.tile(
                get_soma_inds(
                    "全局调控",
                    f"注意力竞争兴奋汇总{'-外轮廓中心' if feature_name == '外轮廓中心' else ''}_A全或无弱抑制",
                ),
                REGION[feature_type]["hyper_col_sum"],
            )
        )
        father_inds.extend(
            get_soma_inds(
                feature_type,
                f'{feature_name}_A步长{({ "轮廓中心":2, "角":3, }[feature_type])+2}的激励',
            )
        )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励注意力竞争,
        注意力竞争兴奋汇总,
        控制注意力竞争开始时机,
        激励注意力竞争结果,
        禁止激励注意力竞争结果,
    ]
