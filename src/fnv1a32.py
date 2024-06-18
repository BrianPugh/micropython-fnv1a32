def fnv1a32(obj, state=0x811C9DC5, *, buffer_size=4096):
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
    buffer_size: int
        If ``obj`` is a file, then process data in chunks of this
        size.
    """
    return _fnv1a32(obj, state, buffer_size)
