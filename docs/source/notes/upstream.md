# Upstream contribution scheme

The general context for the `openblas` work was to integrate with `scipy`. In practice the pipeline for this is a bit like this:
- Fixes / changes go to [OpenBLAS](https://github.com/OpenMathLib/OpenBLAS)
- Finalized bindings go to [wrapdb](https://github.com/mesonbuild/wrapdb/pull/1734)
- SciPy updates its `wrapdb` [recipe](https://github.com/scipy/scipy/pull/22047)

## Process

In practice, this means integration testing with `scipy`.

```python
import scipy.linalg

print(scipy.linalg.get_blas_funcs('axpy'))
print(scipy.linalg.get_lapack_funcs('gesvd'))
```

Actually similar to `numpy.show_config()` we can double check what's getting used.

```python
scipy.show_config('dicts')['Build Dependencies']
```

### Baseline

Remember the library locations can be queried from:

```bash
LD_LIBRARY_PATH=${SOMTHIN} gcc --print-file-name=libopenblas.so
# or
PKG_CONFIG_PATH=${WHTEVA} --cflags --libs openblas
```

```bash
cd ${OPENBLAS_GITROOT}
# bless is optional, helps with logging
bless --label makelog_sys -- make -j$(nproc)
make install PREFIX=$(pwd)/local-make
```

Now over to `scipy`.

```bash
PKG_CONFIG_PATH="${OPENBLAS_GITROOT}/local-make/lib/pkgconfig" python dev.py build -C-Dblas=openblas -C-Dlapack=openblas
python dev.py test -- -k linprog -x
# ...?
```

Which yields:

```bash
💻  ninja -C /home/rgoswami/Git/Github/ScientificPython/scipy/build -j10
ninja: Entering directory `/home/rgoswami/Git/Github/ScientificPython/scipy/build'
[2/338] Generating subprojects/highs/src/HConfig.h with a custom command
Build OK
💻  meson install -C build --only-changed --tags runtime,python-runtime,tests,devel
Installing, see meson-install.log...
Installation OK
SciPy from development installed path at: /home/rgoswami/Git/Github/ScientificPython/scipy/build-install/lib/python3.12/site-packages
Running tests for scipy version:1.16.0.dev0+git20250410.aeaed57, installed at:/home/rgoswami/Git/Github/ScientificPython/scipy/build-install/lib/python3.12/site-packages/scipy
===================================== test session starts =====================================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/rgoswami/Git/Github/ScientificPython/scipy
configfile: pytest.ini
plugins: anyio-4.3.0, cov-5.0.0, approvaltests-0.2.4, datadir-1.5.0, approvaltests-14.3.0, benchmark-5.1.0, hypothesis-6.130.6, xdist-3.6.1, timeout-2.3.1
collected 19 items / 1 error                                                                  

=========================================== ERRORS ============================================
_ ERROR collecting build-install/lib/python3.12/site-packages/scipy/_lib/tests/test__util.py __
ImportError while importing test module '/home/rgoswami/Git/Github/ScientificPython/scipy/build-install/lib/python3.12/site-packages/scipy/_lib/tests/test__util.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../../../../../Python/openblas_buildsys_snips/.pixi/envs/default/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
scipy/_lib/tests/test__util.py:21: in <module>
    from scipy import cluster, interpolate, linalg, optimize, sparse, spatial, stats
scipy/__init__.py:131: in __getattr__
    return _importlib.import_module(f'scipy.{name}')
../../../../../../Python/openblas_buildsys_snips/.pixi/envs/default/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
scipy/cluster/__init__.py:27: in <module>
    from . import vq, hierarchy
scipy/cluster/vq.py:76: in <module>
    from scipy.spatial.distance import cdist
scipy/spatial/__init__.py:116: in <module>
    from ._geometric_slerp import geometric_slerp
scipy/spatial/_geometric_slerp.py:7: in <module>
    from scipy.spatial.distance import euclidean
scipy/spatial/distance.py:122: in <module>
    from . import _hausdorff, _distance_pybind, _distance_wrap
E   ImportError: /home/rgoswami/Git/Github/ScientificPython/scipy/build-install/lib/python3.12/site-packages/scipy/spatial/_distance_pybind.cpython-312-x86_64-linux-gnu.so: undefined symbol: __cxa_call_terminate
=================================== short test summary info ===================================
ERROR scipy/_lib/tests/test__util.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
====================================== 1 error in 0.13s =======================================
```

Although its nice to know at-least some of these are working..

```bash
python dev.py ipython
```

```python
import numpy as np
from scipy.linalg import lapack
a=np.random.rand(4,4)
lapack.dpotrf(a, np.zeros(4))
```

### With `meson`

```bash
PKG_CONFIG_PATH="${OPENBLAS_GITROOT}/../pkgconfig" python dev.py build -C-Dblas=meson-openblas -C-Dlapack=meson-openblas
python dev.py test -- -k linprog -x
# ...? AGAIN.
```

Though once again, things work out just fine in most cases.

```bash
python dev.py ipython
```

```python
import numpy as np
from scipy.linalg import lapack
a=np.random.rand(4,4)
lapack.dpotrf(a, np.zeros(4))
```

## WrapDB Updates

Basically copy over everything and ditch the `benchmarks` folder.

```bash
export DDIR="/home/rgoswami/Git/Github/Quansight/wrapdb/subprojects/packagefiles/openblas"
export SDIR="/home/rgoswami/Git/Github/Quansight/OpenBLAS" 
rsync -zarv --prune-empty-dirs --include="*/" --include="meson_options.txt" --exclude="*" $SDIR/ $DDIR
rsync -zarv --prune-empty-dirs --include="*/" --include="meson.build" --exclude="*" $SDIR/ $DDIR
# Remove benchmarks
```

## Relevant samples


