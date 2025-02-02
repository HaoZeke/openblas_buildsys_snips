# Approval Tests

To facilitate easier testing of `openblas` builds, we use approval tests, a.k.a.
golden-master tests.

## Usage

```{code-block} bash
# First time
pytest -vvv  --approvaltests-use-reporter='PythonNativeReporter'
# Move things as per the report
# Or check results with meld
pytest -vvv  --approvaltests-add-reporter='meld' 
```

Often it is simpler to move everything together.

```{code-block} bash
export GITROOT=$(git rev-parse --show-toplevel) 
for file in ${GITROOT}/tests/approved_files/*.received.txt; do mv -f "$file" "${file/received.txt/approved.txt}"; done
```
