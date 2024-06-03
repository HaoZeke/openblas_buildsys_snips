# NumPy and BLAS
Given that one of the primary aims of having OpenBLAS as a first-class `meson`
subproject is to ease its integration with NumPy it makes sense to cover some of
the mechanics of NumPy and BLAS calls.

Before starting with this, it is instructive to recall that NumPy only uses a
[subset of LAPACK/BLAS](https://mail.python.org/archives/list/numpy-discussion@python.org/thread/PYB2JQH7GCCH5EIBNZFUXITH4LL5U72B/#YFKHWGXE3AWY3TLIUBJU5E33TZ34JD5S) in the first place.

## Dot products
Probably the easiest entry-point is the `PyArray_MatrixProduct`, which in turn
dispatches to `cblas_matrixproduct` which branches to either `syrk` or `gemm`
calls.

Finding the exact call is a bit of a pain, short of stepping through with `gdb`
there isn't much of a fool-proof method.
