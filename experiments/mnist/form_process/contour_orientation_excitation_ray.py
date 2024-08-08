from consts.feature import (
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    LINE_RECEPTIVE_FIELD_LEVELS,
    ORIENT_SIDES,
)
from ...util import REGION, get_soma_inds, save_axon_end_inds_with_new_nerves
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


def excite_rays_at_various_orientations_and_scales(cortex_obj):
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
                    f"orientation-S{add_level}", f"orientation_of_{orient}_direction_{orient_side}_side"
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"ray-S{receptive_field_level}",
                    f"rays_in_{orient}_direction_{orient_side}_side",
                )
            )
            axon_end_release_sums.extend(
                [65 / len(add_levels) * (0.5 + 0.1 * (receptive_field_level // 2))]
                * REGION[f"orientation-S{add_level}"]["hyper_col_sum"]
            )
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def antagonistic_inhibition_of_rays_across_orientations_and_scales(cortex_obj):
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
                np.tile(
                    get_soma_inds(
                        f"global_control", f"apply_antagonistic_inhibition_to_orientation_excitation_rays_A_inhibit"
                    ),
                    REGION[f"ray-S{receptive_field_level}"]["hyper_col_sum"],
                )
            )
            father_inds.extend(
                get_soma_inds(
                    f"ray-S{receptive_field_level}",
                    f"rays_in_{orient}_direction_{orient_side}_side",
                )
            )
    return make_new_nerve_packs(
        mother_inds,
        father_inds,
        cortex_obj,
        new_nerve_callback=save_axon_end_inds_with_new_nerves(
            axon_end_inds, "antagonistic_inhibition_of_rays_across_orientations_and_scales"
        ),
        reset_nerve_props_matrix=np.array(
            axon_end_release_sums, dtype=[("transmitter_release_sum", "float")]
        ),
    )


def eliminate_antagonistic_inhibition_of_rays_across_orientations_and_scales(cortex_obj):
    mother_inds, father_inds = [], []
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
                    f"orientation-S{add_level}", f"orientation_of_{orient}_direction_{orient_side}_side_A_inhibit"
                )
            )
    father_inds = axon_end_inds["antagonistic_inhibition_of_rays_across_orientations_and_scales"]
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inhibit_rays_across_scales_and_orientations_by_inner_orientation_at_smaller_scale(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for orient in ORIENTS:
            inhibit_orient = orient
            for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
                higher_receptive_field_level = receptive_field_level + 2
                inhibit_level = [
                    level
                    for level in RECEPTIVE_FIELD_LEVELS
                    if level <= higher_receptive_field_level
                ][-1]
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{inhibit_level}",
                        f"summary_of_{inhibit_orient}_direction_inner_scale_inner_contour_orientation_sum_value_A_inhibit",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side",
                    )
                )
                axon_end_release_sums.extend(
                    np.tile(
                        [65 * (receptive_field_level // 2 + 1)],
                        REGION[f"orientation-S{1}"]["hyper_col_sum"],
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


def inhibit_rays_across_scales_and_orientations_by_inner_orientation_at_larger_scale(cortex_obj):
    mother_inds, father_inds = [], []
    for orient_side in ORIENT_SIDES:
        for orient in ORIENTS:
            for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
                if receptive_field_level < 3 or receptive_field_level == 21:
                    continue
                inhibit_level = receptive_field_level + 2
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{inhibit_level}",
                        f"orientation_of_{orient}_direction_inner_contour_sum_value_A_inhibit",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side",
                    )
                )
    return form_nerve.make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def inhibit_rays_across_scales_and_orientations_at_ends(cortex_obj):
    mother_inds, father_inds, axon_end_release_sums = [], [], []
    for orient_side in ORIENT_SIDES:
        for orient in ORIENTS:
            for receptive_field_level in LINE_RECEPTIVE_FIELD_LEVELS:
                if receptive_field_level == LINE_RECEPTIVE_FIELD_LEVELS[-1]:
                    continue
                higher_receptive_field_level = receptive_field_level + 2
                mother_inds.extend(
                    get_soma_inds(
                        f"orientation-S{higher_receptive_field_level}",
                        f"orientation_of_{orient}_direction_{orient_side}_side_A_inhibit",
                    )
                )
                father_inds.extend(
                    get_soma_inds(
                        f"ray-S{receptive_field_level}",
                        f"rays_in_{orient}_direction_{orient_side}_side",
                    )
                )
                axon_end_release_sums.extend(
                    np.tile(
                        [65 * (receptive_field_level // 2 + 1)],
                        REGION[f"orientation-S{higher_receptive_field_level}"][
                            "hyper_col_sum"
                        ],
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
        excite_rays_at_various_orientations_and_scales,
        antagonistic_inhibition_of_rays_across_orientations_and_scales,
        eliminate_antagonistic_inhibition_of_rays_across_orientations_and_scales,
        inhibit_rays_across_scales_and_orientations_by_inner_orientation_at_smaller_scale,
        inhibit_rays_across_scales_and_orientations_by_inner_orientation_at_larger_scale,
        inhibit_rays_across_scales_and_orientations_at_ends,
    ]
