lapack_args = []
# Recall from the LAPACK Users Guide 1990 that:
# XYYZZZ
# X -> S (real) | D (double) | C (complex) | Z (double complex)
# YY -> Matrix type
# ZZZ -> computation
#
# We only need to build the following matrix types for OpenBLAS
# GE (general, unsymmetric)
# LA (auxiliary)
# PO (symmetric or Hermitian positive definite)
# TR (triangular or quasi-triangular in some cases)
#
# Along with the following computations:
# TRF (factorize)
# TRS (solve Ax=b by forward / backward substitution)
# SWP (swap rows)
# UUM (product L^HL or UU^H, unblocked)
# UU2 (product L^HL or UU^H, blocked)
# TF2 (Cholesky, unblocked)
# TI2 (triangular matrix inverse, unblocked)
# TRI (inverse)
#
# Note that 2 implies the unblocked version
#
# Specifically we have:
#
# getf2:  GEneral matrix Factorization (unblocked)
# getrf:  GEneral matrix Factorization (blocked)
# getrs:  GEneral matrix solve (using factored matrix)
# laswp:  LA auxiliary routine for swapping rows
# lauu2:  LA auxiliary routine for unblocked matrix factorization
# lauum:  LA auxiliary routine for blocked matrix factorization
# potf2:  POsitive definite matrix factorization (unblocked)
# potrf:  POsitive definite matrix factorization (blocked)
# trti2:  TRiangular matrix Inversion (unblocked)
# trtri:  TRiangular matrix Inversion (blocked)
# trtrs:  TRiangular matrix solve
_lapack_roots = [
    {
        'base': '?getf2_k',
        '_types': ['s', 'd', 'q'],
        'fdir': 'getf2',
        'fname': 'getf2_k.c',
    },
    {
        'base': '?getf2_k',
        '_types': ['c', 'z', 'x'],
        'fdir': 'getf2',
        'fname': 'zgetf2_k.c',
    },
    {
        'base': '?getrf_single',
        '_types': ['s', 'd', 'q', 'c', 'z', 'x'],
        'fdir': 'getrf',
        'fname': 'getrf_single.c',
        'def': ['UNIT'],
    },
    {
        'base': '?getrf_parallel',
        '_types': ['s', 'd', 'q', 'c', 'z', 'x'],
        'fdir': 'getrf',
        'fname': 'getrf_parallel.c',
        'def': ['UNIT'],
        'addl_srcs': ['../param.h'],
    },
    # XXX: laswp has CPU based dispatch.. needs the kern approach
]

_lapack_libs = []
foreach conf : _lapack_roots
    foreach type : conf['_types']
        if 'q' in type or 'x' in type
            # TODO: Figure out when to build these
            # These are the XDOUBLE symbols
            continue
        endif
        # Seed with common args
        compiler_args = _cargs + lapack_args
        # Generate the symbol flags
        base = conf['base']
        # From the root meson.build
        if symb_defs.has_key(base)
            symb_base = symb_defs[base]
            if symb_base.has_key('def')
                foreach _d : symb_base['def']
                    compiler_args += ('-D' + _d)
                endforeach
            endif
            if symb_base.has_key('undef')
                foreach _u : symb_base['undef']
                    compiler_args += ('-U' + _u)
                endforeach
            endif
        endif
        # Set the type arguments
        if precision_mappings.get(type).has_key('def')
            foreach d : precision_mappings[type]['def']
                compiler_args += ['-D' + d]
            endforeach
        endif
        if precision_mappings.get(type).has_key('undef')
            foreach u : precision_mappings[type]['undef']
                compiler_args += ['-U' + u]
            endforeach
        endif

        if conf.has_key('addl')
            compiler_args += conf['addl']
        endif

        # Construct the actual symbol names, and mangled symbols
        # TODO: This might be conditional on other options
        sym_name = conf['base'].replace('?', type)
        sym_underscored = f'@sym_name@_'

        # Construct conditionals
        # If specific to the symbol
        if conf.has_key('def')
            foreach d : conf['def']
                compiler_args += ['-D' + d]
            endforeach
        endif
        if conf.has_key('undef')
            foreach u : conf['undef']
                compiler_args += ['-U' + u]
            endforeach
        endif

        # Make mangled symbols
        # TODO: This might be conditional on other options

        all_srcs = [conf['fdir'] + '/' + conf['fname']]
        if conf.has_key('addl_srcs')
            all_srcs += conf['addl_srcs']
        endif
        # Create the static library for each symbol
        lib = static_library(
            sym_name,
            sources: all_srcs,
            include_directories: _inc,
            c_args: compiler_args + [
                f'-DASMNAME=@asm_name_prefix@@sym_name@',
                f'-DASMFNAME=@asm_name_prefix@@sym_underscored@',
                f'-DNAME=@sym_underscored@',
                f'-DCNAME=@sym_name@',
                f'-DCHAR_NAME="@sym_underscored@"',
                f'-DCHAR_CNAME="@sym_name@"',
            ],
        )
        _lapack_libs += lib
    endforeach
endforeach

_lapack = static_library('_lapack', link_whole: _lapack_libs)
