# Based on the given mock data list, load the mock data in order.
class Mock_data_loader():

    def __init__(self, mock_data_list=[]):
        self.mock_data_list = mock_data_list
        self.current_data_ind = -1
        self.is_current_data_new_feature = False
        self.is_next_data_new_feature = True
        self.is_current_data_new_mnist = False
        self.is_next_data_new_mnist = True
        self.current_data = {}
        self.current_data_run_tick = 0
        self.prev_data = self.current_data
        self.force_load_next_mock_data = False

    def load_next_mock_data(self, force_load_next_mock_data=False):
        self.force_load_next_mock_data = force_load_next_mock_data

        self.update_mock_data_ind()

        self.prev_data = self.current_data
        self.current_data = self.get_mock_data()

        self.update_mock_data_info()

    def update_mock_data_ind(self):

        if self.is_can_load_next_mock_data():
            self.current_data_ind += 1
            self.current_data_run_tick = 0

        self.current_data_run_tick += 1

        assert self.current_data_ind < len(
            self.mock_data_list), 'mock_data_reach_end'

    def update_mock_data_info(self):
        self.is_current_data_new_feature = self.is_next_data_new_feature
        self.is_next_data_new_feature = self.is_can_load_next_mock_data()

        self.is_current_data_new_mnist = self.is_next_data_new_mnist
        self.is_next_data_new_mnist = self.current_data.get(
            'is_last_feature', True)

    def is_can_load_next_mock_data(self):
        return self.force_load_next_mock_data or (self.current_data_run_tick >=
                                                  self.current_data.get(
                                                      'run_tick_sum', -1))

    def get_mock_data(self, mock_data_ind=None):
        mock_data_ind = mock_data_ind or self.current_data_ind
        return self.mock_data_list[mock_data_ind] if mock_data_ind < len(
            self.mock_data_list) else {}

    def get_current_feature_name(self):
        return self.current_data['feature_name']

    def insert_mock_data(self, mock_data_list):
        self.mock_data_list = [
            *self.mock_data_list[:self.current_data_ind + 1],
            *mock_data_list,
            *self.mock_data_list[self.current_data_ind + 1:],
        ]
