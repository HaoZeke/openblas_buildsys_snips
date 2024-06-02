import numpy as np
import json
import gzip
import argparse
from numpy.testing import assert_almost_equal
from dataclasses import dataclass

@dataclass
class ExpectedOutputs:
    matrix_matrix: np.ndarray
    matrix_vector: np.ndarray
    vector_matrix: np.ndarray
    vector_vector: float
    syrk_float_un: np.ndarray
    syrk_float_ut: np.ndarray
    syrk_float_ln: np.ndarray
    syrk_float_lt: np.ndarray
    syrk_double_un: np.ndarray
    syrk_double_ut: np.ndarray
    syrk_double_ln: np.ndarray
    syrk_double_lt: np.ndarray
    gemm_case: np.ndarray

    def to_dict(self):
        return {
            "matrix_matrix": self.matrix_matrix.tolist(),
            "matrix_vector": self.matrix_vector.tolist(),
            "vector_matrix": self.vector_matrix.tolist(),
            "vector_vector": self.vector_vector,
            "syrk_float_un": self.syrk_float_un.tolist(),
            "syrk_float_ut": self.syrk_float_ut.tolist(),
            "syrk_float_ln": self.syrk_float_ln.tolist(),
            "syrk_float_lt": self.syrk_float_lt.tolist(),
            "syrk_double_un": self.syrk_double_un.tolist(),
            "syrk_double_ut": self.syrk_double_ut.tolist(),
            "syrk_double_ln": self.syrk_double_ln.tolist(),
            "syrk_double_lt": self.syrk_double_lt.tolist(),
            "gemm_case": self.gemm_case.tolist(),
        }

    @staticmethod
    def from_dict(data):
        return ExpectedOutputs(
            matrix_matrix=np.array(data["matrix_matrix"]),
            matrix_vector=np.array(data["matrix_vector"]),
            vector_matrix=np.array(data["vector_matrix"]),
            vector_vector=data["vector_vector"],
            syrk_float_un=np.array(data["syrk_float_un"]),
            syrk_float_ut=np.array(data["syrk_float_ut"]),
            syrk_float_ln=np.array(data["syrk_float_ln"]),
            syrk_float_lt=np.array(data["syrk_float_lt"]),
            syrk_double_un=np.array(data["syrk_double_un"]),
            syrk_double_ut=np.array(data["syrk_double_ut"]),
            syrk_double_ln=np.array(data["syrk_double_ln"]),
            syrk_double_lt=np.array(data["syrk_double_lt"]),
            gemm_case=np.array(data["gemm_case"]),
        )

def test_dot_operations(expected_outputs):
    np.random.seed(128)
    N = 7

    # Generate matrices and vectors
    A = np.random.rand(4, 2)
    B = A.T
    v = np.random.rand(2)
    v1 = np.random.rand(4)
    v2 = np.random.rand(4)
    C_float = np.random.rand(4, 4).astype(np.float32)
    C_double = np.random.rand(4, 4).astype(np.float64)

    # Matrix-Matrix multiplication
    res = np.dot(A, B)
    tgt = expected_outputs.matrix_matrix
    assert_almost_equal(res, tgt, decimal=N)

    # Matrix-Vector multiplication
    res = np.dot(A, v)
    tgt = expected_outputs.matrix_vector
    assert_almost_equal(res, tgt, decimal=N)

    # Vector-Matrix multiplication
    res = np.dot(v1, A)
    tgt = expected_outputs.vector_matrix
    assert_almost_equal(res, tgt, decimal=N)

    # Vector-Vector multiplication (dot product)
    res = np.dot(v1, v2)
    tgt = expected_outputs.vector_vector
    assert_almost_equal(res, tgt, decimal=N)

    # SYRK float cases
    res = np.dot(C_float, C_float.T)
    tgt = expected_outputs.syrk_float_un
    assert_almost_equal(res, tgt, decimal=N, err_msg="syrk_float_un failed", verbose=True)

    res = np.dot(C_float.T, C_float)
    tgt = expected_outputs.syrk_float_ut
    assert_almost_equal(res, tgt, decimal=N)

    res = np.dot(C_float.T, C_float.T)
    tgt = expected_outputs.syrk_float_ln
    assert_almost_equal(res, tgt, decimal=N)

    res = np.dot(C_float, C_float)
    tgt = expected_outputs.syrk_float_lt
    assert_almost_equal(res, tgt, decimal=N)

    # SYRK double cases
    res = np.dot(C_double, C_double.T)
    tgt = expected_outputs.syrk_double_un
    assert_almost_equal(res, tgt, decimal=N)

    res = np.dot(C_double.T, C_double)
    tgt = expected_outputs.syrk_double_ut
    assert_almost_equal(res, tgt, decimal=N)

    res = np.dot(C_double.T, C_double.T)
    tgt = expected_outputs.syrk_double_ln
    assert_almost_equal(res, tgt, decimal=N)

    res = np.dot(C_double, C_double)
    tgt = expected_outputs.syrk_double_lt
    assert_almost_equal(res, tgt, decimal=N)

    # GEMM case
    res = np.dot(A, A.T)
    tgt = expected_outputs.gemm_case
    assert_almost_equal(res, tgt, decimal=N)

def generate_expected_outputs():
    np.random.seed(128)

    # Generate matrices and vectors
    A = np.random.rand(4, 2)
    B = A.T
    v = np.random.rand(2)
    v1 = np.random.rand(4)
    v2 = np.random.rand(4)
    C_float = np.random.rand(4, 4).astype(np.float32)
    C_double = np.random.rand(4, 4).astype(np.float64)

    # Expected results using NumPy
    expected_outputs = ExpectedOutputs(
        matrix_matrix=np.dot(A, B),
        matrix_vector=np.dot(A, v),
        vector_matrix=np.dot(v1, A),
        vector_vector=np.dot(v1, v2),
        syrk_float_un=np.dot(C_float, C_float.T),
        syrk_float_ut=np.dot(C_float.T, C_float),
        syrk_float_ln=np.dot(C_float.T, C_float.T),
        syrk_float_lt=np.dot(C_float, C_float),
        syrk_double_un=np.dot(C_double, C_double.T),
        syrk_double_ut=np.dot(C_double.T, C_double),
        syrk_double_ln=np.dot(C_double.T, C_double.T),
        syrk_double_lt=np.dot(C_double, C_double),
        gemm_case=np.dot(A, A.T),
    )

    return expected_outputs

def main():
    parser = argparse.ArgumentParser(
        description="Test OpenBLAS operations or generate expected outputs."
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate and save expected outputs to compressed JSON",
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Run tests with expected outputs from compressed JSON file",
    )
    args = parser.parse_args()

    if args.generate:
        expected_outputs = generate_expected_outputs()
        with gzip.open("expected_outputs.json.gz", "wt") as f:
            json.dump(expected_outputs.to_dict(), f, indent=4)
        print("Expected outputs saved to expected_outputs.json.gz")
    elif args.test:
        with gzip.open(args.test, "rt") as f:
            data = json.load(f)
            expected_outputs = ExpectedOutputs.from_dict(data)
        try:
            test_dot_operations(expected_outputs)
            print("All tests passed.")
        except AssertionError as e:
            print(f"Test failed: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
