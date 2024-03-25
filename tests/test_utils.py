from openblas_buildsys_snips import _utils


def test_basic_netlib():
    lines = """
$(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL)
	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@

$(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL)
	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@
"""
    _output = _utils.pair_kdir_lines(lines.split("\n"))
    expect = [
        "$(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL) $(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@",
        "$(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL) $(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@",
    ]
    assert [x for x in _output] == expect
