# Upstream contribution scheme

The general context for the `openblas` work was to integrate with `scipy`. In practice the pipeline for this is a bit like this:
- Fixes / changes go to [OpenBLAS](https://github.com/OpenMathLib/OpenBLAS)
- Finalized bindings go to [wrapdb](https://github.com/mesonbuild/wrapdb/pull/1734)
- SciPy updates its `wrapdb` [recipe](https://github.com/scipy/scipy/pull/22047)

## Process

In practice, this means integration testing with `scipy`.

```bash
PKG_CONFIG_PATH="$(OPENBLAS_GITROOT)/../pkgconfig" python dev.py build -C-Dblas=meson-openblas -C-Dlapack=meson-openblas
```

## WrapDB

See this original PR.

```bash
export DDIR="/home/rgoswami/Git/Github/Quansight/wrapdb/subprojects/packagefiles/openblas"
export SDIR="/home/rgoswami/Git/Github/Quansight/OpenBLAS" 
rsync -zarv --prune-empty-dirs --include="*/" --include="meson_options.txt" --exclude="*" $SDIR/ $DDIR
rsync -zarv --prune-empty-dirs --include="*/" --include="meson.build" --exclude="*" $SDIR/ $DDIR
# Remove benchmarks
```

## Relevant samples


