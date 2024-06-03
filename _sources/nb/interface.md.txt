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
together. When we compile source files from the interface directory into a
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

## Practicalities

This means that the `interface` is pretty useful, since it includes the
`cblas_definitions`.

```python
import openblas_buildsys_snips.make.blas_kernel as opbk
import openblas_buildsys_snips._utils as oputil

from pathlib import Path
```

```python
ml = Path.cwd() / Path("../../../tests/test_blas_symb/interface_Makefile")
lines = ml.read_text().split('\n')
```

```python
opbk.parse_compilation_commands(oputil.pair_suffix_lines(lines), "min")
```

```python
print(parsed_lines)
```

```python

```

```python
import re

def parse_blas_routine_commands(lines, base):
    """
    Parse BLAS routine compilation commands to extract types and directives.

    Parameters
    ----------
    lines : list of str
        Compilation commands extracted from a Makefile.
    base : str
        Base routine name with a '?' where type letters should be replaced.

    Returns
    -------
    dict
        Dictionary with routine base, types encountered, and associated defines and undefines.
    """
    type_prefixes = ['s', 'd', 'q', 'c', 'z', 'x']
    routine_details = {
        'base': base.replace('?', ''),
        '_types': [],
        'def': [],
        'undef': []
    }

    # Prepare regex to capture the necessary parts
    pattern = re.compile(r'^(\w+)\.\$\((?:SUFFIX|PSUFFIX)\).*?-c(.*?)\$<.*$')

    # Collect information
    for line in lines:
        match = pattern.search(line)
        if match:
            routine_name, flags = match.groups()
            type_char = routine_name[0] if routine_name[0] in type_prefixes else routine_name[:2]
            routine_details['_types'].append(type_char)
            # Process defines and undefines
            routine_details['def'].extend(re.findall(r'-D(\S+)', flags))
            routine_details['undef'].extend(re.findall(r'-U(\S+)', flags))

    # Remove duplicates and sort for consistency
    routine_details['_types'] = sorted(set(routine_details['_types']))
    routine_details['def'] = sorted(set(routine_details['def']))
    routine_details['undef'] = sorted(set(routine_details['undef']))

    return routine_details

# Example lines
lines = [
    'isamax.$(SUFFIX) isamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
    'idamax.$(SUFFIX) idamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
    'icamax.$(SUFFIX) icamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
    'izamax.$(SUFFIX) izamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
    'ixamax.$(SUFFIX) ixamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)'
]

# Example usage
base = '?amax'
result = parse_blas_routine_commands(lines, base)
print(result)

# Example usage with command lines and specifying the base symbols
lines = [
    'smax.$(SUFFIX) smax.$(PSUFFIX) : max.c\t$(CC) $(CFLAGS) -c -UUSE_ABS -UUSE_MIN $< -o $(@F)',
    'dmax.$(SUFFIX) dmax.$(PSUFFIX) : max.c\t$(CC) $(CFLAGS) -c -UUSE_ABS -UUSE_MIN $< -o $(@F)',
    'qmax.$(SUFFIX) qmax.$(PSUFFIX) : max.c\t$(CC) $(CFLAGS) -c -UUSE_ABS -UUSE_MIN $< -o $(@F)',
    'smin.$(SUFFIX) smin.$(PSUFFIX) : max.c\t$(CC) $(CFLAGS) -c -UUSE_ABS -DUSE_MIN $< -o $(@F)',
    'dmin.$(SUFFIX) dmin.$(PSUFFIX) : max.c\t$(CC) $(CFLAGS) -c -UUSE_ABS -DUSE_MIN $< -o $(@F)',
    'qmin.$(SUFFIX) qmin.$(PSUFFIX) : max.c\t$(CC) $(CFLAGS) -c -UUSE_ABS -DUSE_MIN $< -o $(@F)',
    'isamax.$(SUFFIX) isamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
    'idamax.$(SUFFIX) idamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
    'iqamax.$(SUFFIX) iqamax.$(PSUFFIX) : imax.c\t$(CC) $(CFLAGS) -c -DUSE_ABS -UUSE_MIN $< -o $(@F)',
 'srot.$(SUFFIX) srot.$(PSUFFIX) : rot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'drot.$(SUFFIX) drot.$(PSUFFIX) : rot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'qrot.$(SUFFIX) qrot.$(PSUFFIX) : rot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'csrot.$(SUFFIX) csrot.$(PSUFFIX) : zrot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'zdrot.$(SUFFIX) zdrot.$(PSUFFIX) : zrot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'xqrot.$(SUFFIX) xqrot.$(PSUFFIX) : zrot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
     'saxpy.$(SUFFIX) saxpy.$(PSUFFIX) : axpy.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'daxpy.$(SUFFIX) daxpy.$(PSUFFIX) : axpy.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'qaxpy.$(SUFFIX) qaxpy.$(PSUFFIX) : axpy.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'caxpy.$(SUFFIX) caxpy.$(PSUFFIX) : zaxpy.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'zaxpy.$(SUFFIX) zaxpy.$(PSUFFIX) : zaxpy.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'xaxpy.$(SUFFIX) xaxpy.$(PSUFFIX) : zaxpy.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
 'caxpyc.$(SUFFIX) caxpyc.$(PSUFFIX) : zaxpy.c\t$(CC) $(CFLAGS) -c -DCONJ $< -o $(@F)',
 'zaxpyc.$(SUFFIX) zaxpyc.$(PSUFFIX) : zaxpy.c\t$(CC) $(CFLAGS) -c -DCONJ $< -o $(@F)',
 'xaxpyc.$(SUFFIX) xaxpyc.$(PSUFFIX) : zaxpy.c\t$(CC) $(CFLAGS) -c -DCONJ $< -o $(@F)',
]

base_symbols = ['?max', '?min', 'i?amax', '?rot', '?axpy']  # Base symbols with wildcards
parsed_configs = parse_blas_routine_commands(lines, 'axpy')
print(parsed_configs)
```

