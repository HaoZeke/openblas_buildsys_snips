import pytest
from openblas_buildsys_snips.make.blas_kernel import parse_makefile_lines
from pathlib import Path


def test_with_provided_base(datadir):
    lines = (datadir / "Makefile.L2").read_text()
    expected_ger = {
        "base": "ger",
        "modes": {
            "s": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
            "d": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
            "q": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
            "c": {
                "dir": "generic",
                "kernel": "ger_k.c",
                "exts": ["u_k", "c_k", "v_k", "d_k"],
            },
            "z": {
                "dir": "generic",
                "kernel": "ger_k.c",
                "exts": ["u_k", "c_k", "v_k", "d_k"],
            },
            "x": {
                "dir": "generic",
                "kernel": "ger_k.c",
                "exts": ["u_k", "c_k", "v_k", "d_k"],
            },
        },
    }
    expected_geru = {
        "base": "geru",
        "modes": {
            "c": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
            "z": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
            "x": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
        },
    }
    expected_gerc = {
        "base": "gerc",
        "modes": {
            "c": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
            "z": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
            "x": {"dir": "generic", "kernel": "zger.c", "exts": ["_k"]},
        },
    }
    assert (
        parse_makefile_lines(lines.split("\n"), "generic", "ger_k.c", base="ger")
        == expected_ger
    )
    assert (
        parse_makefile_lines(lines.split("\n"), "generic", "zger.c", base="geru")
        == expected_geru
    )
    assert (
        parse_makefile_lines(lines.split("\n"), "generic", "zger.c", base="gerc")
        == expected_gerc
    )


def test_without_provided_base():
    lines = [
        "$(KDIR)zsymv_U$(TSUFFIX).$(SUFFIX)  $(KDIR)zsymv_U$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZSYMV_U_KERNEL)   $(ZSYMV_U_PARAM)",
        "$(KDIR)ssymv_L$(TSUFFIX).$(SUFFIX)  $(KDIR)ssymv_L$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SSYMV_L_KERNEL)  $(SSYMV_L_PARAM)",
    ]
    expected = {
        "base": "symv",
        "modes": {
            "z": {"dir": "generic", "kernel": "zsymv_k.c", "exts": ["_U"]},
            "s": {"dir": "generic", "kernel": "zsymv_k.c", "exts": ["_L"]},
        },
    }
    assert parse_makefile_lines(lines, "generic", "zsymv_k.c") == expected
