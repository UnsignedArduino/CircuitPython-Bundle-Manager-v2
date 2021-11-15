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

import tkinter as tk
from typing import Union, Callable

from TkZero.Label import Label
from TkZero.Style import define_style, WidgetStyleRoots

configured_styles = False


class ClickableLabel(Label):
    def __init__(self, parent: Union[tk.Widget, Union[tk.Tk, tk.Toplevel]],
                 command: Callable):
        """
        Make a ClickableLabel.

        :param parent: The parent of the label.
        :param command: The command to run when clicked.
        """
        super().__init__(parent)
        self.command = command
        self.bind("<Button-1>", self.click)
        global configured_styles
        if not configured_styles:
            configured_styles = True
            define_style(WidgetStyleRoots.Label, "clickable",
                         foreground="#6495ED")
            define_style(WidgetStyleRoots.Label, "clickable_hover",
                         foreground="#0000FF")
            define_style(WidgetStyleRoots.Label, "clickable_click",
                         foreground="#00008B")
        self.apply_style("clickable")
        self.bind("<Enter>", lambda _: self.apply_style("clickable_hover"))
        self.bind("<Leave>", lambda _: self.apply_style("clickable"))

    def click(self, _):
        """
        Click.
        """
        self.apply_style("clickable_click")
        self.after(100, lambda: self.apply_style("clickable"))
        self.command()
