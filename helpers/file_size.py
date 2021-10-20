import logging
from pathlib import Path

from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


# https://stackoverflow.com/a/55659577/10291933
class ByteSize(int):
    _kiB = 1024
    _suffixes = 'B', 'kiB', 'MiB', 'GiB', 'PiB'

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.bytes = self.B = int(self)
        self.kilobytes = self.kiB = self / self._kiB ** 1
        self.megabytes = self.MiB = self / self._kiB ** 2
        self.gigabytes = self.GiB = self / self._kiB ** 3
        self.petabytes = self.PiB = self / self._kiB ** 4
        *suffixes, last = self._suffixes
        suffix = next((
            suffix
            for suffix in suffixes
            if 1 < getattr(self, suffix) < self._kiB
        ), suffixes[0])
        self.readable = suffix, getattr(self, suffix)

        super().__init__()

    def __str__(self):
        return self.__format__('.2f')

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def __format__(self, format_spec):
        suffix, val = self.readable
        return '{val:{fmt}} {suf}'.format(val=val, fmt=format_spec,
                                          suf=suffix)

    def __sub__(self, other):
        return self.__class__(super().__sub__(other))

    def __add__(self, other):
        return self.__class__(super().__add__(other))

    def __mul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rsub__(self, other):
        return self.__class__(super().__sub__(other))

    def __radd__(self, other):
        return self.__class__(super().__add__(other))

    def __rmul__(self, other):
        return self.__class__(super().__rmul__(other))


def get_size(path: Path) -> ByteSize:
    if path.is_file():
        return ByteSize(path.stat().st_size)
    else:
        return ByteSize(sum(file.stat().st_size for file in path.rglob("*")))
