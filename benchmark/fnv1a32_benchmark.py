from fnv1a32 import fnv1a32
import micropython
import uprofiler

data = bytes(50_000)


@uprofiler.profile
def fnv1a32_vanilla_micropython(buf):
    h = 0x811C9DC5
    for b in buf:
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


@uprofiler.profile(name="fnv1a32_native")
@micropython.native
def fnv1a32_native(buf):
    h = 0x811C9DC5
    for b in buf:
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


@uprofiler.profile(name="fnv1a32_viper")
@micropython.viper
def fnv1a32_viper(buf: ptr8, length: int) -> uint:
    state = uint(0x811C9DC5)
    for i in range(length):
        b = uint(buf[i])
        state ^= b
        state *= 0x01000193
    return state


fnv1a32_native_module = uprofiler.profile(fnv1a32, name="fnv1a32_native_module")

fnv1a32_vanilla_micropython(data)
fnv1a32_native(data)
fnv1a32_viper(data, len(data))
fnv1a32_native_module(data)

uprofiler.print_results()
