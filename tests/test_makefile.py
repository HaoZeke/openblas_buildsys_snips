import pytest
from openblas_buildsys_snips.make.blas_kernel import parse_makefile_lines


def test_with_provided_base():
    lines = """
$(KDIR)sger_k$(TSUFFIX).$(SUFFIX)  $(KDIR)sger_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SGERKERNEL) $(SGERPARAM)
	$(CC) -c $(CFLAGS) -UDOUBLE $< -o $@
endif

ifeq ($(BUILD_DOUBLE),1)

$(KDIR)dger_k$(TSUFFIX).$(SUFFIX)  $(KDIR)dger_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DGERKERNEL) $(DGERPARAM)
	$(CC) -c $(CFLAGS) -DDOUBLE $< -o $@
endif

$(KDIR)qger_k$(TSUFFIX).$(SUFFIX)  $(KDIR)qger_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(QGERKERNEL) $(QGERPARAM)
	$(CC) -c $(CFLAGS) -DXDOUBLE $< -o $@

ifeq ($(BUILD_COMPLEX),1)

$(KDIR)cgeru_k$(TSUFFIX).$(SUFFIX)  $(KDIR)cgeru_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CGERUKERNEL) $(CGERPARAM)
	$(CC) -c $(CFLAGS) -UDOUBLE -UCONJ $< -o $@

$(KDIR)cgerc_k$(TSUFFIX).$(SUFFIX)  $(KDIR)cgerc_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CGERCKERNEL) $(CGERPARAM)
	$(CC) -c $(CFLAGS) -UDOUBLE -DCONJ $< -o $@

$(KDIR)cgerv_k$(TSUFFIX).$(SUFFIX)  $(KDIR)cgerv_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CGERUKERNEL) $(CGERPARAM)
	$(CC) -c $(CFLAGS) -UDOUBLE -UCONJ -DXCONJ $< -o $@

$(KDIR)cgerd_k$(TSUFFIX).$(SUFFIX)  $(KDIR)cgerd_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(CGERCKERNEL) $(CGERPARAM)
	$(CC) -c $(CFLAGS) -UDOUBLE -DCONJ -DXCONJ $< -o $@
endif

ifeq ($(BUILD_COMPLEX16),1)

$(KDIR)zgeru_k$(TSUFFIX).$(SUFFIX)  $(KDIR)zgeru_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZGERUKERNEL) $(ZGERPARAM)
	$(CC) -c $(CFLAGS) -DDOUBLE -UCONJ $< -o $@

$(KDIR)zgerc_k$(TSUFFIX).$(SUFFIX)  $(KDIR)zgerc_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZGERCKERNEL) $(ZGERPARAM)
	$(CC) -c $(CFLAGS) -DDOUBLE -DCONJ $< -o $@

$(KDIR)zgerv_k$(TSUFFIX).$(SUFFIX)  $(KDIR)zgerv_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZGERUKERNEL) $(ZGERPARAM)
	$(CC) -c $(CFLAGS) -DDOUBLE -UCONJ -DXCONJ $< -o $@

$(KDIR)zgerd_k$(TSUFFIX).$(SUFFIX)  $(KDIR)zgerd_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(ZGERCKERNEL) $(ZGERPARAM)
	$(CC) -c $(CFLAGS) -DDOUBLE -DCONJ -DXCONJ $< -o $@
endif

$(KDIR)xgeru_k$(TSUFFIX).$(SUFFIX)  $(KDIR)xgeru_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(XGERUKERNEL) $(XGERPARAM)
	$(CC) -c $(CFLAGS) -DXDOUBLE -UCONJ $< -o $@

$(KDIR)xgerc_k$(TSUFFIX).$(SUFFIX)  $(KDIR)xgerc_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(XGERCKERNEL) $(XGERPARAM)
	$(CC) -c $(CFLAGS) -DXDOUBLE -DCONJ $< -o $@

$(KDIR)xgerv_k$(TSUFFIX).$(SUFFIX)  $(KDIR)xgerv_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(XGERUKERNEL) $(XGERPARAM)
	$(CC) -c $(CFLAGS) -DXDOUBLE -UCONJ -DXCONJ $< -o $@

$(KDIR)xgerd_k$(TSUFFIX).$(SUFFIX)  $(KDIR)xgerd_k$(TSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(XGERCKERNEL) $(XGERPARAM)
	$(CC) -c $(CFLAGS) -DXDOUBLE -DCONJ -DXCONJ $< -o $@
"""
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
