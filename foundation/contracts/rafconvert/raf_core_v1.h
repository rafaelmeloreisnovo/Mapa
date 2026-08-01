#ifndef RAFAELIA_RAF_CORE_V1_H
#define RAFAELIA_RAF_CORE_V1_H

/*
 * RAFAELIA RafConvert/RafDisk core contract V1
 * State: DESIGN_CONTRACT_IMPLEMENTATION_PENDING
 * Freestanding: no libc, malloc, shell, network, or OS ABI required.
 * This header defines types, flags, bounded cursors, and checked arithmetic.
 */

#if defined(__cplusplus)
extern "C" {
#endif

typedef unsigned char      raf_u8;
typedef unsigned short     raf_u16;
typedef unsigned int       raf_u32;
typedef unsigned long long raf_u64;
typedef signed int         raf_i32;

#if defined(__UINTPTR_TYPE__)
typedef __UINTPTR_TYPE__ raf_uptr;
#else
typedef unsigned long raf_uptr;
#endif

typedef char raf_assert_u8_is_1[(sizeof(raf_u8) == 1u) ? 1 : -1];
typedef char raf_assert_u16_is_2[(sizeof(raf_u16) == 2u) ? 1 : -1];
typedef char raf_assert_u32_is_4[(sizeof(raf_u32) == 4u) ? 1 : -1];
typedef char raf_assert_u64_is_8[(sizeof(raf_u64) == 8u) ? 1 : -1];
typedef char raf_assert_uptr_matches_pointer[
    (sizeof(raf_uptr) == sizeof(void *)) ? 1 : -1];

#define RAF_ABI_VERSION_V1          0x00010000u
#define RAF_FLAG_SCHEMA_VERSION_V1  0x00010000u
#define RAF_U64_MAX_VALUE           (~(raf_u64)0u)
#define RAF_UPTR_MAX_VALUE          (~(raf_uptr)0u)
#define RAF_BIT64(n)                ((raf_u64)1u << (n))

/* Errors are causal status values, never combinable capability flags. */
typedef enum raf_status_v1 {
    RAF_OK = 0,
    RAF_E_ARGUMENT = 1,
    RAF_E_BOUNDS = 2,
    RAF_E_OVERFLOW = 3,
    RAF_E_LIMIT = 4,
    RAF_E_SIGNATURE = 5,
    RAF_E_FORMAT = 6,
    RAF_E_UNSUPPORTED = 7,
    RAF_E_INVARIANT = 8,
    RAF_E_ALIGNMENT = 9,
    RAF_E_OVERLAP = 10,
    RAF_E_CODEC = 11,
    RAF_E_INTEGRITY = 12,
    RAF_E_SIGNATURE_STALE = 13,
    RAF_E_TOKEN_VAZIO = 14,
    RAF_E_PROHIBITED = 15,
    RAF_E_VERIFY = 16
} raf_status_v1;

/* bits 0..7: format traits */
#define RAF_F_COMPRESSED       RAF_BIT64(0)
#define RAF_F_ARCHIVE          RAF_BIT64(1)
#define RAF_F_DISK_IMAGE       RAF_BIT64(2)
#define RAF_F_FILESYSTEM       RAF_BIT64(3)
#define RAF_F_STREAMABLE       RAF_BIT64(4)
#define RAF_F_RANDOM_ACCESS    RAF_BIT64(5)
#define RAF_F_SIGNED           RAF_BIT64(6)
#define RAF_F_ENCRYPTED        RAF_BIT64(7)

/* bits 8..15: I/O traits */
#define RAF_IO_READ_ONLY       RAF_BIT64(8)
#define RAF_IO_SEEKABLE        RAF_BIT64(9)
#define RAF_IO_SPARSE          RAF_BIT64(10)
#define RAF_IO_IN_PLACE        RAF_BIT64(11)
#define RAF_IO_STAGED          RAF_BIT64(12)
#define RAF_IO_MEMORY_MAP      RAF_BIT64(13)
#define RAF_IO_CHUNKED         RAF_BIT64(14)
#define RAF_IO_EXTERNAL_CODEC  RAF_BIT64(15)

/* bits 16..23: alignment classes */
#define RAF_A_2                RAF_BIT64(16)
#define RAF_A_4                RAF_BIT64(17)
#define RAF_A_512              RAF_BIT64(18)
#define RAF_A_2048             RAF_BIT64(19)
#define RAF_A_4096             RAF_BIT64(20)
#define RAF_A_16384            RAF_BIT64(21)
#define RAF_A_65536            RAF_BIT64(22)
#define RAF_A_CUSTOM           RAF_BIT64(23)

/* bits 24..31: transforms */
#define RAF_T_COPY             RAF_BIT64(24)
#define RAF_T_NORMALIZE        RAF_BIT64(25)
#define RAF_T_EXTRACT          RAF_BIT64(26)
#define RAF_T_REPACK           RAF_BIT64(27)
#define RAF_T_RECOMPRESS       RAF_BIT64(28)
#define RAF_T_CANONICALIZE     RAF_BIT64(29)
#define RAF_T_ZERO_FILL        RAF_BIT64(30)
#define RAF_T_DEDUPLICATE      RAF_BIT64(31)

/* bits 32..39: integrity */
#define RAF_I_CRC32            RAF_BIT64(32)
#define RAF_I_CRC32C           RAF_BIT64(33)
#define RAF_I_SHA256           RAF_BIT64(34)
#define RAF_I_SHA3             RAF_BIT64(35)
#define RAF_I_BLAKE3           RAF_BIT64(36)
#define RAF_I_MERKLE           RAF_BIT64(37)
#define RAF_I_SIGNATURE        RAF_BIT64(38)
#define RAF_I_ROUNDTRIP        RAF_BIT64(39)

/* bits 40..47: backend/ISA */
#define RAF_ISA_PORTABLE_C     RAF_BIT64(40)
#define RAF_ISA_ARMV7          RAF_BIT64(41)
#define RAF_ISA_AARCH64        RAF_BIT64(42)
#define RAF_ISA_NEON           RAF_BIT64(43)
#define RAF_ISA_X86_64         RAF_BIT64(44)
#define RAF_ISA_SSE42          RAF_BIT64(45)
#define RAF_ISA_AVX2           RAF_BIT64(46)
#define RAF_ISA_CRC_EXT        RAF_BIT64(47)

/* bits 48..55: safety/policy */
#define RAF_P_BOUNDED          RAF_BIT64(48)
#define RAF_P_NO_MALLOC        RAF_BIT64(49)
#define RAF_P_DETERMINISTIC    RAF_BIT64(50)
#define RAF_P_NO_SHELL         RAF_BIT64(51)
#define RAF_P_NO_NETWORK       RAF_BIT64(52)
#define RAF_P_DRY_RUN          RAF_BIT64(53)
#define RAF_P_ATOMIC_COMMIT    RAF_BIT64(54)
#define RAF_P_CLAIM_FALSE      RAF_BIT64(55)

#define RAF_FLAGS_EXPERIMENTAL_MASK ((raf_u64)0xFFu << 56)

typedef enum raf_format_id_v1 {
    RAF_FMT_UNKNOWN = 0,
    RAF_FMT_ZIP = 1,
    RAF_FMT_APK = 2,
    RAF_FMT_ISO9660 = 3,
    RAF_FMT_TAR = 4,
    RAF_FMT_PAX = 5,
    RAF_FMT_AR = 6,
    RAF_FMT_CAB = 7,
    RAF_FMT_7Z = 8,
    RAF_FMT_VHD = 9,
    RAF_FMT_VHDX = 10,
    RAF_FMT_RAW = 11,
    RAF_FMT_RAFDISK = 12,
    RAF_FMT_ARG_TOKEN_VAZIO = 13
} raf_format_id_v1;

typedef enum raf_roundtrip_grade_v1 {
    RAF_R0_EXACT_BYTES = 0,
    RAF_R1_STRUCTURAL = 1,
    RAF_R2_SEMANTIC = 2,
    RAF_R3_LOSSY_DECLARED = 3,
    RAF_R4_PROHIBITED = 4
} raf_roundtrip_grade_v1;

typedef struct raf_ro_cursor_v1 {
    const raf_u8 *base;
    raf_u64 size;
    raf_u64 off;
} raf_ro_cursor_v1;

typedef struct raf_rw_cursor_v1 {
    raf_u8 *base;
    raf_u64 size;
    raf_u64 off;
} raf_rw_cursor_v1;

typedef struct raf_extent_v1 {
    raf_u64 src_offset;
    raf_u64 src_length;
    raf_u64 dst_offset;
    raf_u64 dst_length;
    raf_u64 alignment;
    raf_u64 flags;
    raf_u32 codec_id;
    raf_u32 integrity_id;
} raf_extent_v1;

typedef struct raf_ir_v1 {
    raf_u32 abi_version;
    raf_u32 format_id;
    raf_u64 source_size;
    raf_u64 logical_size;
    raf_u64 feature_flags;
    raf_u64 extent_count;
    const raf_extent_v1 *extents;
} raf_ir_v1;

typedef struct raf_limits_v1 {
    raf_u64 max_input_bytes;
    raf_u64 max_output_bytes;
    raf_u64 max_entries;
    raf_u64 max_extents;
    raf_u64 max_name_bytes;
    raf_u64 max_recursion_depth;
    raf_u64 max_alignment;
    raf_u64 max_ratio_expansion_milli;
    raf_u64 memory_budget_bytes;
} raf_limits_v1;

typedef struct raf_capability_edge_v1 {
    raf_u32 source_format;
    raf_u32 target_format;
    raf_u32 roundtrip_grade;
    raf_u32 deterministic;
    raf_u64 required_flags;
    raf_u64 preserved_flags;
    raf_u64 lost_flags;
} raf_capability_edge_v1;

static inline raf_status_v1 raf_add_u64_checked(
    raf_u64 a, raf_u64 b, raf_u64 *out)
{
    if (!out) return RAF_E_ARGUMENT;
    if (a > RAF_U64_MAX_VALUE - b) return RAF_E_OVERFLOW;
    *out = a + b;
    return RAF_OK;
}

static inline raf_status_v1 raf_mul_u64_checked(
    raf_u64 a, raf_u64 b, raf_u64 *out)
{
    if (!out) return RAF_E_ARGUMENT;
    if (a != 0u && b > RAF_U64_MAX_VALUE / a) return RAF_E_OVERFLOW;
    *out = a * b;
    return RAF_OK;
}

static inline raf_status_v1 raf_align_up_u64(
    raf_u64 value, raf_u64 alignment, raf_u64 *out)
{
    raf_u64 mask;
    if (!out) return RAF_E_ARGUMENT;
    if (alignment == 0u || (alignment & (alignment - 1u)) != 0u)
        return RAF_E_ALIGNMENT;
    mask = alignment - 1u;
    if (value > RAF_U64_MAX_VALUE - mask) return RAF_E_OVERFLOW;
    *out = (value + mask) & ~mask;
    return RAF_OK;
}

static inline raf_status_v1 raf_range_check_u64(
    raf_u64 offset, raf_u64 length, raf_u64 total)
{
    if (offset > total) return RAF_E_BOUNDS;
    if (length > total - offset) return RAF_E_BOUNDS;
    return RAF_OK;
}

static inline raf_status_v1 raf_ro_take_v1(
    raf_ro_cursor_v1 *cursor, raf_u64 length, const raf_u8 **out)
{
    raf_status_v1 status;
    if (!cursor || !out) return RAF_E_ARGUMENT;
    if (cursor->size > (raf_u64)RAF_UPTR_MAX_VALUE) return RAF_E_LIMIT;
    if (!cursor->base) {
        if (cursor->size != 0u || cursor->off != 0u || length != 0u)
            return RAF_E_ARGUMENT;
        *out = cursor->base;
        return RAF_OK;
    }
    status = raf_range_check_u64(cursor->off, length, cursor->size);
    if (status != RAF_OK) return status;
    *out = cursor->base + (raf_uptr)cursor->off;
    cursor->off += length;
    return RAF_OK;
}

static inline raf_u16 raf_load_le16(const raf_u8 *p)
{
    return (raf_u16)((raf_u16)p[0] | ((raf_u16)p[1] << 8));
}

static inline raf_u32 raf_load_le32(const raf_u8 *p)
{
    return (raf_u32)((raf_u32)p[0]
        | ((raf_u32)p[1] << 8)
        | ((raf_u32)p[2] << 16)
        | ((raf_u32)p[3] << 24));
}

static inline raf_u64 raf_load_le64(const raf_u8 *p)
{
    return (raf_u64)raf_load_le32(p)
        | ((raf_u64)raf_load_le32(p + 4) << 32);
}

static inline raf_u32 raf_load_be32(const raf_u8 *p)
{
    return (raf_u32)(((raf_u32)p[0] << 24)
        | ((raf_u32)p[1] << 16)
        | ((raf_u32)p[2] << 8)
        | (raf_u32)p[3]);
}

/* Implementations must keep portable-C semantics as the functional oracle. */
typedef raf_status_v1 (*raf_probe_fn_v1)(
    raf_ro_cursor_v1 input,
    const raf_limits_v1 *limits,
    raf_ir_v1 *out_ir);

typedef raf_status_v1 (*raf_verify_fn_v1)(
    raf_ro_cursor_v1 input,
    const raf_ir_v1 *expected,
    raf_u64 policy_flags);

#if defined(__cplusplus)
}
#endif

#endif /* RAFAELIA_RAF_CORE_V1_H */
