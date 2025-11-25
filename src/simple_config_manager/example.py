from dataclasses import dataclass

from configs import _Configs

"""CONFIGURATION CLASS EXAMPLE"""


@dataclass
class FirstSection:
    """Explanatory comment about section (optional)"""
    # mandatory field if to be filled with values from .ini file, must match with section name used inside .ini file!
    _section_name = 'First section'

    use: int  # explanatory comment about configuration (optional)
    any: int
    name: int
    you: int
    like: int


@dataclass
class AnotherSection:
    _section_name = 'Another section'

    # those are all available data types, type hint is mandatory!
    some_text: str
    a_number: int
    another_number: float
    some_bool: bool
    some_list: list[str]
    another_list: list[int]
    yet_another_list : list[float]


@dataclass
class Runtime:

    # some configurations are best set during runtime...
    current_time: str
    some_user_entry: int
    selected_path: str


@dataclass(init=False)  # take __init__ method from _Configs class, keeps section fields from being required arguments
class Configs(_Configs):  # inherit from _Configs parent class

    first_section: FirstSection  # link each field to a section via type hint
    another_section: AnotherSection  # define and add as many sections as you like
    runtime: Runtime = None  # use None as default, if configurations should be set during runtime rather than from ini
