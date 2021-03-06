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
import tkinter as tk
from typing import Callable
import webbrowser

from TkZero.Button import Button
from TkZero.Combobox import Combobox
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Labelframe import Labelframe
from TkZero.Dialog import show_error
from TkZero.Notebook import Tab, Notebook
from TkZero.Progressbar import Progressbar
from TkZero.Scrollbar import Scrollbar, OrientModes
from TkZero.Text import Text, TextWrap

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable

logger = create_logger(name=__name__, level=logging.DEBUG)


class DriveTab(Tab):
    """
    The DriveTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager):
        """
        Make a DriveTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent, "Drive")
        self.cpybm = cpybm
        logger.debug("Making drive tab")
        self.make_gui()

    def make_gui(self):
        """
        Make the GUI for the drive tab.
        """
        logger.debug("Making GUI for drive tab")
        self.make_select_frame()
        make_resizable(self, cols=0, rows=1)
        self.make_info_frame()
        self.update_drives()
        self.select_box.read_only = False
        if self.cpybm.data_manager.has_key("last_selected_drive"):
            selected = self.cpybm.data_manager.get_key("last_selected_drive")
            if selected in self.select_box.values:
                self.select_box.value = selected
                return
            selected += " (CircuitPython drive)"
            if selected in self.select_box.values:
                self.select_box.value = selected
                return
        self.select_box.read_only = True
        self.update_selected()

    def open_selected_drive(self):
        """
        Open the selected drive in explorer.
        """
        path = self.cpybm.selected_drive.path
        logger.debug(f"Opening {path} in default file manager!")
        if path.exists():
            webbrowser.open(str(path))
        else:
            show_error(self, title="CircuitPython Bundle Manager: Error!",
                       message=f"Drive {path} has been disconnected!",
                       detail="Refreshing available drives.")
            self.update_drives()

    def make_select_frame(self):
        """
        Make the selected device frame.
        """
        self.select_frame = Frame(self)
        self.select_frame.grid(row=0, column=0, sticky=tk.NW + tk.E)
        make_resizable(self.select_frame, 0, 1)
        self.select_label = Label(self.select_frame, text="Selected device: ")
        self.select_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.select_box = Combobox(self.select_frame, width=20,
                                   command=self.update_selected)
        self.select_box.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.select_refresh = Button(self.select_frame, text="Refresh",
                                     command=self.update_drives)
        self.select_refresh.grid(row=0, column=2, padx=1, pady=0, sticky=tk.NE)
        self.select_open = Button(self.select_frame, text="Open in default file manager",
                                  command=self.open_selected_drive)
        self.select_open.grid(row=0, column=3, padx=1, pady=0, sticky=tk.NE)
        self.select_open.enabled = False
        self.update_drives()

    def update_drives(self, on_finish: Callable = lambda: None):
        """
        Update all connected drives.

        :param on_finish: The function to run when this finishes.
        """
        logger.debug("Updating connected drives")
        self.select_frame.enabled = False
        self.update()
        self.select_box.read_only = False
        self.drive_dict = {"None": None}
        try:
            self.cpybm.device_manager.index_drives()
            for drive in self.cpybm.device_manager.circuitpython_drives:
                self.drive_dict[str(drive.path) + " (CircuitPython drive)"] = drive
            for drive in self.cpybm.device_manager.drives:
                self.drive_dict[str(drive.path)] = drive
            self.select_box.values = self.drive_dict.keys()
            self.select_box.value = self.select_box.values[0]
        except Exception as e:
            show_error(self, title="CircuitPython Bundle Manager: Error!",
                       message=f"There was an error refreshing the list of available drives!",
                       detail=str(e))
        finally:
            self.select_box.read_only = True
            self.select_frame.enabled = True
            self.select_open.enabled = False
            on_finish()

    def update_selected(self):
        """
        Update the selected device for the info frame.
        """
        logger.debug(f"Updating selected drive")
        self.select_open.enabled = False
        if self.select_box.value not in self.drive_dict:
            return
        selected_drive = self.drive_dict[self.select_box.value]
        if not hasattr(self, "info_frame"):
            logger.debug("Cannot show selected device info since widgets don't exist yet!")
            return
        if selected_drive is None:
            logger.debug("Selected drive is None")
            self.cpybm.selected_drive = None
            self.info_frame.grid_remove()
        else:
            logger.debug(f"Selected drive is {selected_drive} ({selected_drive.path})")
            self.cpybm.selected_drive = selected_drive
            self.cpybm.data_manager.set_key("last_selected_drive", str(selected_drive.path))
            self.info_frame.grid()
            self.info_frame.text = f"Info about {selected_drive.path}"
            self.total_storage_label.text = f"Total storage space: " \
                                            f"({str(selected_drive.used_size)}" \
                                            f" / {str(selected_drive.total_size)})"
            self.total_storage_pbar.value = selected_drive.used_size
            self.total_storage_pbar.maximum = selected_drive.total_size
            self.select_open.enabled = True
            if selected_drive.is_circuitpython:
                self.boot_out_frame.enabled = True
                self.boot_out_text.read_only = False
                self.boot_out_text.text = selected_drive.boot_out_text
                self.boot_out_text.read_only = True
                if selected_drive.code_py_path is not None and selected_drive.code_py_path.exists():
                    self.code_storage_label.grid()
                    self.code_storage_label.text = f"{selected_drive.code_py_path.name}: (" \
                                                   f"{str(selected_drive.code_py_size)})"
                    self.code_storage_pbar.grid()
                    self.code_storage_pbar.value = selected_drive.code_py_size
                    self.code_storage_pbar.maximum = selected_drive.total_size
                else:
                    self.code_storage_label.grid_remove()
                    self.code_storage_pbar.grid_remove()
                if selected_drive.boot_py_path is not None and selected_drive.boot_py_path.exists():
                    self.boot_storage_label.grid()
                    self.boot_storage_label.text = f"{selected_drive.boot_py_path.name}: (" \
                                                   f"{str(selected_drive.boot_py_size)})"
                    self.boot_storage_pbar.grid()
                    self.boot_storage_pbar.value = selected_drive.boot_py_size
                    self.boot_storage_pbar.maximum = selected_drive.total_size
                else:
                    self.boot_storage_label.grid_remove()
                    self.boot_storage_pbar.grid_remove()
                if selected_drive.lib_path is not None and selected_drive.lib_path.exists():
                    self.lib_storage_label.grid()
                    self.lib_storage_label.text = f"{selected_drive.lib_path.name}: (" \
                                                  f"{str(selected_drive.lib_size)})"
                    self.lib_storage_pbar.grid()
                    self.lib_storage_pbar.value = selected_drive.lib_size
                    self.lib_storage_pbar.maximum = selected_drive.total_size
                else:
                    self.lib_storage_label.grid_remove()
                    self.lib_storage_pbar.grid_remove()
            else:
                self.boot_out_text.text = ""
                self.boot_out_frame.enabled = False
                self.code_storage_label.grid_remove()
                self.code_storage_pbar.grid_remove()
                self.boot_storage_label.grid_remove()
                self.boot_storage_pbar.grid_remove()
                self.lib_storage_label.grid_remove()
                self.lib_storage_pbar.grid_remove()

    def make_info_frame(self):
        """
        Make the info about drive frame.
        """
        self.info_frame = Labelframe(self)
        self.info_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.info_frame.grid_remove()
        make_resizable(self.info_frame, cols=range(0, 2), rows=0)
        self.make_boot_out_frame()
        self.make_storage_specs_frame()

    def make_boot_out_frame(self):
        """
        Make the boot_out.txt frame.
        """
        self.boot_out_frame = Frame(self.info_frame)
        self.boot_out_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(self.boot_out_frame, rows=1, cols=0)
        self.boot_out_label = Label(self.boot_out_frame, text="boot_out.txt:")
        self.boot_out_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.boot_out_text = Text(self.boot_out_frame, width=25, height=8,
                                  wrapping=TextWrap.NoWrapping)
        self.boot_out_text.read_only = True
        self.boot_out_text.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.boot_out_text_h = Scrollbar(self.boot_out_frame, widget=self.boot_out_text)
        self.boot_out_text_h.grid(row=1, column=1, padx=1, pady=1)
        self.boot_out_text_w = Scrollbar(self.boot_out_frame, orientation=OrientModes.Horizontal,
                                         widget=self.boot_out_text)
        self.boot_out_text_w.grid(row=2, column=0, padx=1, pady=1)

    def make_storage_specs_frame(self):
        """
        Make the storage specs frame.
        """
        self.storage_frame = Frame(self.info_frame)
        self.storage_frame.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(self.storage_frame, rows=(1, 3, 5, 7), cols=0)
        self.total_storage_label = Label(self.storage_frame)
        self.total_storage_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.total_storage_pbar = Progressbar(self.storage_frame, length=300, allow_text=False)
        self.total_storage_pbar.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.code_storage_label = Label(self.storage_frame)
        self.code_storage_label.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW)
        self.code_storage_pbar = Progressbar(self.storage_frame, length=300, allow_text=False)
        self.code_storage_pbar.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.boot_storage_label = Label(self.storage_frame)
        self.boot_storage_label.grid(row=4, column=0, padx=1, pady=1, sticky=tk.NW)
        self.boot_storage_pbar = Progressbar(self.storage_frame, length=300, allow_text=False)
        self.boot_storage_pbar.grid(row=5, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.lib_storage_label = Label(self.storage_frame)
        self.lib_storage_label.grid(row=6, column=0, padx=1, pady=1, sticky=tk.NW)
        self.lib_storage_pbar = Progressbar(self.storage_frame, length=300, allow_text=False)
        self.lib_storage_pbar.grid(row=7, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.code_storage_label.grid_remove()
        self.code_storage_pbar.grid_remove()
        self.boot_storage_label.grid_remove()
        self.boot_storage_pbar.grid_remove()
        self.lib_storage_label.grid_remove()
        self.lib_storage_pbar.grid_remove()
