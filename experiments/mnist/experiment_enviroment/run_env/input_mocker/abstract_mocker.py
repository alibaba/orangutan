from .mock_data_loader import Mock_data_loader
# from typing import List


class Abstract_mocker():

    def __init__(self, cortex_obj, mock_data_list=[]):
        self.cortex_obj = cortex_obj
        self.cortex = self.cortex_obj.cortex
        self.mock_data_loader = Mock_data_loader(
            mock_data_list=mock_data_list, )

    def mock_input(self):
        pass
