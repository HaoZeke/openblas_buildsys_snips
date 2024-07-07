import random
import os
import numpy as np
import pytest
from approvaltests.approvals import verify


@pytest.fixture(scope="module", autouse=True)
def set_random():
    sval = 128
    rng = np.random.default_rng(sval)
    np.random.seed(sval)
    os.environ["PYTHONHASHSEED"] = str(sval)
    random.seed(sval)
    return rng


# ggbmv - General Band Matrix-Vector Multiply
def test_sgbmv_n(set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float32)
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_sgbmv_t(set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float32)
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_dgbmv_n(set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float64)
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dgbmv_t(set_random):
    rng = set_random
    A = rng.random((4, 4)).astype(np.float64)
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


# sbmv - Symmetric Band Matrix-Vector Multiply
def test_ssbmv_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_ssbmv_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_dsbmv_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dsbmv_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


# spmv - Symmetric Packed Matrix-Vector Multiply
def test_sspmv_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_sspmv_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_dspmv_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dspmv_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


# spr - Symmetric Packed Rank-1 Update
def test_sspr_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    A += np.outer(x, x)
    verify(A)


def test_sspr_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    A += np.outer(x, x)
    verify(A)


def test_dspr_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    A += np.outer(x, x)
    verify(A)


def test_dspr_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    A += np.outer(x, x)
    verify(A)


# spr2 - Symmetric Packed Rank-2 Update
def test_sspr2_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    y = rng.random(4).astype(np.float32)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


def test_sspr2_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    y = rng.random(4).astype(np.float32)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


def test_dspr2_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    y = rng.random(4).astype(np.float64)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


def test_dspr2_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    y = rng.random(4).astype(np.float64)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


# syr - Symmetric Rank-1 Update
def test_ssyr_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    A += np.outer(x, x)
    verify(A)


def test_ssyr_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    A += np.outer(x, x)
    verify(A)


def test_dsyr_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    A += np.outer(x, x)
    verify(A)


def test_dsyr_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    A += np.outer(x, x)
    verify(A)


# syr2 - Symmetric Rank-2 Update
def test_ssyr2_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    y = rng.random(4).astype(np.float32)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


def test_ssyr2_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    y = rng.random(4).astype(np.float32)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


def test_dsyr2_U(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    y = rng.random(4).astype(np.float64)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


def test_dsyr2_L(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    y = rng.random(4).astype(np.float64)
    A += np.outer(x, y) + np.outer(y, x)
    verify(A)


# tbmv - Triangular Band Matrix-Vector Multiply
def test_stbmv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_stbmv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_stbmv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_stbmv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_dtbmv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtbmv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtbmv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtbmv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_stbmv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_stbmv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_stbmv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_stbmv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_dtbmv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtbmv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtbmv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtbmv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


# tbsv - Triangular Band Matrix-Vector Solve
def test_stbsv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_stbsv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stbsv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_stbsv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtbsv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtbsv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtbsv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtbsv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stbsv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stbsv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_stbsv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stbsv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtbsv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtbsv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtbsv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtbsv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


# tpmv - Triangular Packed Matrix-Vector Multiply
def test_stpmv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_stpmv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_stpmv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_stpmv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_dtpmv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtpmv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtpmv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtpmv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


# tpsv - Triangular Packed Matrix-Vector Solve
def test_stpsv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_stpsv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stpsv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_stpsv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtpsv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtpsv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtpsv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtpsv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stpsv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stpsv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_stpsv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_stpsv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtpsv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtpsv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtpsv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtpsv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


# trmv - Triangular Matrix-Vector Multiply
def test_strmv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_strmv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_strmv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_strmv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_dtrmv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtrmv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtrmv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtrmv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_strmv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_strmv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_strmv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A.T, x)
    verify(res)


def test_strmv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.dot(A, x)
    verify(res)


def test_dtrmv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtrmv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


def test_dtrmv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A.T, x)
    verify(res)


def test_dtrmv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.dot(A, x)
    verify(res)


# trsv - Triangular Matrix-Vector Solve
def test_strsv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_strsv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_strsv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_strsv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtrsv_NUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtrsv_NUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtrsv_NLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtrsv_NLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_strsv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_strsv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_strsv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_strsv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float32))
    x = rng.random(4).astype(np.float32)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtrsv_TUU(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtrsv_TUN(set_random):
    rng = set_random
    A = np.triu(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)


def test_dtrsv_TLU(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A.T, x)
    verify(res)


def test_dtrsv_TLN(set_random):
    rng = set_random
    A = np.tril(rng.random((4, 4)).astype(np.float64))
    x = rng.random(4).astype(np.float64)
    res = np.linalg.solve(A, x)
    verify(res)
