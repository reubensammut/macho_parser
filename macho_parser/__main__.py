#!/usr/bin/env python3
import sys

from macho_parser.util import resolve_path

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <filename>\n")
        sys.exit(1)

    exe_path = resolve_path(sys.argv[1])
    print(exe_path)

if __name__ == '__main__':
    main()
