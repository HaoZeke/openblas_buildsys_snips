
# Table of Contents

1.  [About](#org2408634)
    1.  [Why](#org3dc2317)
    2.  [Usage](#org0c30ebb)
    3.  [Documentation](#org9bc2ecc)
        1.  [Readme](#org6a84874)
2.  [License](#orgeffcaee)


<a id="org2408634"></a>

# About

A set of tiny functions to keep the `meson.build` files for OpenBLAS in sync
with the corresponding `Makefiles`.


<a id="org3dc2317"></a>

## Why

For testing the constituent regular expressions and to keep a single notebook to
help construct paired build systems.


<a id="org0c30ebb"></a>

## Usage

The documentation consists of notebooks which can be taken as a rough chart of
porting away from `Makefiles` and `CMake`.

While the library can be installed via `pip` and then used in scripts, that
would be rather odd at this point in its developement. The idea is to mostly
generate snippets and copy them into `meson.build` files by hand for now, later
these can form the basis of a templated system for automating updates further.


<a id="org9bc2ecc"></a>

## Documentation


<a id="org6a84874"></a>

### Readme

The `readme` can be constructed via:

    ./scripts/org_to_md.sh readme_src.org readme.md


<a id="orgeffcaee"></a>

# License

MIT.

