#include "raf_core_v1.h"

/*
 * Object-only compile probe. It intentionally has no main, libc, heap, shell,
 * syscall, or target ABI dependency. Runtime assertions belong to a later
 * domain-specific harness; this file proves that the public contract can be
 * consumed by a freestanding translation unit.
 */
int raf_core_v1_contract_probe(void)
{
    raf_u64 out = 0u;
    raf_u8 bytes[8] = { 1u, 2u, 3u, 4u, 5u, 6u, 7u, 8u };
    raf_ro_cursor_v1 cursor = { bytes, 8u, 0u };
    const raf_u8 *view = (const raf_u8 *)0;

    if (raf_align_up_u64(5u, 4u, &out) != RAF_OK || out != 8u)
        return 1;

    if (raf_ro_take_v1(&cursor, 4u, &view) != RAF_OK)
        return 2;

    if (view != bytes || cursor.off != 4u)
        return 3;

    if (raf_add_u64_checked(RAF_U64_MAX_VALUE, 1u, &out)
        != RAF_E_OVERFLOW)
        return 4;

    if (raf_mul_u64_checked(RAF_U64_MAX_VALUE, 2u, &out)
        != RAF_E_OVERFLOW)
        return 5;

    return 0;
}
