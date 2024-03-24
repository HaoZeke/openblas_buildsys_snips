import pytest
from openblas_buildsys_snips.make.blas_kernel import parse_makefile_lines

# Test cases


def test_with_provided_base():
    lines = """$(KDIR)dger_k$(TSUFFIX).$(SUFFIX)  $(KDIR)dger_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DGERKERNEL) $(DGERPARAM)"
    $(KDIR)cgeru_k$(TSUFFIX).$(SUFFIX)  $(KDIR)cgeru_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CGERUKERNEL) $(CGERPARAM)"
    """
    expected = {
        "base": "ger",
        "modes": {
            "d": {"dir": "generic", "kernel": "ger_k.c", "exts": ["_k"]},
            "c": {"dir": "generic", "kernel": "ger_k.c", "exts": ["u_k"]},
        },
    }
    assert parse_makefile_lines(lines.split('\n'), "generic", "ger_k.c", base="ger") == expected
