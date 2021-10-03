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