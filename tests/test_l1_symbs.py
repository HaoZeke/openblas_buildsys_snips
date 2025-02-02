import random
import os
import numpy as np
import pytest
from approvaltests.approvals import verify


# Dot product functions
def test_sdot_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    res = np.dot(x, y)
    verify(res)


def test_ddot_k(set_random):
    x = set_random.random(4).astype(np.float64)
    y = set_random.random(4).astype(np.float64)
    res = np.dot(x, y)
    verify(res)


def test_dsdot_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    res = np.dot(x, y).astype(np.float64)
    verify(res)


# Bfloat16 dot product (simulate with float16)
def test_sbdot_k(set_random):
    x = set_random.random(4).astype(np.float16)
    y = set_random.random(4).astype(np.float16)
    res = np.dot(x, y).astype(np.float32)
    verify(res)


# Conversion functions
def test_sbstobf16_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = x.astype(np.float16)
    verify(y)


def test_sbdtobf16_k(set_random):
    x = set_random.random(4).astype(np.float64)
    y = x.astype(np.float16)
    verify(y)


def test_sbf16tos_k(set_random):
    x = set_random.random(4).astype(np.float16)
    y = x.astype(np.float32)
    verify(y)


def test_dbf16tod_k(set_random):
    x = set_random.random(4).astype(np.float16)
    y = x.astype(np.float64)
    verify(y)


# Complex dot product functions
def test_cdotc_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    y = set_random.random(4).astype(np.complex64)
    res = np.vdot(x, y)
    verify(res)


def test_cdotu_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    y = set_random.random(4).astype(np.complex64)
    res = np.dot(x, y)
    verify(res)


def test_zdotc_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    y = set_random.random(4).astype(np.complex128)
    res = np.vdot(x, y)
    verify(res)


def test_zdotu_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    y = set_random.random(4).astype(np.complex128)
    res = np.dot(x, y)
    verify(res)


# AXPY operations
def test_saxpy_k(set_random):
    alpha = 1.5
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    res = alpha * x + y
    verify(res)


def test_daxpy_k(set_random):
    alpha = 1.5
    x = set_random.random(4).astype(np.float64)
    y = set_random.random(4).astype(np.float64)
    res = alpha * x + y
    verify(res)


# Complex AXPY operations
def test_caxpy_k(set_random):
    alpha = 1.5 + 0.5j
    x = set_random.random(4).astype(np.complex64)
    y = set_random.random(4).astype(np.complex64)
    res = alpha * x + y
    verify(res)


def test_zaxpy_k(set_random):
    alpha = 1.5 + 0.5j
    x = set_random.random(4).astype(np.complex128)
    y = set_random.random(4).astype(np.complex128)
    res = alpha * x + y
    verify(res)


# Copy operations
def test_scopy_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = np.empty_like(x)
    np.copyto(y, x)
    verify(y)


def test_dcopy_k(set_random):
    x = set_random.random(4).astype(np.float64)
    y = np.empty_like(x)
    np.copyto(y, x)
    verify(y)


def test_ccopy_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    y = np.empty_like(x)
    np.copyto(y, x)
    verify(y)


def test_zcopy_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    y = np.empty_like(x)
    np.copyto(y, x)
    verify(y)


# Swap operations
def test_sswap_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    x, y = y, x
    verify((x, y))


def test_dswap_k(set_random):
    x = set_random.random(4).astype(np.float64)
    y = set_random.random(4).astype(np.float64)
    x, y = y, x
    verify((x, y))


def test_cswap_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    y = set_random.random(4).astype(np.complex64)
    x, y = y, x
    verify((x, y))


def test_zswap_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    y = set_random.random(4).astype(np.complex128)
    x, y = y, x
    verify((x, y))


# ASUM operations
def test_sasum_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.sum(np.abs(x))
    verify(res)


def test_dasum_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.sum(np.abs(x))
    verify(res)


def test_casum_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.sum(np.abs(x))
    verify(res)


def test_zasum_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.sum(np.abs(x))
    verify(res)


# SUM operations
def test_ssum_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.sum(x)
    verify(res)


def test_dsum_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.sum(x)
    verify(res)


def test_csum_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.sum(x)
    verify(res)


def test_zsum_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.sum(x)
    verify(res)


# AMAX operations
def test_samax_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.amax(x)
    verify(res)


def test_damax_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.amax(x)
    verify(res)


def test_camax_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.amax(x)
    verify(res)


def test_zamax_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.amax(x)
    verify(res)


# AMIN operations
def test_samin_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.amin(x)
    verify(res)


def test_damin_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.amin(x)
    verify(res)


def test_camin_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.amin(x)
    verify(res)


def test_zamin_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.amin(x)
    verify(res)


# IAMAX operations
def test_isamax_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.argmax(x)
    verify(res)


def test_idamax_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.argmax(x)
    verify(res)


def test_icamax_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.argmax(np.abs(x))
    verify(res)


def test_izamax_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.argmax(np.abs(x))
    verify(res)


# IAMIN operations
def test_isamin_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.argmin(x)
    verify(res)


def test_idamin_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.argmin(x)
    verify(res)


def test_icamin_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.argmin(np.abs(x))
    verify(res)


def test_izamin_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.argmin(np.abs(x))
    verify(res)


# SCAL operations
def test_sscal_k(set_random):
    x = set_random.random(4).astype(np.float32)
    alpha = 1.5
    res = alpha * x
    verify(res)


def test_dscal_k(set_random):
    x = set_random.random(4).astype(np.float64)
    alpha = 1.5
    res = alpha * x
    verify(res)


def test_cscal_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    alpha = 1.5 + 0.5j
    res = alpha * x
    verify(res)


def test_zscal_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    alpha = 1.5 + 0.5j
    res = alpha * x
    verify(res)


