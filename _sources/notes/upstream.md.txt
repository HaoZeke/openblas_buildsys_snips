# Upstream contribution scheme

The general context for the `openblas` work was to integrate with `scipy`. In practice the pipeline for this is a bit like this:
- Fixes / changes go to [OpenBLAS](https://github.com/OpenMathLib/OpenBLAS)
- Finalized bindings go to [wrapdb](https://github.com/mesonbuild/wrapdb/pull/1734)
- SciPy updates its `wrapdb` [recipe](https://github.com/scipy/scipy/pull/22047)

## Process

In practice, this means integration testing with `scipy`.
