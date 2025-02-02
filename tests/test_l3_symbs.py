import numpy as np
import pytest
from approvaltests import verify
from approvaltests.namer import NamerFactory


blas_l3_symbols = {
    "sgemm": lambda A, B, C: np.dot(A, B) + C,
    "dgemm": lambda A, B, C: np.dot(A, B) + C,
    "cgemm": lambda A, B, C: np.dot(A, B) + C,
    "zgemm": lambda A, B, C: np.dot(A, B) + C,
    "strmm": lambda A, B: np.dot(A, B),
    "dtrmm": lambda A, B: np.dot(A, B),
    "ctrmm": lambda A, B: np.dot(A, B),
    "ztrmm": lambda A, B: np.dot(A, B),
    "strsm": lambda A, B: np.linalg.solve(A, B),
    "dtrsm": lambda A, B: np.linalg.solve(A, B),
    "ctrsm": lambda A, B: np.linalg.solve(A, B),
    "ztrsm": lambda A, B: np.linalg.solve(A, B),
    "ssymm": lambda A, B, C: np.dot(A, B) + C,
    "dsymm": lambda A, B, C: np.dot(A, B) + C,
    "csymm": lambda A, B, C: np.dot(A, B) + C,
    "zsymm": lambda A, B, C: np.dot(A, B) + C,
    "chemm": lambda A, B, C: np.dot(A, B) + C,
    "zhemm": lambda A, B, C: np.dot(A, B) + C,
    "ssyrk": lambda A: np.dot(A, A.T),
    "dsyrk": lambda A: np.dot(A, A.T),
    "csyrk": lambda A: np.dot(A, A.T.conj()),
    "zsyrk": lambda A: np.dot(A, A.T.conj()),
    "cherk": lambda A: np.dot(A, A.T.conj()),
    "zherk": lambda A: np.dot(A, A.T.conj()),
    "ssyr2k": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "dsyr2k": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "csyr2k": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "zsyr2k": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "cher2k": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "zher2k": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "ssyrk_kernel": lambda A: np.dot(A, A.T),
    "dsyrk_kernel": lambda A: np.dot(A, A.T),
    "csyrk_kernel": lambda A: np.dot(A, A.T.conj()),
    "zsyrk_kernel": lambda A: np.dot(A, A.T.conj()),
    "cherk_kernel": lambda A: np.dot(A, A.T.conj()),
    "zherk_kernel": lambda A: np.dot(A, A.T.conj()),
    "ssyr2k_kernel": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "dsyr2k_kernel": lambda A, B: np.dot(A, B.T) + np.dot(B, A.T),
    "csyr2k_kernel": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "zsyr2k_kernel": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "cher2k_kernel": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
    "zher2k_kernel": lambda A, B: np.dot(A, B.T.conj()) + np.dot(B, A.T.conj()),
}


@pytest.mark.parametrize(
    "symbol,trans_a,trans_b",
    [
        (symbol, trans_a, trans_b)
        for symbol in [
            "sgemm",
            "dgemm",
            "cgemm",
            "zgemm",
            "ssymm",
            "dsymm",
            "csymm",
            "zsymm",
            "chemm",
            "zhemm",
        ]
        for trans_a in ["n", "t", "c"]
        if not (symbol.startswith("s") or symbol.startswith("d")) or trans_a != "c"
        for trans_b in ["n", "t", "c"]
        if not (symbol.startswith("s") or symbol.startswith("d")) or trans_b != "c"
    ],
)
def test_gemm(symbol, trans_a, trans_b, set_random):
    rng = set_random
    dtype = (
        np.float32
        if symbol.startswith("s")
        else (
            np.float64
            if symbol.startswith("d")
            else np.complex64 if symbol.startswith("c") else np.complex128
        )
    )
    A = rng.random((4, 4)).astype(dtype)
    if trans_a == "t":
        A = A.T
    elif trans_a == "c":
        A = A.T.conj()
    B = rng.random((4, 4)).astype(dtype)
    if trans_b == "t":
        B = B.T
    elif trans_b == "c":
        B = B.T.conj()
    C = rng.random((4, 4)).astype(dtype)
    res = blas_l3_symbols[symbol](A, B, C)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{trans_a}{trans_b}"))


