from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ORIENT_SIDES,
)
from ...util import get_soma_inds
import numpy as np
from ...form_nerve.form_nerve import form_nerve

make_new_nerve_packs = form_nerve.make_new_nerve_packs
axon_end_inds = {}
prop_pack_list = [
    (orient_side, orient, receptive_field_level)
    for orient_side in ORIENT_SIDES
    for orient in ORIENTS
    for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS
]


def ray_feedback_excitation_vertical_orientation(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side, orient, receptive_field_level in prop_pack_list:
        add_levels = np.array(
            [
                level
                for level in RECEPTIVE_FIELD_LEVELS
                if level <= receptive_field_level
            ]
        )
        for add_level in add_levels:
            mother_inds.extend(
                get_soma_inds(
                    f"ray-S{receptive_field_level}",
                    f"rays_in_{orient}_direction_{orient_side}_side_feedback",
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"orientation-S{add_level}", f"orientation_of_{orient}_direction_{orient_side}_side_feedback_DMax"
                )
            )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        ray_feedback_excitation_vertical_orientation,
    ]
