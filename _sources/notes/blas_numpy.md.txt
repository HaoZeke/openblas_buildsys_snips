# NumPy and BLAS
Given that one of the primary aims of having OpenBLAS as a first-class `meson`
subproject is to ease its integration with NumPy it makes sense to cover some of
the mechanics of NumPy and BLAS calls.

Before starting with this, it is instructive to recall that NumPy only uses a
[subset of LAPACK/BLAS](https://mail.python.org/archives/list/numpy-discussion@python.org/thread/PYB2JQH7GCCH5EIBNZFUXITH4LL5U72B/#YFKHWGXE3AWY3TLIUBJU5E33TZ34JD5S) in the first place.

These are basically `f2c`'d versions of LAPACK, so they're not exactly LAPACKE.

Essentially, only 48 symbols defining 16 operations are necessary:
- {c,d,s,z}copy
 + Copies a vector
 + BLAS L1
- {c,d,s,z}geev
 + Compute eigenvalues, optionally right and/or left eigenvectors
 + (ge)neral matrix (ev) --> eigenvalues
 + LAPACK
- {c,d,s,z}gelsd
- {c,d,s,z}gemm
- {c,d,s,z}gesdd
- {c,d,s,z}gesv
- {c,d,s,z}getrf
- {c,v}heevd
- {c,d,s,z}potrf
- {c,d,s,z}potri
- {c,d,s,z}potrs
- {d,z}geqrf
- {d}orgqr
- {d,s}syevd
- {z}ungqr
- {d}cabs1

`cblas` wrappers also dispatch into `syrk` or `gemm` so it makes sense to look
into them a bit more.

## Dot products
Probably the easiest entry-point is the `PyArray_MatrixProduct`, which in turn
dispatches to `cblas_matrixproduct` which branches to either `syrk` or `gemm`
calls.

Finding the exact call is a bit of a pain, short of stepping through with `gdb`
there isn't much of a fool-proof method.
