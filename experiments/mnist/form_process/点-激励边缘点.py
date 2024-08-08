from consts.feature import ORIENTS, ORIENT_SUM
from ...util import (
    get_soma_inds,
    get_around_and_center_hyper_col_inds_with_around_mask,
    get_orient_distance_matrix,
)
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def 激励各个方向的边缘点(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient_ind, orient in enumerate(ORIENTS):
        """
        将激励边缘点的像素范围限制在45度以内，是希望当特征只有一个像素宽度的时候，依然可以像人一样，以较高的兴奋激励边缘点，进而有效地感知缺口等特征
        如果用90度的范围，一个边缘点就会需要3个像素点共同激励，不利于感知较细的特征
        """
        orient_distance_ratio_matrix = get_orient_distance_matrix(
            ORIENTS[(orient_ind + ORIENT_SUM // 2) % ORIENT_SUM], 3, 45.0
        )
        orient_distance_ratio_matrix /= np.sum(orient_distance_ratio_matrix)
        around_pos_inds, center_pos_inds, inrange_around_pos_mask = (
            get_around_and_center_hyper_col_inds_with_around_mask(
                "点", "点", orient_distance_ratio_matrix > 0
            )
        )
        this_mother_inds = get_soma_inds("点", "input", around_pos_inds)
        mother_inds.extend(this_mother_inds)
        father_inds.extend(
            get_soma_inds("点", f"{orient}方向的边缘点", center_pos_inds)
        )
        axon_end_release_sum = np.tile(
            65 * orient_distance_ratio_matrix, (inrange_around_pos_mask.shape[0], 1, 1)
        )[inrange_around_pos_mask]
        reset_nerve_props_matrix.extend(
            np.repeat(
                axon_end_release_sum,
                this_mother_inds.size // np.sum(inrange_around_pos_mask),
            )
        )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            reset_nerve_props_matrix, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def 边缘点处的像素抑制边缘点(cortex_obj):
    mother_inds, father_inds, reset_nerve_props_matrix = [], [], []
    for orient in ORIENTS:
        mother_inds.extend(get_soma_inds("点", "input_A抑制"))
        father_inds.extend(get_soma_inds("点", f"{orient}方向的边缘点"))
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        激励各个方向的边缘点,
        边缘点处的像素抑制边缘点,
    ]
