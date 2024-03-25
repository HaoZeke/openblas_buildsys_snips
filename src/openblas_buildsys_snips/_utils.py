import itertools


def pair_kdir_lines(lines):
    """
    Pair each line containing `$(KDIR)` with its immediately following line.

    This generator function iterates over a sequence of lines. For each line
    that contains the `$(KDIR)` marker, it pairs this line with the next line in
    the sequence. Both lines are stripped of leading and trailing whitespace
    before being concatenated and yielded.

    Parameters
    ----------
    **lines** : iterable of str

        An iterable sequence of lines (strings) to be processed. This can be a
        list of strings, a file object, or any iterable that yields strings
        representing individual lines.

    Yields
    ------
    **str**

        Paired lines concatenated into a single string. Only lines containing
        `$(KDIR)` are processed and paired with their subsequent line. Each
        yielded string is a concatenation of a `$(KDIR)` line and its following
        line, separated by a space.

    Examples
    --------
    ```
    >>> lines = [
    ... "$(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL)",
    ... "$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@",
    ... "$(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL)",
    ... "$(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@"
    ... ]
    >>> paired_lines = list(pair_kdir_lines(lines))
    >>> for pline in paired_lines:
    ...     print(pline)
    $(KDIR)srot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)srot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(SROTKERNEL) $(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -UDOUBLE  $< -o $@
    $(KDIR)drot_k$(TSUFFIX).$(SUFFIX)  $(KDIR)drot_k$(TPSUFFIX).$(PSUFFIX)  : $(KERNELDIR)/$(DROTKERNEL) $(CC) -c $(CFLAGS) $(FMAFLAG) -UCOMPLEX -UCOMPLEX -DDOUBLE  $< -o $@
    ```
    """
    it1, it2 = itertools.tee(lines)
    next(it2, None)  # Advance the lookahead iterator

    for line1, line2 in zip(it1, it2):
        if "$(KDIR)" in line1:
            yield f"{line1.strip()} {line2.strip()}"
