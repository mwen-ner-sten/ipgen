"""
IPGen - A flexible IP address generator supporting multiple input and output formats.
"""

__version__ = "0.1.0"

from .core import IPGenerator
from .parsers import (
    parse_csv,
    parse_excel,
    parse_json,
    parse_yaml,
    parse_cidr,
    parse_range,
    parse_wildcard,
    parse_gateway_subnet
)
from .formatters import (
    to_csv,
    to_excel,
    to_json,
    to_yaml,
    to_list,
    to_dict
)
from .gui import IPGenGUI, main as gui_main

__all__ = [
    'IPGenerator',
    'parse_csv',
    'parse_excel',
    'parse_json',
    'parse_yaml',
    'parse_cidr',
    'parse_range',
    'parse_wildcard',
    'parse_gateway_subnet',
    'to_csv',
    'to_excel',
    'to_json',
    'to_yaml',
    'to_list',
    'to_dict',
    'IPGenGUI',
    'gui_main'
] 