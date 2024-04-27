# Testing OpenBLAS

To test the OpenBLAS build, we will focus on

- The OpenBLAS tests
- Integration tests through NumPy

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