@pytest.mark.parametrize(
    "symbol,side,uplo,diag,trans_a",
    [
        (symbol, side, uplo, diag, trans_a)
        for symbol in [
            "strmm",
            "dtrmm",
            "ctrmm",
            "ztrmm",
            "strsm",
            "dtrsm",
            "ctrsm",
            "ztrsm",
        ]
        for side in ["L", "R"]
        for uplo in ["U", "L"]
        for diag in ["U", "N"]
        for trans_a in ["n", "t", "c"]
        if not (symbol.startswith("s") or symbol.startswith("d")) or trans_a != "c"
    ],
)
def test_trmm_trsm(symbol, side, uplo, diag, trans_a, set_random):
    rng = set_random
    dtype = (
        np.float32
        if symbol.startswith("s")
        else (
            np.float64
            if symbol.startswith("d")
            else np.complex64 if symbol.startswith("c") else np.complex128
        )
    )
    A = rng.random((4, 4)).astype(dtype)
    if trans_a == "t":
        A = A.T
    elif trans_a == "c":
        A = A.T.conj()
    if uplo == "U":
        A = np.triu(A)
    else:
        A = np.tril(A)
    if diag == "U":
        np.fill_diagonal(A, 1.0)
    B = rng.random((4, 4)).astype(dtype)
    res = blas_l3_symbols[symbol](A, B)
    verify(
        res,
        options=NamerFactory.with_parameters(f"{symbol}_{side}{uplo}{diag}{trans_a}"),
    )


@pytest.mark.parametrize(
    "symbol,uplo,trans",
    [
        (symbol, uplo, trans)
        for symbol in [
            "ssyrk",
            "dsyrk",
            "csyrk",
            "zsyrk",
            "cherk",
            "zherk",
            "ssyrk_kernel",
            "dsyrk_kernel",
            "csyrk_kernel",
            "zsyrk_kernel",
            "cherk_kernel",
            "zherk_kernel",
        ]
        for uplo in ["U", "L"]
        for trans in ["n", "t", "c"]
        if not (symbol.startswith("s") or symbol.startswith("d")) or trans != "c"
    ],
)
def test_syrk(symbol, uplo, trans, set_random):
    rng = set_random
    dtype = (
        np.float32
        if symbol.startswith("s")
        else (
            np.float64
            if symbol.startswith("d")
            else np.complex64 if symbol.startswith("c") else np.complex128
        )
    )
    A = rng.random((4, 4)).astype(dtype)
    if trans == "t":
        A = A.T
    elif trans == "c":
        A = A.T.conj()
    res = blas_l3_symbols[symbol](A)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{uplo}{trans}"))


@pytest.mark.parametrize(
    "symbol,uplo,trans",
    [
        (symbol, uplo, trans)
        for symbol in [
            "ssyr2k",
            "dsyr2k",
            "csyr2k",
            "zsyr2k",
            "cher2k",
            "zher2k",
            "ssyr2k_kernel",
            "dsyr2k_kernel",
            "csyr2k_kernel",
            "zsyr2k_kernel",
            "cher2k_kernel",
            "zher2k_kernel",
        ]
        for uplo in ["U", "L"]
        for trans in ["n", "t", "c"]
        if not (symbol.startswith("s") or symbol.startswith("d")) or trans != "c"
    ],
)
def test_syr2k(symbol, uplo, trans, set_random):
    rng = set_random
    dtype = (
        np.float32
        if symbol.startswith("s")
        else (
            np.float64
            if symbol.startswith("d")
            else np.complex64 if symbol.startswith("c") else np.complex128
        )
    )
    A = rng.random((4, 4)).astype(dtype)
    B = rng.random((4, 4)).astype(dtype)
    if trans == "t":
        A = A.T
        B = B.T
    elif trans == "c":
        A = A.T.conj()
        B = B.T.conj()
    res = blas_l3_symbols[symbol](A, B)
    verify(res, options=NamerFactory.with_parameters(f"{symbol}_{uplo}{trans}"))
