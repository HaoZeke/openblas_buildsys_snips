---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Interface

The interface directory within the OpenBLAS repository is critical, serving as a
foundational component that bridges high-level BLAS API calls with their
corresponding low-level, optimized implementations. The key point are that these
contain...

**Wrapper Functions**: Housing C wrapper functions that which are the entry
points for the API calls, ensuring that the correct, optimized kernel is
executed based on the architecture and the specific operation being performed.

In essence, the interface directory encapsulates the strategic integration of
compatibility, efficiency, and user accessibility, which is a pretty good
design.

## Buildsystem Perspective

`make` handles each object file on its own, so that won't be covered further.
Let's delve into the `cmake` perspective and then the equivalent `meson`
perspective.

### CMake `OBJECT Library`
In CMake an OBJECT library compiles source files into object files without
archiving them into a library file. This approach is useful for compiling code
that will be used in multiple targets without recompiling the source multiple
times. In the context of OpenBLAS, compiling the interface directory as an
OBJECT library allows these compiled objects (wrappers and interface functions)
to be reused across different final targets (e.g., shared and static versions of
the library). The linker can then resolve symbols to the optimized
implementations, which might be compiled separately and linked together in the
final build step.

### Meson `static_library`
Similarly, in Meson, a `static_library` is a collection of object files archived
together.  When we compile source files from the interface directory into a
`static_library`, we effectively prepare a library which contains all the
wrapper functions which act as entry points to the optimized routines. These
wrappers can invoke different implementations based on the compile-time or
runtime conditions (e.g., architecture-specific optimizations). The unresolved
symbols in this static library (like calls to the optimized kernels) are
intentionally left for the linker to resolve, allowing for flexible linking with
other parts of the project that implement these symbols.

#### Relevant discussions

See [gh-11591](https://github.com/mesonbuild/meson/discussions/11591) for a
discussion on porting `cmake` object libraries to `meson`.

```python

```
