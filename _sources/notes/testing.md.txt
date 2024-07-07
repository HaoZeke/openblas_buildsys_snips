# Testing OpenBLAS

To test the OpenBLAS build, we will focus on

- The OpenBLAS tests
- Integration tests through NumPy

## OpenBLAS tests

The `cblas` tests are of primary interest. So:

```bash
meson setup bbdir --prefix $(pwd)/local
meson install -C bbdir
```

Coupled with a simple patch for the `ctest/Makefile`:

```diff
diff --git i/ctest/Makefile w/ctest/Makefile
index 6c7cc1ed5..1e58e49af 100644
--- i/ctest/Makefile
+++ w/ctest/Makefile
@@ -30,7 +30,7 @@ endif
 override TARGET_ARCH=
 override TARGET_MACH=
 
-LIB = $(TOPDIR)/$(LIBNAME)
+LIB = $(TOPDIR)/local/lib/libopenblas.a
 
 stestl1o = c_sblas1.o
```

Which lets us run the tests via `make`:

```bash
cd ctest
make clean
make
```

In the early stages, this should bring up a bunch of undefined reference to
symbols, all of which need to be fixed before moving on.

## NumPy and OpenBLAS

To check what is already present, `numpy.show_config()` can be used [^1]:

```python
from pprint import pprint as pp
import numpy as np
pp(np.show_config('dicts')['Build Dependencies'])
```

Which will, for a Linux machine and `pip` based implementation yield something
like:

    {'blas': {'detection method': 'pkgconfig',
              'found': True,
              'include directory': '/usr/local/include',
              'lib directory': '/usr/local/lib',
              'name': 'openblas64',
              'openblas configuration': 'USE_64BITINT=1 DYNAMIC_ARCH=1 '
                                        'DYNAMIC_OLDER= NO_CBLAS= NO_LAPACK= '
                                        'NO_LAPACKE= NO_AFFINITY=1 USE_OPENMP= '
                                        'HASWELL MAX_THREADS=2',
              'pc file directory': '/usr/local/lib/pkgconfig',
              'version': '0.3.23.dev'},
     'lapack': {'detection method': 'internal',
                'found': True,
                'include directory': 'unknown',
                'lib directory': 'unknown',
                'name': 'dep140551260102944',
                'openblas configuration': 'unknown',
                'pc file directory': 'unknown',
                'version': '1.26.4'}}

### Relevant build flags

For the newer `meson` builds, the easiest way to set and pass commands is to
use:

```sh
spin build -- -Dblas="none" -Dallow-noblas=true
spin run $SHELL
```

In particular we have:

- `allow-noblas=false` which should be passed when compiling with a custom
  OpenBLAS
- `-Dpkg_config_path=${PWD}/myopenblas`

Where for the `pkg_config_path` contains something like this `openblas.pc` file:

    prefix=/home/rgoswami/something/OpenBLAS
    includedir=${prefix}
    libdir=${prefix}/bbdir

    Name: openblas
    Description: OpenBLAS meson
    Version: 0.3.19
    Cflags: -I${includedir}/openblas
    Libs: -L${libdir} -lopenblas

Note that unfortunately, the `build` and `build-install` directories need to be
fully wiped between runs[^2] .

## Debugging

One of the simpler tests which should call OpenBLAS is simply:

```bash
spin test -t numpy -m full -- -vvvvvv -k "dotmatmat"
```

Which can be coupled with the debug build:

```bash
# Make build
CFLAGS="-O0 -g -ggdb3" \
CXXFLAGS="-O0 -g -ggdb3" \
spin build --clean \
-- -Dblas="openblas" \
-Dblas-order=openblas,mkl,blis \
-Dlapack-order=openblas,mkl,lapack \
-Dallow-noblas=true \
-Dpkg_config_path="$HOME/OpenBLAS/tmpmake/lib/pkgconfig" \
-Dbuildtype=debug \
-Ddisable-optimization=true
# meson build
CFLAGS="-O0 -g -ggdb3" \
CXXFLAGS="-O0 -g -ggdb3" \
spin build --clean \
-- -Dblas="openblas" \
-Dblas-order=openblas,mkl,blis \
-Dlapack-order=openblas,mkl,lapack \
-Dallow-noblas=true \
-Dpkg_config_path="$HOME/OpenBLAS" \
-Dbuildtype=debug \
-Ddisable-optimization=true 
```

