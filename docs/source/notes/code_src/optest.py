import numpy as np
from numpy.testing import assert_almost_equal
import argparse
import json
from dataclasses import dataclass, asdict


@dataclass
class ExpectedOutputs:
    matrix_matrix: np.ndarray
    matrix_vector: np.ndarray
    vector_matrix: np.ndarray
    vector_vector: float

    def to_dict(self):
        return {
            "matrix_matrix": self.matrix_matrix.tolist(),
            "matrix_vector": self.matrix_vector.tolist(),
            "vector_matrix": self.vector_matrix.tolist(),
            "vector_vector": self.vector_vector,
        }

    @staticmethod
    def from_dict(data):
        return ExpectedOutputs(
            matrix_matrix=np.array(data["matrix_matrix"]),
            matrix_vector=np.array(data["matrix_vector"]),
            vector_matrix=np.array(data["vector_matrix"]),
            vector_vector=data["vector_vector"],
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


def generate_expected_outputs():
    np.random.seed(128)
    N = 7

    # Generate matrices and vectors
    A = np.random.rand(4, 2)
    B = A.T
    v = np.random.rand(2)
    v1 = np.random.rand(4)
    v2 = np.random.rand(4)

    # Expected results using NumPy
    expected_outputs = ExpectedOutputs(
        matrix_matrix=np.dot(A, B),
        matrix_vector=np.dot(A, v),
        vector_matrix=np.dot(v1, A),
        vector_vector=np.dot(v1, v2),
    )

    return expected_outputs


def main():
    parser = argparse.ArgumentParser(
        description="Test OpenBLAS operations or generate expected outputs."
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate and save expected outputs to JSON",
    )
    parser.add_argument(
        "--test", type=str, help="Run tests with expected outputs from JSON file"
    )
    args = parser.parse_args()

    if args.generate:
        expected_outputs = generate_expected_outputs()
        with open("expected_outputs.json", "w") as f:
            json.dump(expected_outputs.to_dict(), f, indent=4)
        print("Expected outputs saved to expected_outputs.json")
    elif args.test:
        with open(args.test, "r") as f:
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
