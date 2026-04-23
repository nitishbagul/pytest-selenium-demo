# pytest-selenium-demo

Test automation framework demonstrating pytest + Selenium against saucedemo.com.

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
# All tests
pytest

# Smoke only
pytest -m smoke

# Regression only
pytest -m regression

# Parallel (4 workers)
pytest -n 4

# Headless (good for CI)
pytest --headless

# Firefox instead of Chrome
pytest --browser=firefox

# With retries for flaky tests
pytest --reruns 2

# A specific test file
pytest tests/test_login.py

# A specific test, by name
pytest tests/test_login.py::test_valid_user_can_login

# Override URL via env var
BASE_URL=https://staging.example.com pytest

# Generate Allure results (then `allure serve allure-results` to view)
pytest --alluredir=allure-results
```

## Reports

- HTML report: `reports/report.html` (opens in any browser)
- Screenshots of failures: `screenshots/`
- Allure: run `allure serve allure-results` after a test run
