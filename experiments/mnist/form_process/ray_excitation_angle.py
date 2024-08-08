from consts.feature import (
    ORIENTS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ANGLES,
    ORIENT_SIDES,
    MIN_ANGLE,
)
from ...util import REGION, get_soma_inds
import numpy as np
from ...form_nerve.form_nerve import form_nerve

axon_end_inds = {}


def summarize_ray_max_values_axon_end_release_sums(receptive_field_level):
    return 65 * (0.85 + receptive_field_level / 60)


def summarize_max_rays_in_different_directions(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
            for orient_side in ORIENT_SIDES:
                mother_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray",
                        f"summarize_max_values_of_rays_in_{orient}_direction_{orient_side}_side_DMax",
                    )
                )
                axon_end_release_sums.extend(
                    np.tile(
                        [
                            summarize_ray_max_values_axon_end_release_sums(
                                receptive_field_level
                            )
                        ],
                        REGION[f"ray-S{receptive_field_level}"]["hyper_col_sum"],
                    )
                )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def stimulus_various_angles(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient in ORIENTS:
        for angle in ANGLES:
            mother_inds.extend(
                get_soma_inds(
                    f"ray",
                    [
                        f"summarize_max_values_of_rays_in_{orient}_direction_right_side",
                        f"summarize_max_values_of_rays_in_{(orient+angle)%360 or 360.0}_direction_left_side",
                    ],
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"angle",
                    [
                        f"angle_of_orientation{orient}_and_{(orient+angle)%360 or 360.0}_DMin",
                        f"angle_of_orientation{orient}_and_{(orient+angle)%360 or 360.0}_DMin",
                    ],
                )
            )
            axon_end_release_sums.extend(
                np.tile(
                    [65 * (1 - angle / MIN_ANGLE / 2 * 0.16)],
                    2 * REGION["ray"]["hyper_col_sum"],
                )
            )
    return form_nerve.make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def form_init_nerve():
    return [
        summarize_max_rays_in_different_directions,
        stimulus_various_angles,
    ]
