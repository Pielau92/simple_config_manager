import os

from example import Configs, Runtime

path_ini = os.path.abspath('assets/configs.ini')
configs = Configs(path_ini)

configs.runtime = Runtime(
    current_time='15:38',
    some_user_entry=42,
    selected_path='C:\\some\\path',
)

pass
