#!/usr/bin/env python3
from struct import unpack
import struct
import sys
from time import ctime
from uuid import UUID

from macho_parser.util import TabbedWriter, parse_32bit_version, parse_64bit_version
from macho_parser.parsers.constants import get_cpu_type, get_cpu_subtype, get_filetype, get_flags, get_command, get_sflags, get_prots

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

        self.cmd_parsers = {
            0x2:        self.parse_lc_symtab,
            0xb:        self.parse_lc_dsymtab,
            0xc:        self.parse_lc_load_dylib,
            0xd:        self.parse_lc_load_dylib,
            0xe:        self.parse_lc_load_dylinker,
            0xf:        self.parse_lc_load_dylinker,
            0x19:       self.parse_lc_segment_64,
            0x1b:       self.parse_lc_uuid,
            0x1d:       self.parse_lc_code_signature,
            0x1e:       self.parse_lc_code_signature,
            0x22:       self.parse_lc_dyld_info,
            0x24:       self.parse_lc_version_min_macosx,
            0x25:       self.parse_lc_version_min_macosx,
            0x26:       self.parse_lc_code_signature,
            0x27:       self.parse_lc_load_dylinker,
            0x29:       self.parse_lc_code_signature,
            0x2a:       self.parse_lc_source_version,
            0x2b:       self.parse_lc_code_signature,
            0x80000018: self.parse_lc_load_dylib,
            0x8000001C: self.parse_lc_rpath,
            0x8000001F: self.parse_lc_load_dylib,
            0x80000022: self.parse_lc_dyld_info,
            0x80000028: self.parse_lc_main
        }

    def parse_lc_symtab(self, endian, fh, _maxsize):
        symoff, nsyms, stroff, strsize = unpack(f"{endian}IIII", fh.read(4*4))
        
        with self.w.next_level() as w1:
            w1.tprint(f"Symbol table offset:    {hex(symoff)}")
            w1.tprint(f"Number of symbols:      {nsyms}")
            w1.tprint(f"String table offset:    {hex(stroff)}")
            w1.tprint(f"String table size:      {hex(strsize)}")

    def parse_lc_dsymtab(self, endian, fh, _maxsize):
        ilocalsym, nlocalsym, iextdefsym, nextdefsym, iundefsym, nundefsym = unpack(f"{endian}IIIIII", fh.read(4*6))
        tocoff, ntoc, modtaboff, nmodtab, extrefsymoff, nextrefsyms = unpack(f"{endian}IIIIII", fh.read(4*6))
        indirectsymoff, nindirectsyms, extreloff, nextrel, locreloff, nlocrel = unpack(f"{endian}IIIIII", fh.read(4*6))

        with self.w.next_level() as w1:
            w1.tprint(f"Index local symbols:        {hex(ilocalsym)}")
            w1.tprint(f"Number local symbols:       {nlocalsym}")
            w1.tprint(f"Index extern symbols:       {hex(iextdefsym)}")
            w1.tprint(f"Number extern symbols:      {nextdefsym}")
            w1.tprint(f"Index undef symbols:        {hex(iundefsym)}")
            w1.tprint(f"Number undef symbols:       {nundefsym}")
            w1.tprint(f"TOC offset:                 {hex(tocoff)}")
            w1.tprint(f"TOC entries:                {ntoc}")
            w1.tprint(f"Module table offset:        {hex(modtaboff)}")
            w1.tprint(f"Module table entries:       {nmodtab}")
            w1.tprint(f"Ref sym table offset:       {hex(extrefsymoff)}")
            w1.tprint(f"Ref sym table entries:      {nextrefsyms}")
            w1.tprint(f"Indirect sym table offset:  {hex(indirectsymoff)}")
            w1.tprint(f"Indirect sym table entries: {nindirectsyms}")
            w1.tprint(f"Ext rel entries offset:     {hex(extreloff)}")
            w1.tprint(f"Ext rel entries:            {nextrel}")
            w1.tprint(f"Local rel entries offset:   {hex(locreloff)}")
            w1.tprint(f"Local rel entries:          {nlocrel}")
    
    def parse_lc_load_dylib(self, endian, fh, maxsize):
        offset, timestamp, curver, compatver,data = unpack(f"{endian}IIII{maxsize - (4*4)}s", fh.read(maxsize))
        with self.w.next_level() as w1:
            w1.tprint(f"Name offset in LC:  {hex(offset)}")
            w1.tprint(f"Timestamp:          {ctime(timestamp)}")
            w1.tprint(f"Current version:    {parse_32bit_version(curver)}")
            w1.tprint(f"Compat version:     {parse_32bit_version(compatver)}")
            offset = offset - 8  # ignore cmd and cmd size 
            offset = offset - 16 # offset from start of data
            str_data = data[offset:]
            str_data = str_data[:str_data.find(b"\x00")]
            w1.tprint(f"Name:               {str_data.decode()}") 

    def parse_lc_load_dylinker(self, endian, fh, maxsize):
        offset, data = unpack(f"{endian}I{maxsize - 4}s", fh.read(maxsize))
        with self.w.next_level() as w1:
            w1.tprint(f"Name offset in LC:  {hex(offset)}")
            offset = offset - 8 # ignore cmd and cmd size
            offset = offset - 4 # length of offset 
            str_data = data[offset:]
            str_data = str_data[:str_data.find(b"\x00")]
            w1.tprint(f"Name:               {str_data.decode()}")

    def parse_lc_segment_64(self, endian, fh, _maxsize):
        segname, vmaddr, vmsize, fileoff, filesize, maxprot, initprot, nsects, flags = unpack(f"{endian}16sQQQQIIII", fh.read(4*4 + 16 + 8*4))
        segname = segname.rstrip(b"\x00").decode()
        
        with self.w.next_level() as w1:
            w1.tprint(f"Segment name:       {segname}")
            w1.tprint(f"VM Address:         {hex(vmaddr)}")
            w1.tprint(f"VM Size:            {hex(vmsize)}")
            w1.tprint(f"File Offset:        {hex(fileoff)}")
            w1.tprint(f"File Size:          {hex(filesize)}")
            w1.tprint(f"Maximum Prot:       {get_prots(maxprot)} ({hex(maxprot)})")
            w1.tprint(f"Initial Prot:       {get_prots(initprot)} ({hex(initprot)})")
            w1.tprint(f"Number of sects:    {nsects}")
            w1.tprint(f"Flags:              {hex(flags)}")
            for j in range(nsects):
                sectname, ssegname, saddr, ssize, soffset, salign, sreloff, snreloc, sflags, sres1, sres2, sres3 = unpack(f"{endian}16s16sQQIIIIIIII", fh.read(16*2 + 8*2 + 4*8))
                sectname = sectname.rstrip(b"\x00").decode()
                ssegname = ssegname.rstrip(b"\x00").decode()
                w1.tprint(f"SECT[{j}]")
                with w1.next_level() as w2:
                    w2.tprint(f"Section name:       {sectname}")
                    w2.tprint(f"Segment address:    {hex(saddr)}")
                    w2.tprint(f"Size:               {hex(ssize)}")
                    w2.tprint(f"Offset:             {hex(soffset)}")
                    w2.tprint(f"Align:              {hex(salign)}")
                    w2.tprint(f"Relocations offset: {hex(sreloff)}")
                    w2.tprint(f"Number relocations: {hex(snreloc)}")
                    w2.tprint(f"Segment flags:      {get_sflags(sflags)} ({hex(sflags)})")
                    w2.tprint(f"Reserved1:          {hex(sres1)}")
                    w2.tprint(f"Reserved2:          {hex(sres2)}")
                    w2.tprint(f"Reserved3:          {hex(sres3)}")

    def parse_lc_uuid(self, endian, fh, _maxsize):
        uuid_str = unpack(f"{endian}16s", fh.read(16))[0]
        u = UUID(bytes=uuid_str)
        with self.w.next_level() as w1:
            w1.tprint(f"UUID:       {{{u}}}")

    def parse_lc_code_signature(self, endian, fh, _maxsize):
        dataoff, datasize = unpack(f"{endian}II", fh.read(4*2))
        with self.w.next_level() as w1:
            w1.tprint(f"Offset of data in __LINKEDIT:   {hex(dataoff)}")
            w1.tprint(f"Size of data in __LINKEDIT:     {hex(datasize)}")

    def parse_lc_version_min_macosx(self, endian, fh, _maxsize):
        version, sdk = unpack(f"{endian}II", fh.read(4*2))
        with self.w.next_level() as w1:
            w1.tprint(f"Version:    {parse_32bit_version(version)}")
            w1.tprint(f"SDK:        {parse_32bit_version(sdk)}")

    def parse_lc_source_version(self, endian, fh, _maxsize):
        version = unpack(f"{endian}Q", fh.read(8))[0]
        with self.w.next_level() as w1:
            w1.tprint(f"Version:    {parse_64bit_version(version)}")

    def parse_lc_dyld_info(self, endian, fh, _maxsize):
        reboff, rebsize, bindoff, bindsize, wkbindoff, wkbindsize, lzbindoff, lzbindsize, expoff, expsize = unpack(f"{endian}IIIIIIIIII", fh.read(4*10))
        with self.w.next_level() as w1:
            w1.tprint(f"Rebase offset:      {hex(reboff)}")
            w1.tprint(f"Rebase size:        {hex(rebsize)}")
            w1.tprint(f"Bind offset:        {hex(bindoff)}")
            w1.tprint(f"Bind size:          {hex(bindsize)}")
            w1.tprint(f"Weak bind offset:   {hex(wkbindoff)}")
            w1.tprint(f"Weak bind size:     {hex(wkbindsize)}")
            w1.tprint(f"Lazy bind offset:   {hex(lzbindoff)}")
            w1.tprint(f"Lazy bind size:     {hex(lzbindsize)}")
            w1.tprint(f"Export offset:      {hex(expoff)}")
            w1.tprint(f"Export size:        {hex(expsize)}")

    def parse_lc_rpath(self, endian, fh, maxsize):
        offset, data = unpack(f"{endian}I{maxsize - 4}s", fh.read(maxsize))
        with self.w.next_level() as w1:
            w1.tprint(f"Path offset in LC:  {hex(offset)}")
            offset = offset - 8 # ignore cmd and cmd size
            offset = offset - 4 # length of offset 
            str_data = data[offset:]
            str_data = str_data[:str_data.find(b"\x00")]
            w1.tprint(f"Path:               {str_data.decode()}")

    def parse_lc_main(self, endian, fh, _maxsize):
        entryoff, stacksize = unpack(f"{endian}QQ", fh.read(8*2))
        with self.w.next_level() as w1:
            w1.tprint(f"Offset of main:     {hex(entryoff)}")
            w1.tprint(f"Init stack size:    {hex(stacksize)}")

    def parse_lc_generic(self, endian, fh, _maxsize):
        pass 

    def parse_32bit(self, endian, fh):
        self.w.tprint("32-bit Mach-O")
        cpu_type, cpu_subtype, filetype, ncmds, sizeofcmds, flags = unpack(f"{endian}IIIIIII", fh.read(4*6))
        self.w.tprint(f"CPU Type:       {get_cpu_type(cpu_type)} ({hex(cpu_type)})")
        self.w.tprint(f"CPU SubType:    {get_cpu_subtype(cpu_type, cpu_subtype)} ({hex(cpu_subtype)})")
        self.w.tprint(f"File Type:      {get_filetype(filetype)} ({hex(filetype)})")
        self.w.tprint(f"Number cmds:    {ncmds}")
        self.w.tprint(f"Size of cmds:   {sizeofcmds}")
        self.w.tprint(f"Flags:          {get_flags(flags)} ({hex(flags)})")

    def parse_64bit(self, endian, fh):
        self.w.tprint("64-bit Mach-O")
        cpu_type, cpu_subtype, filetype, ncmds, sizeofcmds, flags, reserved = unpack(f"{endian}IIIIIII", fh.read(4*7))
        self.w.tprint(f"CPU Type:       {get_cpu_type(cpu_type)} ({hex(cpu_type)})")
        self.w.tprint(f"CPU SubType:    {get_cpu_subtype(cpu_type, cpu_subtype)} ({hex(cpu_subtype)})")
        self.w.tprint(f"File Type:      {get_filetype(filetype)} ({hex(filetype)})")
        self.w.tprint(f"Number cmds:    {ncmds}")
        self.w.tprint(f"Size of cmds:   {sizeofcmds}")
        self.w.tprint(f"Flags:          {get_flags(flags)} ({hex(flags)})")
        self.w.tprint(f"Reserved:       {hex(reserved)}")

        for i in range(ncmds):
            cmd, cmdsize = unpack(f"{endian}II", fh.read(4*2))
            self.w.tprint(f"LOAD COMMAND[{i}] - {get_command(cmd)} ({hex(cmd)}) [{hex(cmdsize)}]")

            new_parser = self.cmd_parsers.get(cmd)

            if new_parser is None:
                cmdsize = cmdsize - 8
                fh.seek(cmdsize, 1)
            else:
                new_parser(endian, fh, cmdsize - 8)
            


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
            #except struct.error as se:
            #    sys.stderr.write(f"Incorrect file format\n")
            #    sys.exit(1)
            except KeyError as ke:
                sys.stderr.write(f"Incorrect magic bytes\n")
                sys.exit(1)
        