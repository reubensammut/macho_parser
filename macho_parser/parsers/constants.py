intel_subtypes = {
    0x00: "CPU_SUBTYPE_INTEL_MODEL_ALL",
    0x03: "CPU_SUBTYPE_386",
    0x04: "CPU_SUBTYPE_486",
    0x05: "CPU_SUBTYPE_PENT",
    0x08: "CPU_SUBTYPE_PENTIUM_3",
    0x09: "CPU_SUBTYPE_PENTIUM_M",
    0x0a: "CPU_SUBTYPE_PENTIUM_4",
    0x0b: "CPU_SUBTYPE_ITANIUM",
    0x0c: "CPU_SUBTYPE_XEON",
    0x16: "CPU_SUBTYPE_PENTPRO",
    0x18: "CPU_SUBTYPE_PENTIUM_3_M",
    0x1a: "CPU_SUBTYPE_PENTIUM_4_M",
    0x1b: "CPU_SUBTYPE_ITANIUM_2",
    0x1c: "CPU_SUBTYPE_XEON_MP",
    0x28: "CPU_SUBTYPE_PENTIUM_3_XEON",
    0x36: "CPU_SUBTYPE_PENTII_M3",
    0x56: "CPU_SUBTYPE_PENTII_M5",
    0x67: "CPU_SUBTYPE_CELERON",
    0x77: "CPU_SUBTYPE_CELERON_MOBILE",
    0x84: "CPU_SUBTYPE_486SX"
}

powerpc_subtypes = {
    0x00: "CPU_SUBTYPE_POWERPC_ALL",
    0x01: "CPU_SUBTYPE_POWERPC_601",
    0x02: "CPU_SUBTYPE_POWERPC_602",
    0x03: "CPU_SUBTYPE_POWERPC_603",
    0x04: "CPU_SUBTYPE_POWERPC_603e",
    0x05: "CPU_SUBTYPE_POWERPC_603ev",
    0x06: "CPU_SUBTYPE_POWERPC_604",
    0x07: "CPU_SUBTYPE_POWERPC_604e",
    0x08: "CPU_SUBTYPE_POWERPC_620",
    0x09: "CPU_SUBTYPE_POWERPC_750",
    0x0a: "CPU_SUBTYPE_POWERPC_7400",
    0x0b: "CPU_SUBTYPE_POWERPC_7450",
    0x64: "CPU_SUBTYPE_POWERPC_970"
}

arm_subtypes = {
    0x00: "CPU_SUBTYPE_ARM_ALL",
    0x05: "CPU_SUBTYPE_ARM_V4T",
    0x06: "CPU_SUBTYPE_ARM_V6",
    0x07: "CPU_SUBTYPE_ARM_V5",
    0x08: "CPU_SUBTYPE_ARM_XSCALE",
    0x09: "CPU_SUBTYPE_ARM_V7",
    0x0a: "CPU_SUBTYPE_ARM_V7F",
    0x0b: "CPU_SUBTYPE_ARM_V7S",
    0x0c: "CPU_SUBTYPE_ARM_V7K",
    0x0e: "CPU_SUBTYPE_ARM_V6M",
    0x0f: "CPU_SUBTYPE_ARM_V7M",
    0x10: "CPU_SUBTYPE_ARM_V7EM"
}

sparc_subtypes = {
    0x00: "CPU_SUBTYPE_SPARC_ALL"
}

arm64_subtypes = {
    0x00: "CPU_SUBTYPE_ARM64_ALL"
}

generic_subtype = {
    0x00: "CPU_SUBTYPE_UNKNOWN"
}

cpu_types = {
    0x00000006: {
        "name": "CPU_TYPE_MC680X0",
        "subtypes": generic_subtype
    },
    0x00000007: {
        "name": "CPU_TYPE_X86",
        "subtypes": intel_subtypes
    },
    0x00000008: {
        "name": "CPU_TYPE_MIPS",
        "subtypes": generic_subtype
    },
    0x0000000a: {
        "name": "CPU_TYPE_MC98000",
        "subtypes": powerpc_subtypes
    },
    0x0000000b: {
        "name": "CPU_TYPE_HPPA",
        "subtypes": generic_subtype
    },
    0x0000000c: {
        "name": "CPU_TYPE_ARM",
        "subtypes": arm_subtypes
    },
    0x0000000d: {
        "name": "CPU_TYPE_MC88000",
        "subtypes": generic_subtype
    },
    0x0000000e: {
        "name": "CPU_TYPE_SPARC",
        "subtypes": sparc_subtypes
    },
    0x0000000f: {
        "name": "CPU_TYPE_I860",
        "subtypes": intel_subtypes
    },
    0x00000010: {
        "name": "CPU_TYPE_ALPHA",
        "subtypes": generic_subtype
    },
    0x00000012: {
        "name": "CPU_TYPE_POWERPC",
        "subtypes": powerpc_subtypes
    },
    0x01000007: {
        "name": "CPU_TYPE_X86_64",
        "subtypes": intel_subtypes
    },
    0x0100000c: {
        "name": "CPU_TYPE_ARM64",
        "subtypes": arm64_subtypes
    },
    0x01000012: {
        "name": "CPU_TYPE_POWERPC64",
        "subtypes": powerpc_subtypes
    }
}

