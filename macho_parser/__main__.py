#!/usr/bin/env python3
import sys

from macho_parser.util import resolve_path
from macho_parser.parsers import Parser

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <filename>\n")
        sys.exit(1)

    exe_path = resolve_path(sys.argv[1])
    p = Parser(exe_path)
    p.parse()

if __name__ == '__main__':
    main()
