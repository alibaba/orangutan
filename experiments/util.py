import numpy as np
import importlib
from consts.experiment import EXPERIMENT_NAME
from PIL import Image
from consts.nerve_props import TYPE
import math
from consts.feature import (
    ORIENTS,
    ORIENT_SUM,
    RECEPTIVE_FIELD_LEVELS,
    COMMON_ABSTRACT_TYPES_MAP,
)

regions = importlib.import_module(f"experiments.{EXPERIMENT_NAME}.regions")
REGION = regions.REGION
SOMA_SLICE_MAP = regions.SOMA_SLICE_MAP


def get_neuron_soma_inds_with_full_shape(region_info, region_soma_slice, neuron_name):
    neuron_soma_slice = region_soma_slice[neuron_name]
    region_height, region_width, mini_col_sum_in_hyper_col = region_info["region_shape"]
    full_soma_inds = region_height * region_width * mini_col_sum_in_hyper_col
    soma_inds = np.zeros(full_soma_inds)
    soma_inds[neuron_soma_slice.get("neuron_in_pic_mask", slice(None))] = np.arange(
        neuron_soma_slice["cortex_slice"].start,
        neuron_soma_slice["cortex_slice"].stop,
    )
    return soma_inds


def get_soma_inds(
    region_name,
    neuron_names,
    hyper_col_inds_in_region="all_hyper_col",
    mini_col_inds_in_hyper_col="all_mini_col",
):
    """
    Get the indices of the soma or other compartments of neurons that meet the specified criteria in bulk (excluding synapses).

    Example:
    Call: get_soma_inds("region_name", "neuron_names")
    Returns: array([2418, 2419, 2420, 2421, 2422, ... 3197, 3198, 3199, 3200, 3201])

    Parameters:
    region_name (str): Name of the brain region
    neuron_names (str): Name of the neuron compartments
    hyper_col_inds_in_region (str|int): Index of the hypercolumn located within the inner of the brain region, default("all_hyper_col")
    mini_col_inds_in_hyper_col (str|int): Index of the minicolumn located within each hypercolumn's inner, default("all_mini_col")

    Returns:
    numpy.array: Indices of all compartments that meet the specified criteria.
    """

    region_soma_slice = SOMA_SLICE_MAP.get(region_name)
    if not region_soma_slice:
        return []

    region_info = REGION[region_name]
    if not (isinstance(neuron_names, list) or (type(neuron_names) is np.ndarray)):
        neuron_names = [neuron_names]
    neuron_names = [
        neuron_name
        for neuron_name in neuron_names
        if region_info["neurons"].get(neuron_name)
    ]
    if not len(neuron_names):
        return np.asarray([])

    assert (
        hyper_col_inds_in_region == "all_hyper_col"
        or mini_col_inds_in_hyper_col == "all_mini_col"
    )

    if hyper_col_inds_in_region == "all_hyper_col":
        pass
    elif type(hyper_col_inds_in_region) is np.ndarray:
        hyper_col_inds_in_region = list(hyper_col_inds_in_region)
    elif not isinstance(hyper_col_inds_in_region, list):
        hyper_col_inds_in_region = [hyper_col_inds_in_region]

    if mini_col_inds_in_hyper_col == "all_mini_col":
        pass
    elif type(mini_col_inds_in_hyper_col) is np.ndarray:
        mini_col_inds_in_hyper_col = list(mini_col_inds_in_hyper_col)
    elif not isinstance(mini_col_inds_in_hyper_col, list):
        mini_col_inds_in_hyper_col = [mini_col_inds_in_hyper_col]

    all_soma_inds = []

    for neuron_name in neuron_names:
        soma_inds = get_neuron_soma_inds_with_full_shape(
            region_info, region_soma_slice, neuron_name
        ).astype(int)
        if hyper_col_inds_in_region != "all_hyper_col":
            region_row_sum, hyper_col_sum_per_row, mini_col_sum_in_hyper_col = (
                region_info["region_shape"]
            )
            soma_inds = soma_inds.reshape(
                (region_row_sum * hyper_col_sum_per_row, mini_col_sum_in_hyper_col)
            )
            soma_inds = np.concatenate(
                tuple(
                    [
                        soma_inds[hyper_col_inds, :]
                        for hyper_col_inds in hyper_col_inds_in_region
                    ]
                )
            )

        if mini_col_inds_in_hyper_col != "all_mini_col":
            region_row_sum, hyper_col_sum_per_row, mini_col_sum_in_hyper_col = (
                region_info["region_shape"]
            )
            soma_inds = soma_inds.reshape(
                (region_row_sum * hyper_col_sum_per_row, mini_col_sum_in_hyper_col)
            )
            soma_inds = np.concatenate(
                tuple(
                    [
                        soma_inds[:, mini_col_inds]
                        for mini_col_inds in mini_col_inds_in_hyper_col
                    ]
                )
            )

        all_soma_inds.extend(soma_inds)

    return np.array(all_soma_inds)
    # all_soma_inds = np.array(all_soma_inds)
    # return all_soma_inds[all_soma_inds != 0]


