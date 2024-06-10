from dataclasses import dataclass
import numpy as np
import json
import gzip
from typing import List
from numpy.testing import assert_almost_equal


@dataclass
class MatrixOperationTest:
    label: str
    inputs: List[np.ndarray]
    expression: str
    expected_output: np.ndarray

    def to_dict(self):
        return {
            "label": self.label,
            "inputs": [_inp.tolist() for _inp in self.inputs],
            "expression": self.expression,
            "expected_output": self.expected_output.tolist(),
        }

    @staticmethod
    def from_dict(data):
        inputs = [np.array(_inp) for _inp in data["inputs"]]
        expected_output = np.array(data["expected_output"])
        return MatrixOperationTest(
            label=data["label"],
            inputs=inputs,
            expression=data["expression"],
            expected_output=expected_output,
        )


def run_test(test: MatrixOperationTest):
    local_vars = {f"input{i}": _inp for i, _inp in enumerate(test.inputs)}
    local_vars["np"] = np
    local_vars["assert_almost_equal"] = assert_almost_equal
    result = eval(test.expression, {}, local_vars)
    assert_almost_equal(
        result,
        test.expected_output,
        decimal=7,
        err_msg=f"Test failed for label: {test.label}, expression: {test.expression}",
        verbose=True,
    )


def generate_tests() -> List[MatrixOperationTest]:
    np.random.seed(128)
    C_float = np.random.rand(4, 4).astype(np.float32)

    tests = [
        MatrixOperationTest(
            label="ssyrk_lt",
            inputs=[C_float, C_float],
            expression="np.dot(input0, input1.T)",
            expected_output=np.dot(C_float, C_float.T),
        )
    ]

    return tests


def save_tests(tests: List[MatrixOperationTest], filename: str):
    data = [test.to_dict() for test in tests]
    with gzip.open(filename, "wt") as f:
        json.dump(data, f, indent=4)


def load_tests(filename: str) -> List[MatrixOperationTest]:
    with gzip.open(filename, "rt") as f:
        data = json.load(f)
        return [MatrixOperationTest.from_dict(item) for item in data]
