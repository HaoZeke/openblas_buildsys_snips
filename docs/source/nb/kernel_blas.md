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

# BLAS Kernels
## Makefiles to `meson.build`
The idea is to use functions from the library to parse the `Makefiles` into an easy to maintain set of `meson.build` files.

+++

### First approximation
The first attempt should be and is just collecting the symbols and the relevant flags. We will use the `generic` variant for an `x86_64` machine.

```{code-cell} ipython3

```