```python
import re

import re

def parse_blas_routine_commands(lines, symbol):
    prefix, base = symbol.split('?')
    pattern = re.compile(rf'^{prefix}(\w+){base}\.\$\((?:SUFFIX|PSUFFIX)\) : ([^ \t]+)\t.*?-c\s*(.*)$')

    results = {}

    for line in lines:
        matcher = pattern.match(line)
        if matcher:
            type_char, filename, flags = matcher.groups()
            key = (base, filename)
            if key not in results:
                results[key] = {
                    'base': base,
                    'fname': filename.replace('.c', ''),
                    '_types': [],
                    'def': set(),
                    'undef': set(),
                }
            results[key]['_types'].append(type_char)
            results[key]['def'].update(re.findall(r'-D(\w+)', flags))
            results[key]['undef'].update(re.findall(r'-U(\w+)', flags))

    # Convert sets to sorted lists to finalize the structure
    for result in results.values():
        result['_types'] = sorted(set(result['_types']))
        result['def'] = sorted(result['def'])
        result['undef'] = sorted(result['undef'])

    return list(results.values())


# Test the function with a list of lines from a hypothetical Makefile
lines = [
    'srot.$(SUFFIX) srot.$(PSUFFIX) : rot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
    'drot.$(SUFFIX) drot.$(PSUFFIX) : rot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
    'qrot.$(SUFFIX) qrot.$(PSUFFIX) : rot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
    'csrot.$(SUFFIX) csrot.$(PSUFFIX) : zrot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
    'zdrot.$(SUFFIX) zdrot.$(PSUFFIX) : zrot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
    'xqrot.$(SUFFIX) xqrot.$(PSUFFIX) : zrot.c\t$(CC) $(CFLAGS) -c $< -o $(@F)',
]

symbol = '?rot'
result = parse_blas_routine_commands(lines, symbol)
print(result)

```

```python
print(parse_blas_routine_commands([x for x in oputil.pair_suffix_lines(lines)][1:], 'i?amin'))
print(parse_blas_routine_commands([x for x in oputil.pair_suffix_lines(lines)][1:], '?amin'))
print(parse_blas_routine_commands([x for x in oputil.pair_suffix_lines(lines)][1:], '?min'))
```

```python
sam=[x for x in oputil.pair_suffix_lines(lines)][2]
```

```python
sam.split('\t')
```

```python
symb = '?rot'
prefix, base = symb.split('?')
print(base, prefix)
```

```python
'i?amax'.split('?')
```

```python
'?rot'.split('?')
```

