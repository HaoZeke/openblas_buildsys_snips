import itertools


def pair_kdir_lines(lines):
    it1, it2 = itertools.tee(lines)
    next(it2, None)  # Advance the lookahead iterator

    for line1, line2 in zip(it1, it2):
        if "$(KDIR)" in line1:
            yield f"{line1.strip()} {line2.strip()}"
