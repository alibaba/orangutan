from .form_process_index import FORM_PROCESS_INDEX
import itertools

# def form_init_nerve():
#     return list(
#         itertools.chain(
#             *[form_process() for form_process in FORM_PROCESS_INDEX]))

form_init_nerve = list(
    itertools.chain(*[form_process() for form_process in FORM_PROCESS_INDEX]))
