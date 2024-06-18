# micropython-fnv1a32
[FNV1a32](http://www.isthe.com/chongo/tech/comp/fnv) is a simple 32-bit hash function that is optimized for speed while maintaining a low collision rate.

This repo implements a [micropython native module](https://docs.micropython.org/en/latest/develop/natmod.html) of the fnv1a32 hash function. To use a precompiled micropython native module, download the appropriate architecture/micropython-version [from the release page](https://github.com/BrianPugh/micropython-fnv1a32/releases).
Requires MicroPython `>1.22.0`.

# Usage
This library supplies a single function, `fnv1a32`, that can handle a variety of datatypes. The resulting hash is an `integer` object (not `bytes`!).

### Hashing Data In-Memory
To hash `bytes`/`bytearray`/`str` in-memory:

```python
from fnv1a32 import fnv1a32

fnv1a32_hash = fnv1a32(b"this is the data to be hashed")
```

To continue hashing, supply the previous hash into the next `fnv1a32` invocation:

```python
from fnv1a32 import fnv1a32

fnv1a32_hash = fnv1a32(b"this is the data to be hashed")
fnv1a32_hash = fnv1a32(b"more data", fnv1a32_hash)
```

### Hashing File
To hash a file:

```python
from fnv1a32 import fnv1a32

with open("foo.bin") as f:
    # Defaults to using 4096-byte chunks
    fnv1a32_hash = fnv1a32(f)
```

To read and hash bigger chunks at a time (uses more memory, may improve speed):

```python
from fnv1a32 import fnv1a32

with open("foo.bin") as f:
    fnv1a32_hash = fnv1a32(f, buffer_size=16384)
```

# Unit Testing
To run the unittests, install [Belay](https://github.com/BrianPugh/belay/tree/main) and run the following commands:

```bash
make clean
make

belay run micropython -m unittest tests/test_fnv1a32.py
```

# Benchmark
The following were benchmarked on an rp2040 hashing 50KB of data in-memory.

| Implementation             | Bytes/s   | Relative Speed |
|----------------------------|-----------|----------------|
| vanilla micropython        | 18,325    | 1.00x          |
| @micropython.native        | 19,229    | 1.05x          |
| @micropython.viper         | 2,437,954 | 133.04x        |
| micropython native module  | 8,744,316 | 477.18x        |

To run the benchmark, install [Belay](https://github.com/BrianPugh/belay/tree/main) and run the following commands:

```bash
export MPY_DIR=../micropython  # Replace with your micropython directory.
make clean
ARCH=armv6m make  # Change the arch if running on different hardware.

belay install /dev/ttyUSB0 --with=dev
belay sync /dev/ttyUSB0 fnv1a32.mpy
belay run /dev/ttyUSB0 benchmark/fnv1a32_benchmark.py
```