```python
import re
import textwrap
from typing import List, Dict, Any

def parse_makefile_lines(lines: List[str]) -> List[Dict[str, Any]]:
    ext_mappings_l3 = []
    pattern = re.compile(
        r'^(?P<name>[a-z]+)(?P<ext>_[A-Z]+)\.\$\(\w+\) : (?P<file>[\w.]+)\s*\n?'
        r'\s*\$\(CC\) -c \$\(CFLAGS\) (?P<flags>.*) \$< -o \$\(@F\)'
    )

    for line in lines:
        match = pattern.match(line)
        if match:
            details = match.groupdict()
            ext_details = {
                'ext': details['ext'],
                'def': [],
                'undef': [],
                'for': []
            }

            # Determine 'for' based on the 'name' prefix
            if details['name'][0] in ['s', 'd']:
                ext_details['for'] = ['s', 'd']
            elif details['name'][0] in ['c', 'z', 'x']:
                ext_details['for'] = ['c', 'z', 'x']
            elif details['name'][0] == 'q':
                ext_details['for'] = ['q']

            # Parse flags
            flags = details['flags'].split()
            for flag in flags:
                if flag.startswith('-D') and flag[2:] not in ['DOUBLE', 'COMPLEX']:
                    ext_details['def'].append(flag[2:])
                elif flag.startswith('-U') and flag[2:] not in ['DOUBLE', 'COMPLEX']:
                    ext_details['undef'].append(flag[2:])

            ext_mappings_l3.append(ext_details)

    return ext_mappings_l3

# Example usage
makefile_lines = [
    'strmm_LNUU.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT $< -o $(@F)',
    'strmm_LNUN.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT $< -o $(@F)',
    'strmm_LNLU.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT $< -o $(@F)',
    'strmm_LNLN.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT $< -o $(@F)',
    'strmm_LTUU.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT $< -o $(@F)',
    'strmm_LTUN.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT $< -o $(@F)',
    'strmm_LTLU.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT $< -o $(@F)',
    'strmm_LTLN.$(SUFFIX) : trmm_L.c\n\t$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT $< -o $(@F)',
]

# Parse the makefile lines
parsed_ext_mappings = parse_makefile_lines(makefile_lines)

# Display the parsed mappings
for entry in parsed_ext_mappings:
    print(entry)

```

```python
from openblas_buildsys_snips import _utils
```

```python
makefile_string = """
strmm_LNUU.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT $< -o $(@F)

strmm_LNUN.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT $< -o $(@F)

strmm_LNLU.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT $< -o $(@F)

strmm_LNLN.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT $< -o $(@F)

strmm_LTUU.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT $< -o $(@F)

strmm_LTUN.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT $< -o $(@F)

strmm_LTLU.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT $< -o $(@F)

strmm_LTLN.$(SUFFIX) : trmm_L.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT $< -o $(@F)

strmm_RNUU.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT $< -o $(@F)

strmm_RNUN.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT $< -o $(@F)

strmm_RNLU.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT $< -o $(@F)

strmm_RNLN.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT $< -o $(@F)

strmm_RTUU.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT $< -o $(@F)

strmm_RTUN.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT $< -o $(@F)

strmm_RTLU.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT $< -o $(@F)

strmm_RTLN.$(SUFFIX) : trmm_R.c
	$(CC) -c $(CFLAGS) -UCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT $< -o $(@F)
"""

for x in parse_makefile_lines(_utils.pair_suffix_lines(makefile_string.split("\n"))):
    print(x)
```

```python
makefile_string = """
ctrmm_LNUU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_LNUN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_LNLU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_LNLN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_LTUU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_LTUN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_LTLU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_LTLN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_LRUU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_LRUN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_LRLU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_LRLN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_LCUU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_LCUN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_LCLU.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_LCLN.$(PSUFFIX) : trmm_L.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_RNUU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_RNUN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_RNLU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_RNLN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_RTUU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_RTUN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_RTLU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT -UCONJ $< -o $(@F)

ctrmm_RTLN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT -UCONJ $< -o $(@F)

ctrmm_RRUU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_RRUN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -DUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_RRLU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_RRLN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -UTRANSA -UUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_RCUU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_RCUN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -DUPPER -UUNIT -DCONJ $< -o $(@F)

ctrmm_RCLU.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -DUNIT -DCONJ $< -o $(@F)

ctrmm_RCLN.$(PSUFFIX) : trmm_R.c
	$(CC) -c $(PFLAGS) -DCOMPLEX -UDOUBLE -DTRANSA -UUPPER -UUNIT -DCONJ $< -o $(@F)
"""

for x in parse_makefile_lines(_utils.pair_suffix_lines(makefile_string.split("\n"))):
    print(x)
```

