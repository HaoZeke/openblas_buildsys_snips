import random
import os
import numpy as np
import pytest
from approvaltests import verify
from approvaltests.namer import NamerFactory

@pytest.fixture(autouse=True)
def set_random():
    sval = 128
    rng = np.random.default_rng(sval)
    np.random.seed(sval)
    os.environ["PYTHONHASHSEED"] = str(sval)
    random.seed(sval)
    return rng

blas_symbols = {
    "sgemm": lambda A, B, C: np.dot(A, B) + C,
    "dgemm": lambda A, B, C: np.dot(A, B) + C,
    "strmm": lambda A, B: np.dot(A, B),
    "dtrmm": lambda A, B: np.dot(A, B),
    "strsm": lambda A, B: np.linalg.solve(A, B),
    "dtrsm": lambda A, B: np.linalg.solve(A, B),
    "ssymm": lambda A, B, C: np.dot(A, B) + C,
    "dsymm": lambda A, B, C: np.dot(A, B) + C,
    "ssyrk": lambda A: np.dot(A, A.T),
    "dsyrk": lambda A: np.dot(A, A.T),
    "ssyr2k": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "dsyr2k": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "ssyrk_kernel": lambda A: np.dot(A, A.T),
    "dsyrk_kernel": lambda A: np.dot(A, A.T),
    "ssyr2k_kernel": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "dsyr2k_kernel": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
}

@pytest.mark.parametrize("symbol,trans_a,trans_b", [
    (symbol, trans_a, trans_b)
    for symbol in ["sgemm", "dgemm", "ssymm", "dsymm"]
    for trans_a in ["n", "t"]
    for trans_b in ["n", "t"]
])
def test_gemm(symbol, trans_a, trans_b, set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    if trans_a == "t":
        A = A.T
    B = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    if trans_b == "t":
        B = B.T
    C = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    res = blas_symbols[symbol](A, B, C)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{trans_a}{trans_b}"))

@pytest.mark.parametrize("symbol,side,uplo,diag,trans_a", [
    (symbol, side, uplo, diag, trans_a)
    for symbol in ["strmm", "dtrmm", "strsm", "dtrsm"]
    for side in ["L", "R"]
    for uplo in ["N", "T"]
    for diag in ["U", "N"]
    for trans_a in ["n", "t"]
])
def test_trmm_trsm(symbol, side, uplo, diag, trans_a, set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    if trans_a == "t":
        A = A.T
    if uplo == "U":
        A = np.triu(A)
    else:
        A = np.tril(A)
    if diag == "U":
        np.fill_diagonal(A, 1.0)
    B = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    res = blas_symbols[symbol](A, B)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{side}{uplo}{diag}{trans_a}"))

@pytest.mark.parametrize("symbol,uplo,trans", [
    (symbol, uplo, trans)
    for symbol in ["ssyrk", "dsyrk", "ssyrk_kernel", "dsyrk_kernel"]
    for uplo in ["U", "L"]
    for trans in ["n", "t"]
])
def test_syrk(symbol, uplo, trans, set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    if trans == "t":
        A = A.T
    res = blas_symbols[symbol](A)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{uplo}{trans}"))

@pytest.mark.parametrize("symbol,uplo,trans", [
    (symbol, uplo, trans)
    for symbol in ["ssyr2k", "dsyr2k", "ssyr2k_kernel", "dsyr2k_kernel"]
    for uplo in ["U", "L"]
    for trans in ["n", "t"]
])
def test_syr2k(symbol, uplo, trans, set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    B = rng.random((4, 4)).astype(np.float32 if "s" in symbol else np.float64)
    if trans == "t":
        A = A.T
        B = B.T
    res = blas_symbols[symbol](A, B)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{uplo}{trans}"))
