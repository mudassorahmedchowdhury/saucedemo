# Sauce Demo Selenium Pytest Framework

This project implements a Page Object Model (POM) Selenium framework using Pytest to validate key user flows on `https://www.saucedemo.com/`.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r sauce-automation-test/requirements.txt`.

## Run Tests

- Basic: `pytest sauce-automation-test/tests -v`
- Headless: `pytest sauce-automation-test/tests -v --headless`
- HTML report: `pytest sauce-automation-test/tests -v --headless --html=sauce-automation-test/reports/report.html --self-contained-html`

## Configuration

- Defaults are in `sauce-automation-test/config.json`.
- Override via CLI: `--base-url`, `--browser`, `--headless`.

## Scenarios Covered

- Login success and invalid password
- Add to cart and checkout
- Product sorting low to high with screenshot
- Access restriction without login
- Screenshot captured on test failure and attached in HTML report

## Credentials

- Username: `standard_user`
- Password: `secret_sauce`