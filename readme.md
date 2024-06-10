
# Table of Contents

1.  [About](#orgb178d51)
    1.  [Why](#org1f45efc)
    2.  [Usage](#org2ab8e36)
    3.  [Test generation](#orgf309fc8)
    4.  [Documentation](#orgf2f7bad)
        1.  [Readme](#org900e71e)
        2.  [Sphinx and MyST Markdown](#org5d2e0a8)
        3.  [Generate `org` to `md`](#orgc3df771)
2.  [License](#org93e31bb)


<a id="orgb178d51"></a>

# About

A set of tiny functions to keep the `meson.build` files for OpenBLAS in sync
with the corresponding `Makefiles`.


<a id="org1f45efc"></a>

## Why

For testing the constituent regular expressions and to keep a single notebook to
help construct paired build systems.


<a id="org2ab8e36"></a>

## Usage

The documentation consists of notebooks which can be taken as a rough chart of
porting away from `Makefiles` and `CMake`.

While the library can be installed via `pip` and then used in scripts, that
would be rather odd at this point in its developement. The idea is to mostly
generate snippets and copy them into `meson.build` files by hand for now, later
these can form the basis of a templated system for automating updates further.


<a id="orgf309fc8"></a>

## Test generation

    pip install -e .
    # For the generation
    pip install numpy
    python -m openblas_buildsys_snips.cli --generate
    # Running
    pip uninstall numpy
    # Get it via the spin run $SHELL
    # Run all
    python -m openblas_buildsys_snips.cli --test all --filename tests.json.gz
    # Run one
    python -m openblas_buildsys_snips.cli --test ssyrk_lt --filename tests.json.gz


<a id="orgf2f7bad"></a>

## Documentation


<a id="org900e71e"></a>

### Readme

The `readme` can be constructed via:

    ./scripts/org_to_md.sh readme_src.org readme.md


<a id="org5d2e0a8"></a>

### Sphinx and MyST Markdown

The markdown documentation is typically written with inline styles, but then
re-written to use reference styles via:

    pandoc --reference-links -f gfm $MDFILE -t gfm

These should also always be formatted using `prettier`, for which a style file
is present in `$GITROOT`.


<a id="orgc3df771"></a>

### Generate `org` to `md`

    emacs --script ./scripts/clean_and_convert.el


<a id="org93e31bb"></a>

# License

MIT.

