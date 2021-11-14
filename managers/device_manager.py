import logging
from shutil import disk_usage, copy2, copytree, rmtree
from pathlib import Path
from string import ascii_uppercase
from typing import Union

from helpers.create_logger import create_logger
from helpers.operating_system import on_windows
from helpers.singleton import Singleton
from managers.bundle_manager import Module
from helpers.file_size import get_size, ByteSize

logger = create_logger(name=__name__, level=logging.DEBUG)


class Drive:
    def __init__(self, path: Path):
        """
        Make an object that represents a drive.

        :param path: A Path to the drive.
        """
        self.path = path
        self.is_circuitpython = False
        self.boot_out_path = None
        self.boot_out_text = None
        self.code_py_path = None
        self.code_py_size = None
        self.boot_py_path = None
        self.boot_py_size = None
        self.lib_path = None
        self.lib_size = None
        self.installed_modules = []
        self.total_size, self.used_size, self.free_size = (0, 0, 0)
        self.recalculate_info()

    def recalculate_info(self):
        """
        (Re)calculate disk space.
        """
        self.total_size, self.used_size, self.free_size = disk_usage(self.path)
        self.total_size = ByteSize(self.total_size)
        self.used_size = ByteSize(self.used_size)
        self.free_size = ByteSize(self.free_size)

    def install_module(self, module: Module):
        """
        Install the module to this device. Will raise NotImplementedError if
        this is not a CircuitPython drive.

        :param module: The module to install.
        """
        raise NotImplementedError

    def uninstall_module(self, module: str):
        """
        Uninstall the module in lib. Will raise NotImplementedError if
        this is not a CircuitPython drive.

        :param module: The module to uninstall.
        """
        raise NotImplementedError


class CircuitPythonDrive(Drive):
    def __init__(self, path: Path):
        """
        Make an object that represents a CircuitPython drive.

        :param path: A Path to the drive.
        """
        super().__init__(path)
        self.is_circuitpython = True

    def recalculate_info(self):
        super().recalculate_info()
        self.boot_out_path = self.path / "boot_out.txt"
        self.boot_out_text = None
        if self.boot_out_path.exists():
            self.boot_out_text = self.boot_out_path.read_text()
        else:
            logger.warning(f"Path {self.boot_out_path} does not exist, yet is "
                           f"initiated as a CircuitPythonDrive!")
        self.code_py_path = None
        self.code_py_size = None
        for name in ("code.txt", "code.py", "main.txt", "main.py"):
            code_py_path = self.path / name
            if code_py_path.exists():
                logger.debug(f"Found code.py path at {code_py_path}")
                self.code_py_path = code_py_path
                self.code_py_size = get_size(self.code_py_path)
                logger.debug(f"Size of code file is {self.code_py_size}")
                break
        else:
            logger.warning("Unable to find code file!")
        self.boot_py_path = None
        self.boot_py_size = None
        for name in ("settings.txt", "settings.py", "boot.txt", "boot.py"):
            boot_py_path = self.path / name
            if boot_py_path.exists():
                logger.debug(f"Found code.py path at {boot_py_path}")
                self.boot_py_path = boot_py_path
                self.boot_py_size = get_size(self.boot_py_path)
                logger.debug(f"Size of code file is {self.boot_py_size}")
                break
        else:
            logger.warning("Unable to find boot file!")
        self.lib_path = None
        self.lib_size = None
        self.installed_modules = []
        lib_path = self.path / "lib"
        if lib_path.exists() and lib_path.is_dir():
            self.lib_path = lib_path
            logger.debug(f"Found /lib folder at {self.lib_path}")
            self.lib_size = get_size(self.lib_path)
            logger.debug(f"Size of /lib folder is {self.lib_size}")
            for path in self.lib_path.glob("*"):
                logger.debug(f"Found installed module: {path.name}")
                self.installed_modules.append(path.name)
        else:
            logger.warning(f"Unable to find {lib_path}!")

    def install_module(self, module: Module):
        """
        Install the module to this device. Will raise NotImplementedError if
        this is not a CircuitPython drive.

        :param module: The module to install.
        """
        logger.debug(f"Installing module {module} ({module.name})")
        if module.path.is_file():
            copy2(module.path, self.lib_path)
        else:
            copytree(module.path, self.lib_path / module.path.name)

    def uninstall_module(self, module: str):
        """
        Uninstall the module in lib. Will raise NotImplementedError if
        this is not a CircuitPython drive.

        :param module: The module to uninstall.
        """
        logger.debug(f"Uninstalling module {module}")
        module_path = self.lib_path / module
        if not module_path.exists():
            raise FileNotFoundError(f"Could not find {module} to uninstall!")
        if module_path.is_file():
            module_path.unlink()
        else:
            rmtree(module_path)


class DeviceManager(metaclass=Singleton):
    def __init__(self, drive_path: Union[Path, None]):
        """
        Make a DeviceManager.

        :param drive_path: The directory where drives will be mounted. Can be
         None if on Windows.
        """
        self.drive_path = drive_path
        self.drives = []
        self.circuitpython_drives = []
        self.index_drives()

    def index_drives(self):
        """
        Index for connected drives.
        """
        logger.debug("Indexing for connected drives")
        self.drives = []
        self.circuitpython_drives = []
        if on_windows():
            logger.debug("On Windows, testing for all drives from A-Z")
            for letter in ascii_uppercase:
                path = Path(f"{letter}:")
                if not path.exists():
                    continue
                try:
                    disk_usage(path)
                except FileNotFoundError:
                    continue
                boot_out_path = path / "boot_out.txt"
                if boot_out_path.exists():
                    self.circuitpython_drives.append(CircuitPythonDrive(path))
                    logger.debug(f"Found CircuitPython drive at {path}")
                else:
                    self.drives.append(Drive(path))
                    logger.debug(f"Found drive at {path}")
        else:
            logger.debug(f"Not on Windows, iterating through "
                         f"{self.drive_path}")
            for path in self.drive_path.glob("*"):
                if not path.is_dir():
                    continue
                try:
                    disk_usage(path)
                except FileNotFoundError:
                    continue
                boot_out_path = path / "boot_out.txt"
                if boot_out_path.exists():
                    self.circuitpython_drives.append(CircuitPythonDrive(path))
                    logger.debug(f"Found CircuitPython drive at {path}")
                else:
                    self.drives.append(Drive(path))
                    logger.debug(f"Found drive at {path}")