```python
makefile_string = """
ssymm_LU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -UCOMPLEX -ULOWER -URSIDE -DNN $< -o $(@F)

ssymm_LL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -UCOMPLEX -DLOWER -URSIDE -DNN $< -o $(@F)

ssymm_RU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -UCOMPLEX -ULOWER -DRSIDE -DNN $< -o $(@F)

ssymm_RL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -UCOMPLEX -DLOWER -DRSIDE -DNN $< -o $(@F)

dsymm_LU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -UCOMPLEX -ULOWER -URSIDE -DNN $< -o $(@F)

dsymm_LL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -UCOMPLEX -DLOWER -URSIDE -DNN $< -o $(@F)

dsymm_RU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -UCOMPLEX -ULOWER -DRSIDE -DNN $< -o $(@F)

dsymm_RL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -UCOMPLEX -DLOWER -DRSIDE -DNN $< -o $(@F)

qsymm_LU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -UCOMPLEX -ULOWER -URSIDE -DNN $< -o $(@F)

qsymm_LL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -UCOMPLEX -DLOWER -URSIDE -DNN $< -o $(@F)

qsymm_RU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -UCOMPLEX -ULOWER -DRSIDE -DNN $< -o $(@F)

qsymm_RL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -UCOMPLEX -DLOWER -DRSIDE -DNN $< -o $(@F)

csymm_LU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -DCOMPLEX -ULOWER -URSIDE -DNN $< -o $(@F)

csymm_LL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -DCOMPLEX -DLOWER -URSIDE -DNN $< -o $(@F)

csymm_RU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -DCOMPLEX -ULOWER -DRSIDE -DNN $< -o $(@F)

csymm_RL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -UDOUBLE -DCOMPLEX -DLOWER -DRSIDE -DNN $< -o $(@F)

zsymm_LU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -DCOMPLEX -ULOWER -URSIDE -DNN $< -o $(@F)

zsymm_LL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -DCOMPLEX -DLOWER -URSIDE -DNN $< -o $(@F)

zsymm_RU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -DCOMPLEX -ULOWER -DRSIDE -DNN $< -o $(@F)

zsymm_RL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DDOUBLE -DCOMPLEX -DLOWER -DRSIDE -DNN $< -o $(@F)

xsymm_LU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -DCOMPLEX -ULOWER -URSIDE -DNN $< -o $(@F)

xsymm_LL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -DCOMPLEX -DLOWER -URSIDE -DNN $< -o $(@F)

xsymm_RU.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -DCOMPLEX -ULOWER -DRSIDE -DNN $< -o $(@F)

xsymm_RL.$(SUFFIX) : symm_k.c level3.c ../../param.h
	$(CC) -c $(CFLAGS) -DXDOUBLE -DCOMPLEX -DLOWER -DRSIDE -DNN $< -o $(@F)
"""
```

```python

def parse_makefile_lines(lines: List[str]) -> List[Dict[str, Any]]:
    ext_mappings_l3 = []
    pattern = re.compile(
        r'^(?P<name>[a-z]+)(?P<ext>_[A-Z]+)\.\$\(\w+\) : (?P<file>[\w.]+)\s*\n?'
        r'\s*\$\(CC\) -c \$\(PFLAGS\) (?P<flags>.*) \$< -o \$\(@F\)'
    )

    for line in lines:
        match = pattern.match(line)
        if match:
            details = match.groupdict()
            ext_details = {
                'ext': details['ext'],
                'def': [],
                'undef': [],
                'for': []
            }

            # Determine 'for' based on the 'name' prefix
            if details['name'][0] in ['s', 'd']:
                ext_details['for'] = ['s', 'd']
            elif details['name'][0] in ['c', 'z', 'x']:
                ext_details['for'] = ['c', 'z', 'x']
            elif details['name'][0] == 'q':
                ext_details['for'] = ['q']

            # Parse flags
            flags = details['flags'].split()
            for flag in flags:
                if flag.startswith('-D') and flag[2:] not in ['DOUBLE', 'COMPLEX']:
                    ext_details['def'].append(flag[2:])
                elif flag.startswith('-U') and flag[2:] not in ['DOUBLE', 'COMPLEX']:
                    ext_details['undef'].append(flag[2:])

            ext_mappings_l3.append(ext_details)

    return ext_mappings_l3


for x in parse_makefile_lines(_utils.pair_suffix_lines(makefile_string.split("\n"))):
    print(f'{x},')
```

```python
list(_utils.pair_suffix_lines(makefile_string.split("\n")))
```

```python

```
