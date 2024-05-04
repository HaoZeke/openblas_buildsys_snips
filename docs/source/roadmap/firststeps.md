# First steps

The idea is to follow along with the evolution of the `CMakelists.txt` file, the
history of which
[is here](https://github.com/OpenMathLib/OpenBLAS/commits/develop/CMakeLists.txt?after=b1e8ba50173423dd1999c7e1bc97c93039efc5e3+174).

Note that though the evolution of the `CMakeLists` is used, the conversion
itself follows the `Makefile`, along with the regex functions defined in this
library.

Broadly speaking this proceeds along the following path:

0. [x] Hardcode some of the default `config` generation mechanism (port them
       later)

- `f_check` and `c_check`
- `prebuild` and `system`

1. [ ] Port the `interface`
2. [ ] `driver/level2`
3. [ ] `driver/level3`
4. [ ] `driver/others`
5. [ ] `kernel`, which will need to dynamically choose the right one
6. [ ] Optionally construct and add `lapacke` and the other bells and whistles

Essentially means steps 1 through 5 can be broken down into the following:

- **Interfaces** :: Primarily contains wrapper functions for BLAS API calls for
  interfacing with higher-level BLAS functions but do not contain the
  computational kernels themselves.

- **Drivers** :: Include some optimized implementations for Level 2 and Level 3
  BLAS operations, such as matrix-vector and matrix-matrix multiplications.
  These still rely on lower-level kernels for the actual computations.

- **Kernels**: This is where the core computational kernels reside. These
  kernels are highly optimized for specific architectures and perform the
  low-level arithmetic operations called by higher-level functions.

Of course, OpenBLAS includes lapack as well, but that is a later concern.

## Architectures

The way OpenBLAS is meant to run optimizations depends on processor families,
e.g. HASWELL or SANDYBRIDGE. Typically this means that the "nearest"
architecture might be used as a starting point for even more optimizations.
