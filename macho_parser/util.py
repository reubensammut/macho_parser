#!/usr/bin/env python3
import sys
import plistlib
from pathlib import Path
from contextlib import contextmanager

def resolve_path(name):
    path = Path(name)
    resolved_file = ''
    if not path.exists():
        sys.stderr.write(f"File '{path}' does not exist\n")
        sys.exit(1)
    
    if path.is_dir() and path.suffix != '.app':
        sys.stderr.write(f"'{path}' is not a Mac '.app'\n")
        sys.exit(1)
    elif path.is_dir():
        plist_path = path / "Contents" / "Info.plist"
        if not(plist_path.exists() and plist_path.is_file()):
            sys.stderr.write(f"'{path}' does not have an 'Info.plist'\n")
            sys.exit(1)
        else:
            try:
                with open(plist_path, "rb") as fh:
                    plist = plistlib.load(fh)
                    exe_path_str = plist["CFBundleExecutable"]
                    if exe_path_str.startswith('MacOS/'):
                        exe_path_str = exe_path_str[len('MacOS/'):]
                    exe_path = Path(path / "Contents" / "MacOS" / exe_path_str)
                    if not(exe_path.exists() and exe_path.is_file()):
                        sys.stderr.write(f"CFBundleExecutable '{exe_path_str}' does not exist for '{path}'\n")
                        sys.exit(1)
                    else:
                        resolved_file = exe_path
            except plistlib.InvalidFileException as ife:
                sys.stderr.write(f"'{path}' has an invalid 'Info.plist'\n")
                sys.exit(1)
            except KeyError as ke:
                sys.stderr.write("f'{path}' does not have a CFBundleExecutable\n")
                sys.exit(1)
    else:
        resolved_file = path

    return resolved_file

def parse_32bit_version(version):
    vers = []
    for i in range(3):
        vt = version & 0xff
        vers.insert(0, str(vt))
        version = version >> 8
    return '.'.join(vers)

def parse_64bit_version(version):
    vers = []
    for i in range(5):
        vt = version & 0x3ff
        vers.insert(0, str(vt))
        version = version >> 10
    return '.'.join(vers)
    
class TabbedWriter(object):
    def __init__(self):
        self.tabs = 0
        self.tab = '\t'

    def tprint(self, text):
        print(f"{self.tab * self.tabs}{text}")
    
    @contextmanager
    def next_level(self):
        self.tabs = self.tabs + 1
        yield self
        self.tabs = self.tabs - 1