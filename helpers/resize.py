"""
CircuitPython Bundle Manager v2 - a Python program to easily manage
modules on a CircuitPython device!

Copyright (C) 2021 UnsignedArduino

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from typing import Iterable, Union

from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def make_resizable(parent, rows: Union[Union[Iterable, int], None] = None,
                   cols: Union[Union[Iterable, int], None] = None,
                   weight: int = 1):
    """
    Configure the rows and columns to have a weight of 1.

    :param parent: A Tkinter widget to use.
    :param rows: An Iterable or an int, specifying which row(s) to
     configure.
    :param cols: An Iterable or an int, specifying which column(s) to
     configure.
    :param weight: The weight to set. Defaults to 1.
    """
    if rows is None:
        pass
    elif isinstance(rows, int):
        parent.rowconfigure(rows, weight=weight)
    else:
        for row in rows:
            parent.rowconfigure(row, weight=weight)
    if cols is None:
        pass
    elif isinstance(cols, int):
        parent.columnconfigure(cols, weight=weight)
    else:
        for col in cols:
            parent.columnconfigure(col, weight=weight)
