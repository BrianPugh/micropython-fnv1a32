ARCH ?= x64
MOD = fnv1a32
SRC = src/fnv1a32.c src/fnv1a32.py
include $(MPY_DIR)/py/dynruntime.mk
