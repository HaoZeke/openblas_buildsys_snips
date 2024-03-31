# First steps
The idea is to follow along with the evolution of the `CMakelists.txt` file, the
history of which [is
here](https://github.com/OpenMathLib/OpenBLAS/commits/develop/CMakeLists.txt?after=b1e8ba50173423dd1999c7e1bc97c93039efc5e3+174).

Note that though the evolution of the `CMakeLists` is used, the conversion
itself follows the `Makefile`, along with the regex functions defined in this
library.

Broadly speaking this proceeds along the following path:
0. [X] Hardcode some of the default `config` generation mechanism (port them later)
  - `f_check` and `c_check`
  - `prebuild` and `system`
1. [ ] Port the `interface`
2. [ ] `driver/level2`
3. [ ] `driver/level3`
4. [ ] `driver/others`
5. [ ] `kernel`, which will need to dynamically choose the right one
6. [ ] Optionally construct and add `lapacke` and the other bells and whistles
