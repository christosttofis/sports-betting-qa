# Sports Betting QA

Test plan, bug reports and an automation framework for the **Single Bet Placement** feature.

## Summary

- Bug reports: 17 bugs, 3 of them Critical. The main finding is that the backend doesn't enforce the key business rules ([Key findings](docs/BUG_REPORTS.md#key-findings)).
- Automation: 2 tests, API stake validation and the UI bet journey ([why these two](docs/STRATEGY.md)).

| Deliverable | Location |
|---|---|
| Test plan | [docs/TEST_PLAN.md](docs/TEST_PLAN.md) |
| Execution results & bug reports | [docs/BUG_REPORTS.md](docs/BUG_REPORTS.md) |
| Strategy & recommendations | [docs/STRATEGY.md](docs/STRATEGY.md) |
| Automation framework | `api/`, `pages/`, `utils/`, `tests/` |

## Stack

- Python 3.11+, Selenium WebDriver, pytest, requests (as required)
- [uv](https://docs.astral.sh/uv/) for dependency management: one command creates the venv and installs pinned versions from `uv.lock`
- Ruff for linting and formatting
- pytest-html for a self-contained HTML test report
- Chrome: the driver is downloaded automatically by Selenium Manager

## Project structure

```
api/
└── client.py              # API client (requests), adds x-user-id
pages/                     # Page Objects: BasePage, HomePage, BetSlip, ReceiptModal
utils/
├── config.py              # settings from env vars / .env
├── driver_factory.py      # Chrome WebDriver
└── money.py               # money parsing & payout calculation
tests/
├── conftest.py            # shared fixtures: settings, api, fresh_balance, upcoming_match
├── api/                   # API suite    (@pytest.mark.api)
└── ui/                    # UI E2E suite (@pytest.mark.ui, screenshot on failure)
```

## Setup

```bash
uv sync
cp .env.example .env      # then set USER_ID
```

## Running tests

```bash
uv run pytest             # all tests
uv run pytest -m api      # API suite only
uv run pytest -m ui       # UI suite only
uv run pytest --html=artifacts/report.html --self-contained-html   # with HTML report
```

Expected result: **5 passed, 2 xfailed**. The two xfails are known bugs (BUG-06 in the API test, BUG-01 and BUG-03 in the UI test, see [docs/BUG_REPORTS.md](docs/BUG_REPORTS.md)). Run `uv run pytest --runxfail` to see them fail.

Set `HEADLESS=true` in `.env` to run Chrome without a window. Screenshots of failed UI tests are saved to `artifacts/screenshots/`.

## CI

GitHub Actions ([.github/workflows/tests.yml](.github/workflows/tests.yml)) runs on every push, pull request, or manually:

- **lint**: `ruff check` and `ruff format --check`
- **tests**: API suite, then UI suite (headless Chrome). A results table is shown on the run page (job summary), and the HTML reports, logs and screenshots of failed UI tests are uploaded as the `test-reports` artifact.

The user ID is read from the `USER_ID` repository secret. Runs are queued, never parallel, because all tests share one account on the live app.

## Linting

```bash
uv run ruff check .
uv run ruff format .
```

## Use of AI

I used an AI assistant (Claude Code) during this task: to set up the framework, inspect the app's DOM for locators, run extra exploratory API checks, and help write and edit the docs. I reviewed every change, ran the tests, and made the final calls on what to test, the priorities and the severities.