# NRM2 operations
def test_snrm2_k(set_random):
    x = set_random.random(4).astype(np.float32)
    res = np.linalg.norm(x)
    verify(res)


def test_dnrm2_k(set_random):
    x = set_random.random(4).astype(np.float64)
    res = np.linalg.norm(x)
    verify(res)


def test_cnrm2_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    res = np.linalg.norm(x)
    verify(res)


def test_znrm2_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    res = np.linalg.norm(x)
    verify(res)


# ROT operations
def test_srot_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    c = 0.5
    s = 0.5
    res_x = c * x + s * y
    res_y = c * y - s * x
    verify((res_x, res_y))


def test_drot_k(set_random):
    x = set_random.random(4).astype(np.float64)
    y = set_random.random(4).astype(np.float64)
    c = 0.5
    s = 0.5
    res_x = c * x + s * y
    res_y = c * y - s * x
    verify((res_x, res_y))


def test_csrot_k(set_random):
    x = set_random.random(4).astype(np.complex64)
    y = set_random.random(4).astype(np.complex64)
    c = 0.5
    s = 0.5
    res_x = c * x + s * y
    res_y = c * y - s * x
    verify((res_x, res_y))


def test_zdrot_k(set_random):
    x = set_random.random(4).astype(np.complex128)
    y = set_random.random(4).astype(np.complex128)
    c = 0.5
    s = 0.5
    res_x = c * x + s * y
    res_y = c * y - s * x
    verify((res_x, res_y))


# ROTG operations
def test_srotg_k(set_random):
    a = set_random.random(1).astype(np.float32)
    b = set_random.random(1).astype(np.float32)
    c = np.zeros(1, dtype=np.float32)
    s = np.zeros(1, dtype=np.float32)
    res_a, res_b, res_c, res_s = (
        np.linalg.norm(a),
        0,
        a / np.linalg.norm(a),
        b / np.linalg.norm(a),
    )
    verify((res_a, res_b, res_c, res_s))


def test_drotg_k(set_random):
    a = set_random.random(1).astype(np.float64)
    b = set_random.random(1).astype(np.float64)
    c = np.zeros(1, dtype=np.float64)
    s = np.zeros(1, dtype=np.float64)
    res_a, res_b, res_c, res_s = (
        np.linalg.norm(a),
        0,
        a / np.linalg.norm(a),
        b / np.linalg.norm(a),
    )
    verify((res_a, res_b, res_c, res_s))


def test_csrotg_k(set_random):
    a = set_random.random(1).astype(np.complex64)
    b = set_random.random(1).astype(np.complex64)
    c = np.zeros(1, dtype=np.float32)
    s = np.zeros(1, dtype=np.float32)
    res_a, res_b, res_c, res_s = (
        np.linalg.norm(a),
        0,
        a / np.linalg.norm(a),
        b / np.linalg.norm(a),
    )
    verify((res_a, res_b, res_c, res_s))


def test_zdrotg_k(set_random):
    a = set_random.random(1).astype(np.complex128)
    b = set_random.random(1).astype(np.complex128)
    c = np.zeros(1, dtype=np.float64)
    s = np.zeros(1, dtype=np.float64)
    res_a, res_b, res_c, res_s = (
        np.linalg.norm(a),
        0,
        a / np.linalg.norm(a),
        b / np.linalg.norm(a),
    )
    verify((res_a, res_b, res_c, res_s))


# ROTMG operations
def test_srotmg_k(set_random):
    d1 = set_random.random(1).astype(np.float32)
    d2 = set_random.random(1).astype(np.float32)
    x1 = set_random.random(1).astype(np.float32)
    y1 = set_random.random(1).astype(np.float32)
    param = np.zeros(5, dtype=np.float32)
    verify((d1, d2, x1, y1, param))


def test_drotmg_k(set_random):
    d1 = set_random.random(1).astype(np.float64)
    d2 = set_random.random(1).astype(np.float64)
    x1 = set_random.random(1).astype(np.float64)
    y1 = set_random.random(1).astype(np.float64)
    param = np.zeros(5, dtype=np.float64)
    verify((d1, d2, x1, y1, param))


# ROTM operations
def test_srotm_k(set_random):
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    param = np.zeros(5, dtype=np.float32)
    res_x = param[0] * x + param[1] * y
    res_y = param[2] * x + param[3] * y
    verify((res_x, res_y))


def test_drotm_k(set_random):
    x = set_random.random(4).astype(np.float64)
    y = set_random.random(4).astype(np.float64)
    param = np.zeros(5, dtype=np.float64)
    res_x = param[0] * x + param[1] * y
    res_y = param[2] * x + param[3] * y
    verify((res_x, res_y))


# AXPBY operations
def test_saxpby_k(set_random):
    alpha = 1.5
    beta = 0.5
    x = set_random.random(4).astype(np.float32)
    y = set_random.random(4).astype(np.float32)
    res = alpha * x + beta * y
    verify(res)


def test_daxpby_k(set_random):
    alpha = 1.5
    beta = 0.5
    x = set_random.random(4).astype(np.float64)
    y = set_random.random(4).astype(np.float64)
    res = alpha * x + beta * y
    verify(res)


def test_caxpby_k(set_random):
    alpha = 1.5 + 0.5j
    beta = 0.5 + 0.5j
    x = set_random.random(4).astype(np.complex64)
    y = set_random.random(4).astype(np.complex64)
    res = alpha * x + beta * y
    verify(res)


def test_zaxpby_k(set_random):
    alpha = 1.5 + 0.5j
    beta = 0.5 + 0.5j
    x = set_random.random(4).astype(np.complex128)
    y = set_random.random(4).astype(np.complex128)
    res = alpha * x + beta * y
    verify(res)
