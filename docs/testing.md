# Testing

Tests are written in pytest-style in the `tests` folder. The unit tests are isolated from external state.

```shell
tests/run_tests.sh 
```

This will run the tests for the module sr_cli and show a coverage report to the console:

```shell
uv run pytest tests --cov=sr_cli --cov-report term
```

This will display the test results and code coverage for each tested module:

```console
============================== test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/angel/workspace/python/swiss_re_assignment
configfile: pyproject.toml
plugins: mock-3.15.1, cov-7.1.0
collected 35 items

tests/test_process.py .................                                   [ 48%]
tests/test_utils.py ..................                                    [100%]

================================ tests coverage =================================
_______________ coverage: platform darwin, python 3.14.4-final-0 ________________

Name                 Stmts   Miss  Cover
----------------------------------------
sr_cli/__init__.py       0      0   100%
sr_cli/main.py          26     26     0%
sr_cli/process.py       65      0   100%
sr_cli/utils.py         23      0   100%
----------------------------------------
TOTAL                  114     26    77%
```
