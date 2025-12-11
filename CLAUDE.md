# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MicroPython native module implementing the FNV-1a 32-bit hash function. It provides a high-performance C implementation that runs ~1000x faster than pure Python on embedded devices like the RP2040.

## Build Commands

Building requires MicroPython source and uses the native module build system:

```bash
# Set the MicroPython source directory
export MPY_DIR=../micropython

# Build for default architecture (x64)
make

# Build for specific architecture (e.g., armv6m for RP2040)
ARCH=armv6m make

# Clean build artifacts
make clean
```

Supported architectures: `x64`, `x86`, `armv6m`, `armv7m`, `armv7emsp`, `armv7emdp`, `xtensa`, `xtensawin`, `rv32imc`

## Running Tests

Tests require [Belay](https://github.com/BrianPugh/belay) to run on MicroPython:

```bash
make clean && make
belay run micropython -m unittest tests/test_fnv1a32.py
```

## Running Benchmarks

Benchmarks run on actual hardware (e.g., RP2040):

```bash
ARCH=armv6m make
belay install /dev/ttyUSB0 --with=dev
belay sync /dev/ttyUSB0 fnv1a32.mpy
belay run /dev/ttyUSB0 benchmark/fnv1a32_benchmark.py
```

## Architecture

- `src/fnv1a32.c` - C implementation of the FNV-1a hash loop with 16-byte unrolling for performance. Handles both buffer objects and file-like objects via `readinto`.
- `src/fnv1a32.py` - Python wrapper exposing the `fnv1a32()` function that calls the C `_fnv1a32()` implementation.
- `Makefile` - Uses MicroPython's `dynruntime.mk` to build the `.mpy` native module.

The module exports a single function `fnv1a32(obj, state=0x811C9DC5, *, buffer=4096)` that accepts bytes/bytearray/str or file-like objects.
