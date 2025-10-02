import types
from dataclasses import dataclass, fields
from typing import Type, TypeVar, List, Union

import configparser

T = TypeVar("T")  # type placeholder


@dataclass
class _Configs:
    """Parent dataclass for creating user-defined configuration classes through inheritance.

    A configuration class is used to read and store configuration values from an .ini file. See example.py for more
    information on how a configuration class can be defined."""

    def __init__(self, path_ini: str = None):
        """Initialize configuration object by reading configurations from an ini file.

        :param str path_ini: path to configurations .ini file
        """

        for field in fields(self):
            if field.default is not None:  # if default value 'None' was set, do not try to load section from ini file
                setattr(self, field.name, self._get_ini_section(path_ini, field.type))

    @staticmethod
    def _get_ini_section(path: str, cls: Type[T]) -> T:
        """Load configuration section from .ini file and return as dataclass instance.

        For each of field of the passed dataclass, a matching key value pair has to be present inside the specified
        section of the .ini file. The value of each corresponding key value pair is collected and then passed to
        the dataclass constructor, to return an instance of said class.

        :param str path: path to .ini file
        :param Type[T] cls: class (actual class, not an instance of it) whose instance is used to save configurations
        :return: class instance
        """

        # read .ini file
        config = configparser.ConfigParser(
            interpolation=None  # enables the use of % signs inside strings in settings.ini, otherwise error
        )
        config.optionxform = str  # keep capital letters
        with open(path, encoding='utf-8') as file:
            config.read_string(file.read())

        # get section, if it exists
        section = cls._section_name
        if section not in config:
            raise ValueError(f'Section "{section}" not found inside {path}')
        cfg_section = config[section]

        # read values
        kwargs = {}
        for field in fields(cls):
            name = field.name

            if name not in cfg_section:
                raise ValueError(f'Missing field "{name}" in section "{section}"')

            try:
                kwargs[name] = type_conversion(cfg_section[name], field.type)
            except ValueError:
                raise ValueError(f'Field {name} inside {path} has invalid boolean value "{cfg_section[name]}"')
            except TypeError:
                raise TypeError(f'Field "{name}" inside {path} has unsupported field type "{field.type}"')

        return cls(**kwargs)


def type_conversion(raw: str, typ: type | types.GenericAlias) -> Union[str, int, float, bool, list[str]] | None:
    """Convert raw string value into a desired type.

    :param str raw: raw string value
    :param type | types.GenericAlias typ: type
    :return: value with desired type
    """

    if typ == str:  # string
        return raw
    elif typ == int:  # integer
        return int(raw)
    elif typ == float:  # float
        return float(raw)
    elif typ in {List[str], list[str]}:  # list of strings
        return [x.strip() for x in raw.split(',') if x.strip()]
    elif typ == bool:  # boolean
        if raw.lower() in {'true', '1', 'yes', 'on'}:
            return True
        elif raw.lower() in {'false', '0', 'no', 'off'}:
            return False
        else:
            raise ValueError
    else:
        raise TypeError  # if no matching type was found
