from dataclasses import dataclass

from configs import _Configs

"""CONFIGURATION CLASS EXAMPLE"""


@dataclass
class FirstSection:
    """Explanatory comment about section (optional)"""
    _section_name = 'First section' # mandatory field, must correspond with section name used inside .ini file!

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


@dataclass
class Runtime:
    _section_name = 'Runtime'

    # some configurations are best set during runtime...
    current_time: str
    some_user_entry: str
    selected_path: str


@dataclass(init=False)  # take __init__ method from _Configs class, keeps section fields from being required arguments
class Configs(_Configs):  # inherit from _Configs parent class

    first_section: FirstSection  # link each field to a section via type hint
    another_section: AnotherSection  # define and add as many sections as you like
    runtime: Runtime = None  # use None as default, if configurations should be set during runtime rather than from ini
