import os
import numpy as np
from consts.experiment import HISTORY_DIR, INPUT_DIR, CORTEX_OPTS


def mock_next_feature():
    global mnist, num_input, feature_name
    global props_disappear_tick_spike_times

    [
        feature_name,
        feature_ind,
        mock_feature_tick_count,
        is_new_feature,
        is_new_mnist,
        is_feature_end,
        is_mnist_end,
        load_error,
    ] = load_next_feature()

    cortex_obj.mock_file_name = feature_name

    # 从第二个特征开始的操作
    if feature_ind > 0:
        before_feature_name = replay_feature_names[feature_ind - 1]

        # mock锚点特征的位置
        if mock_feature_tick_count > 0:
            cortex['excite'][ANCHOR_FEATURE_GRID_INDS] = np.load(
                f'{INPUT_DIR}/{before_feature_name};grid.npy',
                allow_pickle=False)

        # 在mock每个特征前的第一帧的时候，mock上个特征的群体编码消失
        if mock_feature_tick_count == 0:
            mock_props_disappear(before_feature_name)
        else:
            # 树突棘竞争会考虑棘上的excite，为避免stp对的树突棘竞争的影响，需要在每组属性传递兴奋前，消除stp
            cortex_obj.reset_cortex_props_to_initial_state(
                include_props=['STP'])

    # 记录群体编码消失的marker_remain
    if mock_feature_tick_count == 1:
        props_disappear_tick_spike_times = cortex['tick_spike_times'][
            POPU_ABSTRACT_DISAPPEAR_INDS]

    # 从每个特征的第二帧开始，mock这个特征的群体编码出现
    if mock_feature_tick_count >= 1:
        mock_props_appear(feature_name)

    if feature_ind == 0 and mock_feature_tick_count == 0:
        # 第一个特征的第一帧是没内容的，需要重置所有属性值
        clear_before_abstract_inds = [
            *POPU_ABSTRACT_APPEAR_INDS,
            *POPU_ABSTRACT_DISAPPEAR_INDS,
        ]
        cortex['excite'][clear_before_abstract_inds] = cortex['RP'][
            clear_before_abstract_inds]
        cortex_obj.vary_soma_inds.update(clear_before_abstract_inds)

    return [
        feature_ind,
        is_new_feature,
        is_new_mnist,
        is_feature_end,
        is_mnist_end,
    ]


def load_next_feature():
    global mock_mnist_tick_count
    is_new_mnist = False
    load_error = None

    mock_mnist_tick_count += 1

    # tick1: 上个特征消失 tick2-3: 这个特征出现
    # 每个被mock的特征可以持续多少tick
    MOCK_FEATURE_TICK_SUM = 3
    feature_ind = mock_mnist_tick_count // MOCK_FEATURE_TICK_SUM
    mock_feature_tick_count = mock_mnist_tick_count % MOCK_FEATURE_TICK_SUM
    is_new_feature = mock_feature_tick_count == 0
    is_feature_end = mock_feature_tick_count == MOCK_FEATURE_TICK_SUM - 1
    is_mnist_end = is_feature_end and feature_ind == len(
        replay_feature_names) - 1

    no_more_feature = feature_ind > len(replay_feature_names) - 1
    if no_more_feature:
        load_next_mnist_error = load_next_mnist()
        if load_next_mnist_error == 'NO_MORE_MNIST':
            load_error = load_next_mnist_error
        else:
            # 成功加载下一个mnist后，加载新的mnist的第一个特征
            return load_next_feature()
    else:
        feature_name = replay_feature_names[feature_ind]

    return [
        feature_name,
        feature_ind,
        mock_feature_tick_count,
        is_new_feature,
        is_new_mnist,
        is_feature_end,
        is_mnist_end,
        load_error,
    ]


def get_all_mock_abstract_feature_names(mnist_names):
    all_feature_names = list(
        set([
            feature_name.split(';')[0]
            for feature_name in os.listdir(INPUT_DIR)
            if feature_name.count(';excite') == 1 and '_'.join(
                os.path.splitext(feature_name)[0].split(';')[0].split('_')[:2])
            in mnist_names
        ]))
    all_feature_names.sort(
        key=lambda name: int(name.replace('_', '').replace(';', '')))

    return all_feature_names


def get_mock_feature_names_list(mnist_names):
    if not isinstance(mnist_names, list):
        mnist_names = [mnist_names]

    feature_names_list = []

    for mnist_name in mnist_names:
        file_names = [
            file_name for file_name in os.listdir(INPUT_DIR)
            if file_name.startswith(mnist_name)
            and file_name.endswith('excite.npy')
        ]

        feature_sum = max([
            int(file_name.split(';')[0].split('_')[2])
            for file_name in file_names
        ]) + 1
        # feature_sequence_sum = 1  # 取第一个特征序列作为输入
        feature_sequence_sum = max([
            int(file_name.split(';')[0].split('_')[3])
            for file_name in file_names
        ]) + 1
        for feature_sequence_ind in range(feature_sequence_sum):
            feature_names = []
            feature_names_list.append(feature_names)
            for feature_ind in range(feature_sum):
                feature_name = f'{mnist_name}_{feature_ind}_{feature_sequence_ind}'
                feature_names.append(feature_name)

    return feature_names_list
