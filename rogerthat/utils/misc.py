import ctypes
import os
import sys


def set_bash_title(OneStr):
    if os.sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(OneStr)
    elif os.sys.platform == 'darwin' or os.sys.platform.startswith('linux'):
        sys.stdout.write(f"\x1b]2;{OneStr}\x07")
