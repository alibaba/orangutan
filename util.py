# coding:utf-8
import numpy as np
import math
import time
from functools import reduce, wraps
from consts.feature import (
    VISUAL_FIELD_WH,
    ORIENTS,
    RECEPTIVE_FIELD_LEVELS,
    ORIENT_SIDES,
    ORIENT_CONTOUR_SIDES,
)


class print_exe_timecost(object):

    def __init__(self, desc=None):
        self.desc = desc

    def __call__(self, func):

        @wraps(func)
        def decorated_func(*args, **kwargs):
            start_time = time.time()
            func_res = func(*args, **kwargs)
            end_time = time.time()
            print(
                f"[timecost][{self.desc or func.__name__}]",
                (end_time - start_time) * 1000,
            )
            return func_res

        return decorated_func


before_time = 0.0


def print_time_delta(desc=None):
    global before_time
    nowa_time = time.time()
    if desc:
        print(desc, (nowa_time - before_time) * 1000)  # ms
    before_time = nowa_time


def exchange_orient_and_distance_to_y_and_x_offset(orient, distance):
    """
    Translate: Convert the given vector direction and distance into y and x offsets.
    :param orient: direction of the vector (in degrees, with 0 degrees facing upwards and clockwise as the positive direction)
    :param distance: distance of the vector
    :return: tuple of y and x offsets
    """
    # Translate: Convert angles to radians and convert directions to a system where the direction facing right is 0 degrees, and clockwise is the positive direction.
    radian = math.radians((orient - 90) % 360)
    # Calculate the offset between y and x.
    y_offset = math.sin(radian) * distance
    x_offset = math.cos(radian) * distance
    # Return offset tuple
    return y_offset, x_offset


def get_is_orient_endpoint_in_visual_field(y, x, orient, receptive_field_level):
    y_offset, x_offset = exchange_orient_and_distance_to_y_and_x_offset(
        orient, receptive_field_level / 2
    )
    return (0 < y + y_offset < VISUAL_FIELD_WH[0]) and (
        0 < x + x_offset < VISUAL_FIELD_WH[1]
    )


is_can_init_orient_mask_map = {
    (orient, receptive_field_level): np.array(
        [
            get_is_orient_endpoint_in_visual_field(y, x, orient, receptive_field_level)
            for y in range(VISUAL_FIELD_WH[0])
            for x in range(VISUAL_FIELD_WH[1])
        ]
    )
    for receptive_field_level in RECEPTIVE_FIELD_LEVELS
    for orient in ORIENTS
}


def exchange_slice_to_inds(_slice):
    return np.arange(_slice.start, _slice.stop)


def try_exchange_str_to_num(value):
    if value.isdigit():
        return int(value)

    try:
        return float(value)
    except ValueError:
        return value


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def cal_deg_with_opposite_and_adjacent(O, A):
    return math.degrees(math.atan2(O, A))