def get_cpu_type(type):
    return cpu_types.get(type)["name"]

def get_cpu_subtype(type, subtype):
    return cpu_types.get(type)["subtypes"][subtype]


filetypes = {
    0x1:    "MH_OBJECT",
    0x2:    "MH_EXECUTE",
    0x3:    "MH_FVMLIB",
    0x4:    "MH_CORE",
    0x5:    "MH_PRELOAD",
    0x6:    "MH_DYLIB",
    0x7:    "MH_DYLINKER",
    0x8:    "MH_BUNDLE",
    0x9:    "MH_DYLIB_STUB",
    0xa:    "MH_DSYM",
    0xb:    "MH_KEXT_BUNDLE"
}

def get_filetype(type):
    return filetypes.get(type)

flags = {
    0x1:        "MH_NOUNDEFS",
    0x2:        "MH_INCRLINK",
    0x4:        "MH_DYLDLINK",
    0x8:        "MH_BINDATLOAD",
    0x10:       "MH_PREBOUND",
    0x20:       "MH_SPLIT_SEGS",
    0x40:       "MH_LAZY_INIT",
    0x80:       "MH_TWOLEVEL",
    0x100:      "MH_FORCE_FLAT",
    0x200:      "MH_NOMULTIDEFS",
    0x400:      "MH_NOFIXPREBINDING",
    0x800:      "MH_PREBINDABLE",
    0x1000:     "MH_ALLMODSBOUND",
    0x2000:     "MH_SUBSECTIONS_VIA_SYMBOLS",
    0x4000:     "MH_CANONICAL",
    0x8000:     "MH_WEAK_DEFINES",
    0x10000:    "MH_BINDS_TO_WEAK",
    0x20000:    "MH_ALLOW_STACK_EXECUTION",
    0x40000:    "MH_ROOT_SAFE",
    0x80000:    "MH_SETUID_SAFE",
    0x100000:   "MH_NO_REEXPORTED_DYLIBS",
    0x200000:   "MH_PIE",
    0x400000:   "MH_DEAD_STRIPPABLE_DYLIB"
}

def get_flags(flag):
    res = ""
    for k,v in flags.items():
        if flag & k == k: 
            if res != "":
                res = res + " | "
            res = res + v
    return res

