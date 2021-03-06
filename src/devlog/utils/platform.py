import fcntl
import os
import stat
import sys
from contextlib import contextmanager
from typing import Generator


@contextmanager
def single_instance_mutex(
            directory: str, name: str, abort: bool = True
        ) -> Generator[int, None, None]:  # pragma: nocover
    lf = os.path.join(directory, f'{name}.lock')
    lf_fd = os.open(
        lf,
        os.O_WRONLY | os.O_CREAT,
        stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,
    )
    try:
        fcntl.lockf(lf_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        msg = f'Only one instance of {name} can be running'
        if abort:
            sys.exit(msg)
        raise IOError(msg)
    try:
        yield lf_fd
    finally:
        os.close(lf_fd)
        os.remove(lf)
