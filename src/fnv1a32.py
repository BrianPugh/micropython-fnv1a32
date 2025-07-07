def fnv1a32(obj, state=0x811C9DC5, *, buffer=4096):
    """Compute the FNV-1a 32-bit hash of a file.

    Parameters
    ----------
    obj:
        If ``{str, bytes, bytearray}``, is treated as data
        and fed into the hashing engine.
        Otherwise, treated as a file handle and iteratively
        read from until exhausted.
    state: int
        Hash state. Set to a previous FNV1a32 hash to continue
        hashing.
    buffer: int | bytearray
        If ``obj`` is a file, then:
        1. If ``buffer`` is an int, then allocate a buffer of this
           size and read/process data in chunks of this size.
        2. If ``buffer`` is a bytearray/memoryview, then use it
           as the buffer.
    """
    return _fnv1a32(obj, state, buffer)
