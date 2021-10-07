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
