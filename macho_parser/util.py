#!/usr/bin/env python3
import sys
import plistlib
from pathlib import Path

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