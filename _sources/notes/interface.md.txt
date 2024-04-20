# Interface

This is where the high level wrappers to the kernel functions are implemented.
This is a unifying layer with very little in the way of numerical
implementation.

- `cblas_` wrappers are not generated for symbols which use `q` or `x`, i.e.
  which define `XDOUBLE`, a.k.a `long double`.
- Some of the `BLAS Extensions` in the Makefile are not defined within the
  `interface` folder (as of [this commit])

  [this commit]:
    https://github.com/HaoZeke/OpenBLAS/commit/a107c63894475bcbaf31de46537eb088e2ad547d
