from dataclasses import dataclass, fields
from typing import Type, TypeVar, List

import configparser

T = TypeVar("T")  # type placeholder


@dataclass
class _Configs:
    """Parent dataclass for creating user-defined configuration classes through inheritance.

    A configuration class is used to read and store configuration values from an .ini file. See example.py for more
    information on how a configuration class can be defined."""

    def __init__(self, path_ini: str = None):
        """Initialize configuration object by loading configurations from an ini file.

        :param str path_ini: path to configurations .ini file
        """

        for field in fields(self):
            if field.default is not None:  # if default value 'None' was set, do not try to load section from ini file
                setattr(self, field.name, self._get_ini_section(path_ini, field.type))

    @staticmethod
    def _get_ini_section(path: str, cls: Type[T]) -> T:
        """Load configuration section from ini file and return as dataclass instance.

        For each attribute defined in the passed dataclass, a corresponding key value pair has to be present inside the
        specified section of the ini file. The value of each corresponding key value pair is collected and then passed to
        the dataclass constructor, to return an instance of said class.

        :param str path: path to ini file
        :param Type[T] cls: class (actual class, not an instance of it) whose instance is used to save configurations
        :return: class instance
        """

        # read ini file
        config = configparser.ConfigParser()
        config.optionxform = str  # keep capital letters
        config.read(path)

        # get section, if it exists
        section = cls._section_name
        if section not in config:
            raise ValueError(f'Section "{section}" not found in {path}')
        cfg_section = config[section]

        kwargs = {}
        for field in fields(cls):
            name = field.name
            typ = field.type

            if field.name not in cfg_section:
                raise ValueError(f'Missing key "{field.name}" in [{section}]')

            raw = cfg_section[name]

            # type conversion
            if typ == int:
                value = int(raw)
            elif typ == float:
                value = float(raw)
            elif typ == str:
                value = raw
            elif typ in {List[str], list[str]}:
                value = [x.strip() for x in raw.split(',') if x.strip()]
            elif typ == bool:
                if raw.lower() in {'true', '1', 'yes', 'on'}:
                    value = True
                elif raw.lower() in {'false', '0', 'no', 'off'}:
                    value = False
                else:
                    raise ValueError(f"Invalid boolean value: {raw}")
            else:
                raise TypeError(
                    f'Unsupported field type {typ} with value "{raw}" in section "{section}" inside {path}.')

            kwargs[name] = value

        return cls(**kwargs)