def get_hyper_col_inds(region_info):
    region_shape = region_info["region_shape"]
    _, _, mini_col_sum_in_hyper_col = region_shape
    hyper_col_inds = np.arange(region_info["hyper_col_sum"]).repeat(
        mini_col_sum_in_hyper_col
    )
    return hyper_col_inds


def get_mini_col_inds(region_info):
    region_shape = region_info["region_shape"]
    region_row_sum, hyper_col_sum_per_row, mini_col_sum_in_hyper_col = region_shape
    hyper_col_sum = hyper_col_sum_per_row * region_row_sum
    mini_col_inds = np.tile(np.arange(mini_col_sum_in_hyper_col), hyper_col_sum) + 1
    return mini_col_inds


def get_gray_matrix_and_mask(path, rotate_time):
    I = Image.open(path)
    L = I.convert("L")  # Convert to grayscale image
    gray_matrix = 255 - np.asarray(L)
    gray_matrix[gray_matrix < 10] = 0
    gray_matrix = np.rot90(gray_matrix, -rotate_time)
    gray_mask = gray_matrix > 0
    return gray_matrix, gray_mask


def get_gray_mesh_grid(gray_mask):
    gray_w, gray_h = gray_mask.shape
    gray_mesh_grid = np.array(
        np.meshgrid(
            np.arange(-gray_w // 2 + 1, gray_w // 2 + 1),
            np.arange(-gray_h // 2 + 1, gray_h // 2 + 1),
        )
    )
    return gray_mesh_grid


def get_around_and_center_hyper_col_inds_with_around_mask(
    around_region_name, center_region_name, around_mask, indicate_a_center_pos=None
):
    """Based on a mask of the peripheral receptive field, batch retrieval of the indices of cortical hypercolumns that can establish synapses in two brain areas is performed.

    Parameters:
        around_region_name (str): Name of the brain area where the cortical hypercolumns located in the peripheral receptive field are located
        center_region_name (str): Name of the brain area where the cortical hypercolumns located in the central receptive field are located
        around_mask (numpy.array): Mask of the receptive field

    Returns:
        around_pos_inds (numpy.array): Indices of the cortical hypercolumns located in the peripheral receptive field in the brain area "inner"
        center_pos_inds (numpy.array): Indices of the cortical hypercolumns located in the central receptive field in the brain area "inner"
        inrange_around_pos_mask (numpy.array): Indices of the cortical hypercolumns in the peripheral receptive field are within the brain region range ([0, total number of cortical hypercolumns in that brain region]) "inner", which can then be used to establish synapse masks with the cortical hypercolumns in the central receptive field.
    """

    around_mask = around_mask.astype(bool)
    gray_mesh_grid = get_gray_mesh_grid(around_mask)
    around_region = REGION[around_region_name]
    center_region = REGION[center_region_name]
    around_region_h, around_region_w, _ = around_region["region_shape"]
    center_region_h, center_region_w, _ = center_region["region_shape"]
    center_pos_mesh_grid = np.array(
        np.meshgrid(
            np.arange(center_region_w),
            np.arange(center_region_h),
        )
    )
    around_pos_grid = (
        center_pos_mesh_grid.reshape((2, -1))[:, :, np.newaxis]
        + gray_mesh_grid.reshape((2, -1))[:, np.newaxis, :]
    ).reshape(
        (
            2,
            center_pos_mesh_grid.shape[1] * center_pos_mesh_grid.shape[2],
            gray_mesh_grid.shape[1],
            gray_mesh_grid.shape[2],
        )
    )
    inrange_around_pos_mask = around_pos_grid[0, :] > -1
    inrange_around_pos_mask *= around_pos_grid[0, :] < center_region_w
    inrange_around_pos_mask *= around_pos_grid[1, :] > -1
    inrange_around_pos_mask *= around_pos_grid[1, :] < center_region_h
    inrange_around_pos_mask *= around_mask
    inrange_around_pos_mask_shape = inrange_around_pos_mask.shape
    # # The central point cannot be connected.
    # inrange_around_pos_mask[:, inrange_around_pos_mask_shape[1] // 2 + 1 -
    #                         1, inrange_around_pos_mask_shape[2] // 2 + 1 -
    #                         1] = False
    if indicate_a_center_pos != None:
        indicate_center_pos_ind = np.arange(inrange_around_pos_mask.shape[0]).reshape(
            around_region_h, around_region_w
        )[indicate_a_center_pos[0], indicate_a_center_pos[1]]
        inrange_around_pos_mask = inrange_around_pos_mask[
            indicate_center_pos_ind : indicate_center_pos_ind + 1, :, :
        ]
        #
        around_pos_grid = around_pos_grid[
            :, indicate_center_pos_ind : indicate_center_pos_ind + 1, :, :
        ]
        # center_pos_inds = center_pos_inds[indicate_center_pos_ind:
        #                                   indicate_center_pos_ind + 1, :, :]
    around_pos_matrix = around_pos_grid[:, inrange_around_pos_mask]
    center_pos_inds_matrix = (
        np.arange(around_region_h * around_region_w)[:, np.newaxis, np.newaxis]
        + np.zeros(inrange_around_pos_mask.shape[1:], int)[np.newaxis, :, :]
    )
    if indicate_a_center_pos != None:
        center_pos_inds_matrix = center_pos_inds_matrix[
            indicate_center_pos_ind : indicate_center_pos_ind + 1, :, :
        ]
    center_pos_inds = center_pos_inds_matrix[inrange_around_pos_mask]
    around_pos_inds_matrix = np.arange(around_region_h * around_region_w).reshape(
        (around_region_h, around_region_w)
    )
    around_pos_inds = around_pos_inds_matrix[around_pos_matrix[1], around_pos_matrix[0]]
    return around_pos_inds, center_pos_inds, inrange_around_pos_mask


def get_around_and_center_pos_inds_with_gray_img(
    around_region_name,
    center_region_name,
    gray_img_path,
    gray_img_rotate_time=0,
    indicate_a_center_pos=None,
):
    gray_matrix, gray_mask = get_gray_matrix_and_mask(
        gray_img_path, gray_img_rotate_time
    )
    return [
        *get_around_and_center_hyper_col_inds_with_around_mask(
            around_region_name, center_region_name, gray_mask, indicate_a_center_pos
        ),
        gray_matrix,
    ]


def get_neuron2_inds_with_neuron1_inds(
    neuron1_inds, region_name, neuron_name1, neuron_name2
):
    neurons = REGION[region_name]["neurons"]
    neuron_ind_delta = (
        neurons[neuron_name2]["neuron_no"] - neurons[neuron_name1]["neuron_no"]
    )
    return neuron1_inds + neuron_ind_delta


def save_new_axon_inds_to(axon_inds, save_to_targ_name):

    def do_save_to(new_axon_inds):
        axon_inds[save_to_targ_name] = new_axon_inds

    return do_save_to


def save_axon_end_inds_with_new_nerves(axon_end_inds_map, axon_end_name):
    """ Translate: Save the index value of the new synaptic bouton
    Parameters:
        axon_end_inds_map (dict): dictionary for saving the synaptic index
        axon_end_name (str): key name for saving the synaptic index
    """

    def do_save(new_nerve_slice, cortex_obj):
        cortex = cortex_obj.cortex
        axon_end_inds_map[axon_end_name] = cortex["ind"][new_nerve_slice][
            cortex["type"][new_nerve_slice] == TYPE["axon_end"]
        ]

    return do_save


def save_new_marker_2_map(new_marker_map, new_marker_name):

    def do_save(nerve_slice_or_inds, cortex_obj):
        if isinstance(nerve_slice_or_inds, slice):
            nerve_inds = cortex_obj.cortex["ind"][nerve_slice_or_inds]
        else:
            nerve_inds = nerve_slice_or_inds
        new_marker = np.unique(cortex_obj.cortex["marker"][nerve_inds])
        if len(new_marker) > 0:
            if new_marker_map.get(new_marker_name):
                new_marker_map[new_marker_name] = list(
                    set(
                        [
                            *new_marker_map[new_marker_name],
                            *new_marker,
                        ]
                    )
                )
            else:
                new_marker_map[new_marker_name] = list(new_marker)

    return do_save


def cal_closest_orient(y_delta, x_delta, no_orient_value=-1):
    if y_delta == 0 and x_delta == 0:
        return no_orient_value
    if y_delta == 0 and x_delta > 0:
        degree = 90.0
    elif y_delta == 0 and x_delta < 0:
        degree = 270.0
    elif y_delta > 0 and x_delta == 0:
        degree = 180.0
    elif y_delta < 0 and x_delta == 0:
        degree = 360.0
    else:
        z_delta = math.sqrt(math.pow(y_delta, 2) + math.pow(x_delta, 2))
        degree = math.degrees(
            math.acos(
                (math.pow(y_delta, 2) - math.pow(x_delta, 2) - math.pow(z_delta, 2))
                / (-2 * abs(x_delta) * z_delta)
            )
        )
        if x_delta > 0 and y_delta > 0:
            degree = 90 + degree
        elif x_delta > 0 and y_delta < 0:
            degree = 90 - degree
        elif x_delta < 0 and y_delta > 0:
            degree = 90 - degree + 180
        elif x_delta < 0 and y_delta < 0:
            degree = 90 + degree + 180
    closest_orient = ORIENTS[np.argmin(abs(ORIENTS - degree))]
    return closest_orient


def get_popu_orients(orient, popu_range=4):
    if orient == "none":
        popu_orients = [(-1, "none", 1)]
    else:
        orient_ind = np.argmin(abs(orient - ORIENTS))
        popu_orients = [
            (
                # offset_orient_ind
                (orient_ind + orient_ind_offset) % ORIENT_SUM,
                # offset_orient
                ORIENTS[(orient_ind + orient_ind_offset) % ORIENT_SUM],
                # offset_orient_ratio
                ((popu_range - abs(orient_ind_offset)) / popu_range),
            )
            for orient_ind_offset in range(-popu_range + 1, popu_range)
        ]
    return popu_orients


def get_popu_receptive_field_levels(receptive_field_level_ind, group_range=4):
    popu_receptive_field_levels = [
        (
            # offset_receptive_field_level_ind
            receptive_field_level_ind + receptive_field_level_ind_offset,
            # offset_receptive_field_level
            RECEPTIVE_FIELD_LEVELS[
                receptive_field_level_ind + receptive_field_level_ind_offset
            ],
            # offset_receptive_field_level_ratio
            ((group_range - abs(receptive_field_level_ind_offset)) / group_range),
        )
        for receptive_field_level_ind_offset in range(-group_range + 1, group_range)
        if -1
        < (receptive_field_level_ind + receptive_field_level_ind_offset)
        < len(RECEPTIVE_FIELD_LEVELS)
    ]

    return popu_receptive_field_levels


def get_popu_props(prop_type, prop_value, popu_range=4):
    prop_info = COMMON_ABSTRACT_TYPES_MAP[prop_type]
    is_can_popu = prop_info.get("is_can_popu", True)
    is_value_recyclable = prop_info["value_recyclable"] != False
    if not is_can_popu or prop_value == "none":
        popu_values = [(-1, prop_value, 1)]
    else:
        prop_number_values = np.asarray(
            [
                prop_value
                for prop_value in prop_info["values"]
                if not isinstance(prop_value, str)
            ]
        )
        value_sum = len(prop_number_values)
        value_ind = np.argmin(abs(prop_value - prop_number_values))
        popu_values = [
            (
                # offset_prop_ind
                (value_ind + value_ind_offset) % value_sum,
                # offset_prop
                prop_number_values[(value_ind + value_ind_offset) % value_sum],
                # offset_prop_ratio
                ((popu_range - abs(value_ind_offset)) / popu_range),
            )
            for value_ind_offset in range(-popu_range + 1, popu_range)
            if is_value_recyclable
            or (
                (value_ind + value_ind_offset) > -1
                and (value_ind + value_ind_offset) < value_sum
            )
        ]
    return popu_values


def cal_deg(xy, xy1):

    a = np.array(xy)
    b = np.array(xy1)

    # Calculate the norm (length) of a
    a_norm = np.linalg.norm(a)
    # Calculate the norm (length) of b
    b_norm = np.linalg.norm(b)
    # Calculate the dot product of a and b (multiply corresponding positions and then add the results).
    a_dot_b = a.dot(b)
    # Calculate the radian value of cos_there using the cosine theorem.
    cos_theta = np.arccos(a_dot_b / (a_norm * b_norm))
    # To convert radians to degrees
    angle = np.rad2deg(cos_theta)
    if np.isnan(angle):
        if (a == 0).all() or (b == 0).all():
            return np.inf
        elif ((a * b) > 0).all():
            return 0
        elif ((a * b) < 0).all():
            return 180.0
    return angle


def get_vector_x_and_y(length, angle):
    # Convert angle to radians.
    angle_rad = math.radians(angle)
    # Calculate the adjacent side and the opposite side.
    x = length * math.sin(angle_rad)
    y = length * math.cos(angle_rad)
    return x, y


def get_orient_distance_matrix(orient, matrix_wh, orient_range):
    """
    Get a relative orientation of a neuron with each neighboring neuron and an approximate ratio of a specific orientation.

    Pseudocode:
    1. Create a matrix with equal width and height, and both odd.
    2. Establish a Y-axis down, X-axis to the right angle coordinate system with the center of the matrix as the origin point, and map it to an orientation angle system (the vector (x=0, y=-1) corresponds to an orientation angle of 360 degrees or 0 degrees).
    3. Calculate the absolute value of the offset of each vector (x, y) from the orientation angle given.
    4. Calculate the offset ratio relative to the specific offset range.
    5. Return the approximate ratio matrix = 1 - offset ratio matrix.

    Example:
    Call: get_orient_distance_matrix(45.0, 3, 90.0)
    Returns: array([[0.        , 0.5       , 1         ],
                    [0.        , 0.        , 0.5       ],
                    [0.        , 0.        , 0.        ]])

    Parameters:
    orient (float): face
    matrix_wh (int): width and height of the matrix, odd
    orient_range (float): the offset range for calculating the offset ratio, offset ratio = offset value/offset range

    Returns:
    numpy.array: The approximate ratio matrix calculated from step 5.
    """

    base_axis = np.arange(-(matrix_wh // 2), matrix_wh // 2 + 1)

    orient_distance_matrix = np.array(
        [
            cal_deg((x, y), get_vector_x_and_y(1, orient))
            for y in base_axis[::-1]
            for x in base_axis
        ]
    ).reshape((matrix_wh, matrix_wh))

    orient_distance_ratio_matrix = (
        np.maximum(0, orient_range - orient_distance_matrix) / orient_range
    )

    return orient_distance_ratio_matrix
    # return orient_distance_matrix, orient_distance_ratio_matrix
