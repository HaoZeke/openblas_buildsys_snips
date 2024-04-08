# L1 Symbol Sample : `drot`

To demonstrate how the `meson.build` system will work, we will try to generate
an `openblas` library which can be used to compile the following snippet:

```{literalinclude} code_src/drot_example.c
```

## Baseline `openblas`

With system libraries this is a snap:

```bash
gcc drot_example.c -lopenblas -o drotex
./drotex
Resulting vectors:
x: 3.000000 4.000000 5.000000 6.000000 
y: 2.000000 2.000000 2.000000 2.000000 
```

Without a system `openblas`, this works out to:

```bash
gh repo clone openmathlib/openblas openblas_temp
cd openblas_temp
make -j$(nproc)
make PREFIX=./tmpmake install
gcc drot_example.c -o drotex "-I$(pwd)/tmpmake/include" "-L$(pwd)/tmpmake/lib" -lopenblas
./drotex
Resulting vectors:
x: 3.000000 4.000000 5.000000 6.000000 
y: 2.000000 2.000000 2.000000 2.000000 
```

# `meson.build` Outline

As discussed in the roadmap, we need:
- `$GITROOT` :: Where the library is declared
- `interface` :: Where the prefixed symbols `c$BLAS_SYM` are named
- `kernel` :: Where the implementation is `$BLAS_SYM`

## Whittling flags

By inspecting `make` logs, we can get the full set of flags for the interface
symbol , `cblas_drot` in this case are:

```bash
'-O2',
'-DSMALL_MATRIX_OPT',
'-DMAX_STACK_ALLOC=2048',
'-Wall',
'-m64',
'-DF_INTERFACE_GFORT',
'-fPIC',
'-DSMP_SERVER',
'-DNO_WARMUP',
'-DMAX_CPU_NUMBER=12',
'-DMAX_PARALLEL_NUMBER=1',
'-DBUILD_SINGLE=1',
'-DBUILD_DOUBLE=1',
'-DBUILD_COMPLEX=1',
'-DBUILD_COMPLEX16=1',
'-msse3',
'-mssse3',
'-msse4.1',
'-mavx',
'-mavx2',
'-UASMNAME',
'-UASMFNAME',
'-UNAME',
'-UCNAME',
'-UCHAR_NAME',
'-UCHAR_CNAME',
'-DASMNAME=cblas_drot',
'-DASMFNAME=cblas_drot_',
'-DNAME=cblas_drot_',
'-DCNAME=cblas_drot',
'-DCHAR_NAME="cblas_drot_"',
'-DCHAR_CNAME="cblas_drot"',
'-DNO_AFFINITY',
'-DDOUBLE',
'-UCOMPLEX',
'-DCBLAS'
```

Which can be broken into a few different categories.

### Common Configuration Flags

Flags which are set for the build as a whole.

- `SMALL_MATRIX_OPT` :: Which enables, as the name suggests a set of additional,
  optionally implemented kernels for interfaced symbols