command_types = {
    0x00000001: "LC_SEGMENT",
    0x00000002: "LC_SYMTAB",
    0x00000003: "LC_SYMSEG",
    0x00000004: "LC_THREAD",
    0x00000005: "LC_UNIXTHREAD",
    0x00000006: "LC_LOADFVMLIB",
    0x00000007: "LC_IDFVMLIB",
    0x00000008: "LC_IDENT",
    0x00000009: "LC_FVMFILE",
    0x0000000a: "LC_PREPAGE",
    0x0000000b: "LC_DYSYMTAB",
    0x0000000c: "LC_LOAD_DYLIB",
    0x0000000d: "LC_ID_DYLIB",
    0x0000000e: "LC_LOAD_DYLINKER",
    0x0000000f: "LC_ID_DYLINKER",
    0x00000010: "LC_PREBOUND_DYLIB",
    0x00000011: "LC_ROUTINES",
    0x00000012: "LC_SUB_FRAMEWORK",
    0x00000013: "LC_SUB_UMBRELLA",
    0x00000014: "LC_SUB_CLIENT",
    0x00000015: "LC_SUB_LIBRARY",
    0x00000016: "LC_TWOLEVEL_HINTS",
    0x00000017: "LC_PREBIND_CKSUM",
    0x00000019: "LC_SEGMENT_64",
    0x0000001A: "LC_ROUTINES_64",
    0x0000001B: "LC_UUID",
    0x0000001D: "LC_CODE_SIGNATURE",
    0x0000001E: "LC_SEGMENT_SPLIT_INFO",
    0x00000020: "LC_LAZY_LOAD_DYLIB",
    0x00000021: "LC_ENCRYPTION_INFO",
    0x00000022: "LC_DYLD_INFO",
    0x00000024: "LC_VERSION_MIN_MACOSX",
    0x00000025: "LC_VERSION_MIN_IPHONEOS",
    0x00000026: "LC_FUNCTION_STARTS",
    0x00000027: "LC_DYLD_ENVIRONMENT",
    0x00000029: "LC_DATA_IN_CODE",
    0x0000002A: "LC_SOURCE_VERSION",
    0x0000002B: "LC_DYLIB_CODE_SIGN_DRS",
    0x0000002C: "LC_ENCRYPTION_INFO_64",
    0x0000002D: "LC_LINKER_OPTION",
    0x0000002E: "LC_LINKER_OPTIMIZATION_HINT",
    0x0000002F: "LC_VERSION_MIN_TVOS",
    0x00000030: "LC_VERSION_MIN_WATCHOS",
    0x00000032: "LC_BUILD_VERSION",
    0x80000018: "LC_LOAD_WEAK_DYLIB",
    0x8000001C: "LC_RPATH",
    0x8000001F: "LC_REEXPORT_DYLIB",
    0x80000022: "LC_DYLD_INFO_ONLY",
    0x80000023: "LC_LOAD_UPWARD_DYLIB",
    0x80000028: "LC_MAIN"
}

def get_command(cmd):
    return command_types.get(cmd, "** NON STANDARD **")

section_flags_base = {
    0x00:       "S_REGULAR",
    0x01:       "S_ZEROFILL",
    0x02:       "S_CSTRING_LITERALS",
    0x03:       "S_4BYTE_LITERALS",
    0x04:       "S_8BYTE_LITERALS",
    0x05:       "S_LITERAL_POINTERS",
    0x06:       "S_NON_LAZY_SYMBOL_POINTERS",
    0x07:       "S_LAZY_SYMBOL_POINTERS",
    0x08:       "S_SYMBOL_STUBS",
    0x09:       "S_MOD_INIT_FUNC_POINTERS",
    0x0a:       "S_MOD_TERM_FUNC_POINTERS",
    0x0b:       "S_COALESCED",
    0x0c:       "S_GB_ZEROFILL",
    0x0d:       "S_INTERPOSING",
    0x0e:       "S_16BYTE_LITERALS",
    0x0f:       "S_DTRACE_DOF",
    0x10:       "S_LAZY_DYLIB_SYMBOL_POINTERS",
    0x11:       "S_THREAD_LOCAL_REGULAR",
    0x12:       "S_THREAD_LOCAL_ZEROFILL",
    0x13:       "S_THREAD_LOCAL_VARIABLES",
    0x14:       "S_THREAD_LOCAL_VARIABLE_POINTERS",
    0x15:       "S_THREAD_LOCAL_INIT_FUNCTION_POINTERS"
}

section_flags_mask = {
    0x00000100: "S_ATTR_LOC_RELOC",
    0x00000200: "S_ATTR_EXT_RELOC",
    0x00000400: "S_ATTR_SOME_INSTRUCTIONS",
    0x02000000: "S_ATTR_DEBUG",
    0x04000000: "S_ATTR_SELF_MODIFYING_CODE",
    0x08000000: "S_ATTR_LIVE_SUPPORT",
    0x10000000: "S_ATTR_NO_DEAD_STRIP",
    0x20000000: "S_ATTR_STRIP_STATIC_SYMS",
    0x40000000: "S_ATTR_NO_TOC",
    0x80000000: "S_ATTR_PURE_INSTRUCTIONS"
}

def get_sflags(flag):
    res = section_flags_base[flag & 0xf]
    flag = flag & ~0xf
    for k,v in section_flags_mask.items():
        if flag & k == k: 
            if res != "":
                res = res + " | "
            res = res + v
    return res

prots = {
    0x01:   "VM_PROT_READ",
    0x02:   "VM_PROT_WRITE",
    0x04:   "VM_PROT_EXECUTE"
}

def get_prots(prot):
    res = ""
    for k,v in prots.items():
        if prot & k == k: 
            if res != "":
                res = res + " | "
            res = res + v
    if res == "":
        res = "VM_PROT_NONE"
    return res
