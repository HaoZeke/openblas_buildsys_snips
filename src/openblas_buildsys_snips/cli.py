import argparse
import numpy as np
from openblas_buildsys_snips._data import save_tests, load_tests, run_test, generate_tests

def main():
    parser = argparse.ArgumentParser(
        description="Test OpenBLAS operations or generate expected outputs."
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate and save test(s) to compressed JSON file"
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Run test(s) from compressed JSON file with the given label (e.g., ssyrk_lt) or 'all' to run all tests"
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="tests.json.gz",
        help="Specify the filename to save/load the tests (default: tests.json.gz)"
    )
    args = parser.parse_args()

    if args.generate:
        tests = generate_tests()
        save_tests(tests, args.filename)
        print(f"Tests saved to {args.filename}")
    elif args.test:
        tests = load_tests(args.filename)
        if args.test == "all":
            for test in tests:
                try:
                    run_test(test)
                    print(f"Test passed for label: {test.label}, expression: {test.expression}")
                except AssertionError as e:
                    print(f"Test failed for label: {test.label}: {e}")
        else:
            for test in tests:
                if test.label == args.test:
                    try:
                        run_test(test)
                        print(f"Test passed for label: {test.label}, expression: {test.expression}")
                    except AssertionError as e:
                        print(f"Test failed for label: {test.label}: {e}")
                    break
            else:
                print(f"No test found with label: {args.test}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
