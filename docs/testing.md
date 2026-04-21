# Testing

Tests are written in pytest-style in the `tests` folder. The unit tests are isolated from external state.

```shell
tests/run_tests.sh
```

This script contains the next command and will run the tests for the module sr_cli and show a coverage report to the console:

```shell
uv run pytest tests --cov=sr_cli --cov-report term
```

This will display the test results and code coverage for each tested module:

```console
$ uv run pytest --cov=sr_cli/ --cov-report term
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/angel/workspace/python/swiss_re_assignment
configfile: pyproject.toml
plugins: mock-3.15.1, cov-7.1.0
collected 45 items

tests/test_input.py ............                                         [ 26%]
tests/test_output.py ..........                                          [ 48%]
tests/test_process.py .............                                      [ 77%]
tests/test_statistics.py ....                                            [ 86%]
tests/test_utils.py ......                                               [100%]

================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.13-final-0 _______________

Name                   Stmts   Miss  Cover
------------------------------------------
sr_cli/__init__.py         0      0   100%
sr_cli/input.py           39      0   100%
sr_cli/main.py            27     27     0%
sr_cli/output.py          57      6    89%
sr_cli/process.py         39      0   100%
sr_cli/statistics.py      24      0   100%
sr_cli/utils.py            8      0   100%
------------------------------------------
TOTAL                    194     33    83%
============================== 45 passed in 0.12s ==============================
```

## Automatic check on development

A GitHub CI job has been configured to run on a pull_request event. This will use Pytest to run the tests. The configuration for this job in the `.github` folder. The results can be found [in the Actions folder](https://github.com/angelgcuartero/swiss_re_assignment/actions).
