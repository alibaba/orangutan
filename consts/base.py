import math

LEN = {
    k: int(math.pow(10, v - 1))
    for k, v in {
        'neuron_no': 3,
        'ind': 5,
        # 'id': 7,
        'col_no': 3
    }.items()
}

# # 脉冲本身产生的兴奋
# NERVE_SPIKE_EXCITE = 10.
# MAX_EXCITE = 2000
MAX_EXCITE = 10000

IMG_PATH = '/Users/laola/CodeProject/Orangutan/vue_server/public'
GRAY_IMG_PATH = f'{IMG_PATH}/orient_spase_coding_gray_imgs'
GRAY_IMG_PATH_D5 = f'{GRAY_IMG_PATH}/d5'
GRAY_IMG_PATH_D7 = f'{GRAY_IMG_PATH}/d7'
GRAY_IMG_PATH_D9 = f'{GRAY_IMG_PATH}/d9'
GRAY_IMG_PATH_D13 = f'{GRAY_IMG_PATH}/d13'