- `MAX_STACK_ALLOC` :: Defaults to 2048, [detailed here](https://github.com/OpenMathLib/OpenBLAS/blob/3cf57a61d59a39cc668b21ceafaa006abcfdcf94/common_stackalloc.h#L41-L48) and [here](https://github.com/xianyi/OpenBLAS/pull/482)

Based on the actual Fortran compiler used, the interface definitions need to be
defined as well.

- `F_INTERFACE_GFORT`, `F_INTERFACE_INTEL`, `F_INTERFACE_G95` :: Indicates use of GNU Fortran interface naming conventions. Specific setup in Meson might be needed based on project requirements for Fortran interoperability.

Along with the symbol precision settings:

- `-DBUILD_SINGLE=1`, `-DBUILD_DOUBLE=1`, `-DBUILD_COMPLEX=1`,
  `-DBUILD_COMPLEX16=1` :: Indicate which data types (single, double, complex,
  double complex) to build. These can be configured in Meson using
  `configuration_data()` objects for preprocessor definitions.
- `-DDOUBLE`, `-UCOMPLEX` :: Indicate building with double precision and
  excluding complex number support. Managed in Meson with conditional
  compilation flags or preprocessor symbols using `add_project_arguments()`.

With some affinity and parallel settings as well.

- `SMP_SERVER` :: Enables SMP (Symmetric Multiprocessing) server mode, affecting
  multi-threading and parallel computation. Thread handling in Meson may require
  specific target properties related to threading.
- `NO_WARMUP`, `MAX_CPU_NUMBER=12`, `MAX_PARALLEL_NUMBER=1` :: Control aspects
  of parallel execution and resource allocation, managed through
  `add_project_arguments()` in Meson for compile-time definitions.
- `NO_AFFINITY` :: Disables processor affinity. System-specific setup or dependencies might be required in Meson for thread affinity management.
  
#### Standard build flags

These have direct `meson` [builtin base
option](https://mesonbuild.com/Builtin-options.html#base-options) equivalents:

- `-O2` :: Specifies the optimization level. Controlled in Meson through the `buildtype` or `optimization` options, where `-O2` corresponds to `buildtype=release` or `optimization=2`.
- `-fPIC` :: Enables Position Independent Code, which is a default in Meson for
  shared libraries.
- `-Wall` :: Activates all compiler warnings, aligning with `warning_level=2` or
  higher.

### Hardware conditionals

These depend on detecting the appropriate hardware.

- `-msse3`, `-mssse3`, `-msse4.1`, `-mavx`, `-mavx2` :: These flags activate
  optimizations for Intel's SSE3, SSSE3, SSE4.1, AVX, and AVX2 instruction sets,
  respectively. 

We can detect and apply through the use of
`meson.get_compiler('c').has_argument()` to conditionally add them based on
compiler support.

### Symbol specific flags

These are first unset, and then set. These flags unset certain preprocessor
definitions, potentially to avoid predefined naming schemes conflicting with
OpenBLAS's custom configurations.

<!-- what about *F -->
<!-- CCOMMON_OPT	+= -DASMNAME=$(FU)$(*F) -DASMFNAME=$(FU)$(*F)$(BU) -DNAME=$(*F)$(BU) -DCNAME=$(*F) -DCHAR_NAME=\"$(*F)$(BU)\" -DCHAR_CNAME=\"$(*F)\" -->

- `ASMNAME`, `ASMFNAME`, `NAME`, `CNAME`, `CHAR_NAME`, `CHAR_CNAME`

One approach to this is to set them in a configuration object, as is done by the
`CMakelist` files, or to directly use `c_args`.

## Putting it together

At this point, a simplified `openblas` library can be built up:

```meson
# ...
_inc = include_directories('.')
subdir('interface')
subdir('kernel')
_openblas = static_library('openblas',
                    link_whole: [ _interface, _kern])
# ...
# view targets via meson introspect bbdir --targets
```

With the relevant `c_args` as is done in [this
commit](https://github.com/HaoZeke/OpenBLAS/commit/fa1f52ff7b13e95f2b31096dd65f001ba87b4b3f).
The Meson build can proceed.

```bash
gh repo clone openmathlib/openblas openblas_meson
cd openblas_meson
git checkout fa1f52ff7b13e95f2b31096dd65f001ba87b4b3f
meson setup bbdir
meson compile -C bbdir
gcc trial.c -o drotex "-I$(pwd)/" "-L$(pwd)/bbdir" -lopenblas
Resulting vectors:
x: 3.000000 4.000000 5.000000 6.000000 
y: 2.000000 2.000000 2.000000 2.000000 
```

Perhaps more pertinently, we can view the actual symbols so generated:

```bash
❯ nm -gC bbdir/libopenblas.a | grep drot
bbdir/interface/libcblas_drot.a.p/rot.c.o:
0000000000000000 T cblas_drot
                 U drot_k
bbdir/kernel/libdrot_k.a.p/arm_rot.c.o:
0000000000000000 T drot_k
```

So in this vein we may now proceed building all the L1 symbols.
