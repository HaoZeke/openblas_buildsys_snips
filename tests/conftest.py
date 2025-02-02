import pytest
import numpy as np
import random
import os


@pytest.fixture(scope="session")
def set_printopts():
    np.set_printoptions(
        edgeitems=3,
        infstr="inf",
        linewidth=75,
        nanstr="nan",
        precision=4,
        suppress=False,
        threshold=1000,
        formatter=None,
    )


@pytest.fixture(scope="session", autouse=True)
def set_random(set_printopts):
    sval = 128
    rng = np.random.default_rng(sval)
    np.random.seed(sval)
    os.environ["PYTHONHASHSEED"] = str(sval)
    random.seed(sval)
    return rng
