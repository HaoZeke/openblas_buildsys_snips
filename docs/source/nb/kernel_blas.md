---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
import openblas_buildsys_snips.make.blas_kernel as opbk
import openblas_buildsys_snips._utils as oputil
```

# BLAS Kernels
## Makefiles to `meson.build`
The idea is to use functions from the library to parse the `Makefiles` into an easy to maintain set of `meson.build` files.

+++

### First approximation
The first attempt should be and is just collecting the symbols and the relevant flags. We will use the `generic` variant for an `x86_64` machine.

```{code-cell} ipython3
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

### AMIN ###

$(KDIR)samin_k$(TSUFFIX).$(SUFFIX)  $(KDIR)samin_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SAMINKERNEL)
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DUSE_ABS  -DUSE_MIN $< -o $@

$(KDIR)damin_k$(TSUFFIX).$(SUFFIX)  $(KDIR)damin_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DAMINKERNEL)
	$(CC) -c $(CFLAGS) -UCOMPLEX -DDOUBLE -DUSE_ABS  -DUSE_MIN $< -o $@

$(KDIR)qamin_k$(TSUFFIX).$(SUFFIX)  $(KDIR)qamin_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(QAMINKERNEL)
	$(CC) -c $(CFLAGS) -UCOMPLEX -DXDOUBLE -DUSE_ABS -DUSE_MIN $< -o $@

$(KDIR)camin_k$(TSUFFIX).$(SUFFIX)  $(KDIR)camin_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CAMINKERNEL)
	$(CC) -c $(CFLAGS) -DCOMPLEX -UDOUBLE -DUSE_ABS  -DUSE_MIN $< -o $@

$(KDIR)zamin_k$(TSUFFIX).$(SUFFIX)  $(KDIR)zamin_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZAMINKERNEL)
	$(CC) -c $(CFLAGS) -DCOMPLEX -DDOUBLE -DUSE_ABS  -DUSE_MIN $< -o $@

$(KDIR)xamin_k$(TSUFFIX).$(SUFFIX)  $(KDIR)xamin_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(XAMINKERNEL)
	$(CC) -c $(CFLAGS) -DCOMPLEX -DXDOUBLE -DUSE_ABS -DUSE_MIN $< -o $@
""".strip().split('\n')
```

```{code-cell} ipython3
opbk.parse_compilation_commands(oputil.pair_kdir_lines(lines), "amax")
```

```{code-cell} ipython3

```
