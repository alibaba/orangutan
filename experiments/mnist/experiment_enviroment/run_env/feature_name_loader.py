class Feature_name_loader():

    def __init__(self, cortex_obj, feature_list):
        self.mock_feature_tick = 0
        self.feature_list = feature_list
        self.cortex_obj = cortex_obj

    def load_next_feature(self):
        self.mock_feature_tick += 1
        self.nowa_feature_name, self.nowa_feature_exinfo = self.feature_list[
            self.mock_feature_tick]
        self.nowa_mnist_name = '_'.join(self.nowa_feature_name.split('_')[:2])
        self.nowa_num = int(self.nowa_feature_name.split('_')[0])
        self.nowa_feature_ind = int(self.nowa_feature_name.split('_')[-1])
        self.cortex_obj.mock_file_name = self.nowa_feature_exinfo.get(
            'mock_file_name', self.nowa_feature_name)
