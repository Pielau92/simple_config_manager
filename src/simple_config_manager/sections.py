"""Contains a dataclass for each section inside the .ini file. Each dataclass consists of configurations with a
given name and datatype. If the attribute '_section_name' is not set, it will not be loaded from the .ini file and
will have to be filled another way (recommended e.g for runtime configurations). For Example:


@dataclass
class Section1:
    _section_name = 'Section name inside ini file'  # delete line if not to be loaded from ini file
    config1: str        # explanatory comment for config1
    config2: int
    config3: bool
    config4: list[str]
"""

from dataclasses import dataclass


@dataclass
class General:
    _section_name = 'General'
    path_exe: str  # path to TRNSYS executable file
    multiprocessing_max: int  # maximum number of simulations performed simultaneously
    multiprocessing_autodetect: bool  # if true, override multiprocessing_max with number of cpu cores
    eval_save_interval: int  # the evaluation progress is saved after each save interval
    conda_venv_name: str  # name of the conda virtual environment (venv) to be used


@dataclass
class Filenames:
    _section_name = 'Filenames'
    dck_template: str
    logger: str
    trnsys_output: str
    savefile: str
    redundant: list[str]
    templates: list[str]
    templates_assets: list[str]


@dataclass
class SheetNames:
    """Excel sheet names"""

    _section_name = 'Excel sheet names'
    sim_variants: str
    variant_input: str
    calculation: str
    cumulative_input: str
    zone_1_input: str
    zone_3_input: str
    zone_1_with_operating_time: str
    zone_1_without_operating_time: str
    zone_3_with_operating_time: str
    zone_3_without_operating_time: str


@dataclass
class ColumnHeaders:
    _section_name = 'Column headers'
    zone1: list[str]
    zone2: list[str]
    zone3: list[str]
    result_column: list[str]
    trnsys_output: list[str]
    sim_variant: list[str]


@dataclass
class Time:
    _section_name = 'Time'
    timeout_sim: int  # if timeout is reached without starting another simulation, stop whole program [s]
    timeout_open_dck_window: int  # if timeout is reached without opening dck selection window, stop defective simulation [s]
    timeout_open_sim_window: int  # if timeout is reached without opening simulation window, stop defective simulation [s]
    buffer_sim_start: int  # time buffer between two simulations, for increased stability [s]


@dataclass
class Runtime:
    """Contains configurations set at runtime."""
    execution_time: str
    filename_sim_variants_excel: str
    dirname_sim_series: str
