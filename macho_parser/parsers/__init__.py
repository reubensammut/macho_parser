#!/usr/bin/env python3
from struct import unpack
import struct
import sys

from macho_parser.util import TabbedWriter
from macho_parser.parsers.constants import get_cpu_type, get_cpu_subtype

class Parser():
    def __init__(self, path):
        self.path = path
        self.w = TabbedWriter()

        self.parsers = {
            0xCAFEBABE: (self.parse_fatbin, ">"),   # Big-Endian Fat Binary
            0xBEBAFECA: (self.parse_fatbin, "<"),   # Little-Endian Fat Binary
            0xFEEDFACE: (self.parse_32bit,  ">"),   # Big-Endian 32-bit binary
            0xCEFAEDFE: (self.parse_32bit,  "<"),   # Little-Endian 32-bit binary
            0xFEEDFACF: (self.parse_64bit,  ">"),   # Big-Endian 64-bit binary
            0xCFFAEDFE: (self.parse_64bit,  "<")    # Little-Endian 64-bit binary
        }

    def parse_32bit(self, endian, fh):
        self.w.tprint("32-bit Mach-O")

    def parse_64bit(self, endian, fh):
        self.w.tprint("64-bit Mach-O")

    def parse_fatbin(self, endian, fh):
        self.w.tprint("FAT BINARY HEADER")
        count = unpack(f"{endian}I", fh.read(4))[0]
        self.w.tprint(f"Count: {count}")

        offsets = []

        for i in range(count):
            cpu_type, cpu_subtype, file_offset, size, align = unpack(f"{endian}IIIII", fh.read(4*5))
            offsets.append(file_offset)
            self.w.tprint(f"Arch[{i}]")
            with self.w.next_level() as w1:
                w1.tprint(f"CPU Type:       {get_cpu_type(cpu_type)} ({hex(cpu_type)})")
                w1.tprint(f"CPU SubType:    {get_cpu_subtype(cpu_type, cpu_subtype)} ({hex(cpu_subtype)})")
                w1.tprint(f"File Offset:    {hex(file_offset)}")
                w1.tprint(f"Size:           {hex(size)}")
                w1.tprint(f"Align:          {2**align} (2^{align})")

        for i in range(len(offsets)):
            self.w.tprint(f"Mach-O[{i}]")
            offset = offsets[i]
            fh.seek(offset)
            magic = unpack(f"{endian}I", fh.read(4))[0]
            (parser,endiansub) = self.parsers[magic]
            with self.w.next_level() as x:
                parser(endiansub, fh)

        
    def parse(self):
        with open(self.path, 'rb') as fh:
            try:
                magic = unpack(">I", fh.read(4))[0]
                (parser,endian) = self.parsers[magic]
                parser(endian, fh)
            except struct.error as se:
                sys.stderr.write(f"Incorrect file format\n")
                sys.exit(1)
            except KeyError as ke:
                sys.stderr.write(f"Incorrect magic bytes\n")
                sys.exit(1)
        