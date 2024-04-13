---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import openblas_buildsys_snips.make.blas_kernel as opbk
import openblas_buildsys_snips._utils as oputil

from pathlib import Path
```

# BLAS Kernels

## Makefiles to `meson.build`

The idea is to use functions from the library to parse the `Makefiles` into an
easy to maintain set of `meson.build` files.

### First approximation

The first attempt should be and is just collecting the symbols and the relevant
flags. We will use the `generic` variant for an `x86_64` machine.

```python
# For tests
lines = """
$(KDIR)samax_k$(TSUFFIX).$(SUFFIX)  $(KDIR)samax_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SAMAXKERNEL)
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE  -DUSE_ABS -UUSE_MIN $< -o $@

$(KDIR)damax_k$(TSUFFIX).$(SUFFIX)  $(KDIR)damax_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DAMAXKERNEL)
	$(CC) -c $(CFLAGS) -UCOMPLEX -DDOUBLE  -DUSE_ABS -UUSE_MIN $< -o $@

$(KDIR)qamax_k$(TSUFFIX).$(SUFFIX)  $(KDIR)qamax_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(QAMAXKERNEL)
	$(CC) -c $(CFLAGS) -UCOMPLEX -DXDOUBLE -DUSE_ABS -UUSE_MIN $< -o $@

$(KDIR)camax_k$(TSUFFIX).$(SUFFIX)  $(KDIR)camax_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CAMAXKERNEL)
	$(CC) -c $(CFLAGS) -DCOMPLEX -UDOUBLE  -DUSE_ABS -UUSE_MIN $< -o $@

$(KDIR)zamax_k$(TSUFFIX).$(SUFFIX)  $(KDIR)zamax_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZAMAXKERNEL)
	$(CC) -c $(CFLAGS) -DCOMPLEX -DDOUBLE  -DUSE_ABS -UUSE_MIN $< -o $@

$(KDIR)xamax_k$(TSUFFIX).$(SUFFIX)  $(KDIR)xamax_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(XAMAXKERNEL)
	$(CC) -c $(CFLAGS) -DCOMPLEX -DXDOUBLE -DUSE_ABS -UUSE_MIN $< -o $@
""".strip().split('\n')
```

#### Level 1

```python
ml = Path.cwd() / Path("../../../tests/test_blas_symb/Makefile.L1")
lines = ml.read_text().split('\n')
```

```python
opbk.parse_compilation_commands(oputil.pair_suffix_lines(lines), "amax")
```

#### Level 2

These are a straightforward extension of L1 and work pretty much the same way.

```python
ml = Path.cwd() / Path("../../../tests/test_blas_symb/Makefile.L2")
lines = ml.read_text().split('\n')
opbk.parse_compilation_commands(oputil.pair_suffix_lines(lines), "hemv")
```

#### Level 3

```python
ml = Path.cwd() / Path("../../../tests/test_blas_symb/Makefile.L3")
lines = ml.read_text().split('\n')
opbk.parse_compilation_commands(oputil.pair_suffix_lines(lines), "gemm_small_kernel_b0")
```

```python

```
