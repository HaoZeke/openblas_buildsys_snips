from openblas_buildsys_snips import _utils


def test_pair_suffix():
    lines = """
$(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL)
	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@

$(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL)
	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@

sbstobf16.$(SUFFIX) sbstobf16.$(PSUFFIX) : tobf16.c
	$(CC) $(CFLAGS) -DSINGLE_PREC -UDOUBLE_PREC -c $< -o $(@F)
"""
    _output = _utils.pair_suffix_lines(lines.split("\n"))
    expect = [
        "$(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL)	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@",
        "$(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL)	$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@",
        "sbstobf16.$(SUFFIX) sbstobf16.$(PSUFFIX) : tobf16.c	$(CC) $(CFLAGS) -DSINGLE_PREC -UDOUBLE_PREC -c $< -o $(@F)"
    ]
    assert [x for x in _output] == expect