The relevant breakpoint should be `cblas_matrixproduct` which should be called
by `PyArray_MatrixProduct2` when `np.dot` is used in a script.

For example, extracting a test from the repo:

```python
# optest.py
import numpy as np
from numpy.testing import assert_almost_equal

np.random.seed(128)
A = np.random.rand(4, 2)
N = 7

res = np.dot(A.transpose(), A)
tgt = np.array([[1.45046013, 0.86323640],
                [0.86323640, 0.84934569]])

assert_almost_equal(res, tgt, decimal=N)
```

```bash
spin gdb optest.py
```

### Baseline tests

Despite the elegance of using `np.show_config`[^3] to figure out what was
actually present at build time, it is reasonable to attempt to have a more
algorithmic approach to determining if OpenBLAS is present.

In this instance, the goal is not to release a series of lifetime benchmarks[^4]
, and so a simpler `pytest-benchmark` setup will suffice.

### Gotchas and Notes

#### `meson` smoke tests

It turns out merely having a `.pc` file and some (but not all) symbols defined
is not good enough. The precise test that the vendored `meson` in NumPy will
perform to determine if `blas` is working as expected is a `dgemm` call.
Specifically it that the following snippet compiles.

```c
#ifdef __cplusplus
extern "C" {
#endif
void dgemm_();
void cblas_dgemm();
int main(int argc, const char *argv[]) {
  dgemm_();
  cblas_dgemm();
  return 0;
}
#ifdef __cplusplus
}
#endif
```

Which means that merely wrapping the L1 symbols is not enough to test with
`numpy`. However, it is possible to provide a dummy / stub to generate the
symbol.

##### Into the rabbit hole

It turns out this is check is part of
`vendored-meson/meson/mesonbuild/dependencies/blas_lapack.py`, which in turn
comes from [the NumPy fork] of `meson` specifically:

```python
...
    def check_symbols(self, compile_args, suffix=None, check_cblas=True,
                      check_lapacke=True, lapack_only=False) -> None:
        # verify that we've found the right LP64/ILP64 interface
        symbols = []
        if not lapack_only:
            symbols += ['dgemm_']
        if check_cblas and self.needs_cblas:
            symbols += ['cblas_ddot']
        if self.needs_lapack:
            symbols += ['zungqr_']
        if check_lapacke and self.needs_lapacke:
            symbols += ['LAPACKE_zungqr']
...
```

The simplest handling is therefore to remove the `symbols += ['dgemm_']` and
conditional altogether. However, though this will compile, it will lead to
import errors:

```sh
ImportError: /python3.11/site-packages/numpy/_core/_multiarray_umath.cpython-311-x86_64-linux-gnu.so: undefined symbol: sgemm_small_kernel_b0_nn
```

So it might still be worthwhile to simply wait until the L3 symbols are ready
before testing with NumPy itself.

#### False starts

These are possible methods to determine if `numpy` uses the default internal
implementation or dispatches to an external OpenBLAS, but these are less than
ideal:

- Use `memray run blas_ops.py` with `memray flamegraph $OUTPUTFILE` and check if
  `@array_function_dispatch` is present or if `_SimpleCData` was loaded from
  `ctypes`
  - While this works, it is rather slow and manual

[^1]:
    The subsequent snippet works on 1.26 and above, earlier versions do not
    support 'dicts'

[^2]:
    However, while porting, note that this may not be enough to detect OpenBLAS
    with `meson`, as discussed in the Gotchas section

[^3]: Not to mention the "eyeball" norm
[^4]: Hence no `asv` usage

[the NumPy fork]:
  https://github.com/numpy/meson/blob/main-numpymeson/mesonbuild/dependencies/blas_lapack.py
