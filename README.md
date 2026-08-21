# Test Automation User Guide
## Python + Pytest + Playwright Framework — Automation Exercise

**Purpose:** This guide is intended for a new engineer joining the project. By reading it from beginning to end, the engineer should understand how to set up the framework, where each type of change belongs, how test data and secrets are supplied, how Pytest and Playwright execute the tests, how evidence and traces are captured, how Allure results/reporting work, how Ruff is used, and how the same tests execute in GitHub Actions.

---

# 1. Framework at a Glance

The framework automates the **Automation Exercise** web application using:

- Python
- Pytest
- Playwright Python Sync API
- `pytest-playwright`
- Allure Pytest
- Ruff
- CSV test data
- YAML configuration
- Environment variables for secrets
- GitHub Actions for CI

The basic responsibility flow is:

```text
Test Requirement
      |
      v
tests/
      |
      v
pages/
      |
      v
Playwright
      |
      v
Browser
      |
      v
Automation Exercise
      |
      v
Playwright Assertions
      |
      v
Pytest Result
      |
      +----------------------+
      |                      |
      v                      v
Allure Results          Trace / Evidence
      |                      |
      +-----------+----------+
                  |
                  v
        artifacts/<timestamp>/
```

The most important separation is:

```text
Tests       = WHAT is being tested
Page Objects= HOW the application is operated
Test Data   = WITH WHAT data
Config      = WHERE / HOW the framework runs
Fixtures    = SETUP / reusable execution objects / cleanup
Utilities   = reusable technical support
Allure      = readable execution result and evidence
CI          = automated execution in GitHub
```

---

# 2. Expected Project Structure

Based on the current imports, configuration, and GitHub Actions workflow, the repository should be organized approximately as follows:

```text
playwright-python-training/
|
├── .github/
│   └── workflows/
│       └── tests.yml
|
├── config/
│   └── config_qa.yaml
|
├── pages/
│   ├── application.py
│   ├── home_page.py
│   ├── login_page.py
│   └── landing_page.py
|
├── test_data/
│   └── test_login.csv
|
├── tests/
│   └── test_login.py
|
├── utilities/
│   └── file_reader.py
|
├── artifacts/                 # Generated during execution
│   └── <YYYYMMDD_HHMMSS>/
│       ├── allure-results/
│       ├── traces/
│       └── allure-report/     # Created when static report is generated
|
├── conftest.py
├── pytest.ini
├── requirements.txt
├── ruff.toml
├── .env                       # Local only; do not commit
└── .gitignore
```

> The uploaded source set did not include `.gitignore`. Ensure `.env`, `.venv`, caches, and generated artifacts are excluded from Git.

Recommended entries:

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
.ruff_cache/
artifacts/
*.pyc
```

---

# 3. What Each File Does

| File / Folder | Purpose | Change this when... |
|---|---|---|
| `tests/test_login.py` | Defines login test scenarios, markers, Allure metadata/steps, parametrization, and expected flow | A login scenario, assertion, marker, or test flow changes |
| `pages/application.py` | Creates one application-level object containing the Page Objects used by tests | A new Page Object must be exposed to tests |
| `pages/home_page.py` | Home-page navigation and home-page-specific locators/actions | Home-page locator/navigation behavior changes |
| `pages/login_page.py` | Login-page locators, login action, and login-related validation methods | Login UI or login behavior changes |
| `pages/landing_page.py` | Logged-in landing-page locators/actions/validation | Post-login UI behavior changes |
| `test_data/test_login.csv` | Data-driven login inputs and expected results | Login datasets need to be added/changed |
| `config/config_qa.yaml` | QA environment URL, test-data path, and artifact settings | Environment URL or artifact capture behavior changes |
| `utilities/file_reader.py` | Reads YAML/CSV and resolves `${ENV_VARIABLE}` placeholders | Test data/config loading behavior changes |
| `conftest.py` | Shared Pytest fixtures, hooks, timestamped artifact location, screenshot evidence, tracing, Allure result location | Framework-level setup/cleanup/reporting behavior changes |
| `pytest.ini` | Pytest test discovery, default options, and marker registration | Markers or Pytest defaults change |
| `requirements.txt` | Python dependencies | A Python package must be added/removed |
| `ruff.toml` | Ruff lint/format rules | Code-quality rules change |
| `.github/workflows/tests.yml` | GitHub Actions CI setup and execution | CI trigger, Python version, browser, commands, secrets, or artifact upload changes |
| `.env` | Local environment variables and credentials | Local environment/secret values change; never commit it |
| `artifacts/` | Generated execution output | Normally never manually edited |

---

# 4. Where Should I Make a Change?

Use this quick decision table before modifying the framework.

| Requirement | Correct place |
|---|---|
| Change QA URL | `config/config_qa.yaml` |
| Add UAT environment | Create `config/config_uat.yaml`, then run with `ENV=uat` |
| Change valid login email/password locally | `.env` |
| Change valid login email/password in CI | GitHub repository secrets |
| Add another invalid login combination | `test_data/test_login.csv` |
| Change login field locator | `pages/login_page.py` |
| Change Home → Login navigation | `pages/home_page.py` |
| Add a new page | Add `pages/<new_page>.py` and expose it in `pages/application.py` |
| Add a new login scenario | `tests/test_login.py` |
| Add a new marker | Test decorator + register it in `pytest.ini` |
| Change screenshot/trace capture policy | `config/config_qa.yaml` |
| Change artifact-generation implementation | `conftest.py` |
| Add a Python dependency | `requirements.txt` |
| Change lint rules | `ruff.toml` |
| Change CI execution | `.github/workflows/tests.yml` |

A new engineer should avoid placing browser locators directly into the test when that locator belongs to an existing Page Object.

---

# 5. Initial Local Setup

## 5.1 Prerequisites

Recommended baseline for this framework:

- Git
- Python 3.11
- VS Code or another Python IDE
- Network access to `https://automationexercise.com/`
- Allure CLI if the rendered Allure report must be opened locally

The CI workflow explicitly uses Python **3.11**.

Verify:

```powershell
python --version
git --version
```

---

## 5.2 Clone the Repository

```powershell
git clone <repository-url>
cd playwright-python-training
```

Always run framework commands from the **repository root**, where `conftest.py`, `pytest.ini`, and `requirements.txt` are located.

---

## 5.3 Create the Virtual Environment

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Verify that the active Python is from the virtual environment:

```powershell
python --version
python -m pip --version
```

---

## 5.4 Install Python Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Current `requirements.txt` contains:

```text
pytest
playwright
pytest-playwright
allure-pytest
ruff
python-dotenv
pipdeptree
PyYAML
```

What the main packages do:

| Package | Purpose |
|---|---|
| `pytest` | Test discovery and execution |
| `playwright` | Browser automation API |
| `pytest-playwright` | Provides Playwright fixtures such as `page` and `context` |
| `allure-pytest` | Sends Pytest execution information to Allure result files |
| `ruff` | Python linting and formatting |
| `python-dotenv` | Loads local values from `.env` |
| `pipdeptree` | Shows installed dependency tree |
| `PyYAML` | Reads YAML configuration |

Important:

```text
allure-pytest != Allure CLI
```

`allure-pytest` generates Allure-compatible **result data**.

The **Allure CLI** is a separate command-line application used to serve/generate the rendered HTML report.

After installing the Allure CLI using your organization's approved installation method, verify:

```powershell
allure --version
```

---

## 5.5 Install the Playwright Browser

The current framework and CI execute against Chromium:

```powershell
playwright install chromium
```

In Linux CI, the workflow uses:

```bash
playwright install --with-deps chromium
```

The `--with-deps` option installs required operating-system dependencies in addition to the Playwright browser.

---

# 6. Configure Local Secrets and Environment

## 6.1 `.env`

Create a `.env` file in the project root:

```dotenv
ENV=qa
ENV_VALID_EMAIL_ID=<valid Automation Exercise account email>
ENV_VALID_PASSWORD=<valid Automation Exercise account password>
```

Example structure only:

```dotenv
ENV=qa
ENV_VALID_EMAIL_ID=training.user@example.com
ENV_VALID_PASSWORD=replace-with-real-secret
```

Do not commit `.env`.

`file_reader.py` calls:

```python
load_dotenv()
```

so values in `.env` become available through `os.getenv(...)`.

---

## 6.2 Why the Credentials Are Not Stored Directly in CSV

The current login CSV uses placeholders:

```csv
email,password,expected_message,type
${ENV_VALID_EMAIL_ID},${ENV_VALID_PASSWORD},Kuttralakani Moscomani,valid
invalid@example.com,wrongpassword,Your email or password is incorrect!,invalid
```

The valid credential row therefore contains **references to environment variables**, not the secret values themselves.

Flow:

```text
test_login.csv
     |
     | ${ENV_VALID_EMAIL_ID}
     | ${ENV_VALID_PASSWORD}
     v
utilities/file_reader.py
     |
     | os.getenv(...)
     v
.env locally
or
GitHub Secrets in CI
```

This is the correct pattern because secrets do not need to be committed to the repository.

---

# 7. Configuration File

Current `config/config_qa.yaml`:

```yaml
application:
  name: Automation Exercise

base_url: "https://automationexercise.com/"

test_data:
  dir: "test_data/"

artifacts:
  evidence: all   # all | fail
  trace: all      # all | fail | none
```

## Configuration Meaning

### `base_url`

Used by `HomePage.open()`:

```python
self.page.goto(self.base_url, wait_until="domcontentloaded")
```

### `test_data.dir`

Used by `read_csv()` to resolve:

```text
test_data/<file-name>.csv
```

### `artifacts.evidence`

Current supported intent:

```text
all  -> attach screenshot evidence for every test
fail -> attach screenshot evidence only when setup/test call failed
```

### `artifacts.trace`

```text
all  -> save Playwright trace for every test
fail -> save trace only when setup/test call failed
none -> do not start tracing
```

---

# 8. Environment Selection

At the bottom of `file_reader.py`:

```python
_env = os.getenv("ENV", "qa")
CONFIG = read_yaml(f"config/config_{_env}.yaml")
```

This means:

```text
ENV=qa
   |
   v
config/config_qa.yaml
```

If `ENV` is not set, the framework defaults to:

```text
qa
```

To add another environment:

```text
config/
├── config_qa.yaml
└── config_uat.yaml
```

Then in PowerShell:

```powershell
$env:ENV="uat"
pytest --browser chromium
```

Or place:

```dotenv
ENV=uat
```

in `.env`.

The corresponding `config/config_uat.yaml` must exist.

---

# 9. How `file_reader.py` Works

`utilities/file_reader.py` provides two primary public functions:

```python
read_csv(...)
read_yaml(...)
```

and also performs environment-placeholder resolution.

## 9.1 Project Root Resolution

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
```

This allows files to be found relative to the repository root instead of depending on the current operating-system path.

---

## 9.2 Resolving `${ENV_VARIABLE}`

The pattern:

```python
ENV_VARIABLE_PATTERN = re.compile(r"^\$\{([A-Z0-9_]+)\}$")
```

recognizes values such as:

```text
${ENV_VALID_EMAIL_ID}
```

Then:

```python
environment_value = os.getenv(variable_name)
```

retrieves the real value.

If the value is missing:

```python
raise ValueError(
    f"Environment variable is not configured: {variable_name}"
)
```

So a missing credential is reported clearly rather than sending an empty password to the website.

---

## 9.3 Reading Login CSV Data

The test uses:

```python
read_csv("test_login.csv")
```

Internally, the utility converts the file name into:

```text
test_data/test_login.csv
```

and returns:

```python
list[dict[str, str]]
```

Conceptually:

```python
[
    {
        "email": "<resolved valid email>",
        "password": "<resolved valid password>",
        "expected_message": "Kuttralakani Moscomani",
        "type": "valid",
    },
    {
        "email": "invalid@example.com",
        "password": "wrongpassword",
        "expected_message": "Your email or password is incorrect!",
        "type": "invalid",
    },
]
```

The secret values are resolved in memory; they do not need to be written back to the CSV.

---

# 10. Page Object Model Used by This Framework

The framework currently uses:

```text
Application
   |
   +-- HomePage
   +-- LoginPage
   +-- LandingPage
```

All Page Objects share the same Playwright `Page` instance.

---

# 11. `pages/application.py`

Current purpose:

```python
class Application:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page

        self.home_page = HomePage(page, base_url)
        self.login_page = LoginPage(page)
        self.landing_page = LandingPage(page)
```

Instead of a test separately doing:

```python
home_page = HomePage(page, base_url)
login_page = LoginPage(page)
landing_page = LandingPage(page)
```

the framework creates:

```python
app
```

and the test uses:

```python
app.home_page
app.login_page
app.landing_page
```

This keeps the test readable.

## Adding a New Page Object

Example: `ProductsPage`.

Create:

```text
pages/products_page.py
```

Then update `application.py`:

```python
from pages.products_page import ProductsPage
```

and:

```python
self.products_page = ProductsPage(page)
```

The test can then use:

```python
app.products_page
```

---

# 12. `pages/home_page.py`

Responsibilities:

- open the AUT
- verify the Automation Exercise title
- navigate to Products
- navigate to Signup / Login

Important method:

```python
def open(self) -> None:
    self.page.goto(self.base_url, wait_until="domcontentloaded")
    expect(self.page).to_have_title(
        re.compile(r"Automation Exercise")
    )
```

This method both navigates and confirms that the expected application page was reached.

Login navigation:

```python
def go_to_login(self) -> None:
    self.page.get_by_role(
        "link",
        name="Signup / Login",
    ).click()
```

If the navigation link changes in the application, this Page Object is the primary place to update it.

---

# 13. `pages/login_page.py`

The constructor defines reusable login-page locators:

```python
self.login_heading = page.get_by_role(
    "heading",
    name="Login to your account",
)

self.email_input = page.locator(
    '[data-qa="login-email"]'
)

self.password_input = page.locator(
    '[data-qa="login-password"]'
)

self.login_button = page.locator(
    '[data-qa="login-button"]'
)
```

Login operation:

```python
def login(self, email: str, password: str) -> None:
    self.email_input.fill(email)
    self.password_input.fill(password)
    self.login_button.click()
```

Invalid-login assertion:

```python
def verify_login_error(self, expected_message: str) -> None:
    expect(
        self.page.get_by_text(
            expected_message,
            exact=True,
        )
    ).to_be_visible()
```

A locator change should be fixed here instead of copied into every test.

---

# 14. `pages/landing_page.py`

After a valid login, the framework verifies:

```python
def verify_logged_in(self, username: str) -> None:
    expect(
        self.page.get_by_text(
            f"Logged in as {username}"
        )
    ).to_be_visible()
```

It also contains reusable locators/actions for:

```text
Logout
Delete Account
```

Current logout method:

```python
def logout(self) -> None:
    self.logout_link.click()
```

---

# 15. `tests/test_login.py`

There are two test definitions.

## 15.1 Login Page Load Test

```python
def test_login_page_loads(app: Application) -> None:
    with allure.step("Open the application"):
        app.home_page.open()

    with allure.step("Navigate to the login page"):
        app.home_page.go_to_login()

    with allure.step("Verify the login page is displayed"):
        app.login_page.verify_loaded()
```

This is one Pytest execution.

---

## 15.2 Data-Driven Login Validation

The test is parameterized using:

```python
@pytest.mark.parametrize(
    "credentials",
    read_csv("test_login.csv"),
)
```

The current CSV contains two data rows.

Therefore this one Python test function produces **two Pytest executions**:

```text
test_login_validation[valid row]
test_login_validation[invalid row]
```

Together with `test_login_page_loads`, the current login file produces:

```text
3 executions
```

assuming both CSV rows are successfully loaded.

---

# 16. Important: When Is the CSV Read?

This is a critical framework behavior.

The expression:

```python
@pytest.mark.parametrize(
    "credentials",
    read_csv("test_login.csv"),
)
```

is evaluated when Pytest **imports/collects the test module**.

Therefore the sequence is:

```text
Pytest starts
   |
   v
imports test_login.py
   |
   v
read_csv("test_login.csv") executes
   |
   v
CSV placeholders are resolved
   |
   v
parameterized test cases are created
   |
   v
actual test execution starts later
```

Consequences:

- `.env` / environment variables must already be configured before running Pytest.
- If `ENV_VALID_EMAIL_ID` is missing, collection can fail before a browser test begins.
- If `test_data/test_login.csv` is missing, collection can fail.
- The data is not loaded inside the test body.

---

# 17. Pytest Markers

The tests currently use:

```python
@pytest.mark.smoke
@pytest.mark.regression
```

Markers are registered in `pytest.ini`:

```ini
[pytest]
addopts = -rA
testpaths = tests
markers =
    smoke: Critical business flow tests
    regression: Regression test suit
```

Useful commands:

```powershell
pytest -m smoke
```

```powershell
pytest -m regression
```

```powershell
pytest -m "smoke and regression"
```

Current login tests carry both markers.

---

# 18. `pytest.ini`

Current configuration:

```ini
[pytest]
addopts = -rA
testpaths = tests
markers =
    smoke: Critical business flow tests
    regression: Regression test suit
```

Meaning:

### `testpaths = tests`

Pytest searches the `tests/` directory by default.

### `addopts = -rA`

Provides additional summary information for all result types.

### `markers`

Registers custom markers and prevents them from being undocumented framework conventions.

---

# 19. `conftest.py` — Core Framework Execution Control

`conftest.py` is the main Pytest integration point for this framework.

It controls:

- timestamped artifact folders
- Allure results location
- `app` fixture
- test-result capture
- screenshot evidence
- Playwright tracing

---

# 20. Timestamped Artifact Folder

At module load time:

```python
RUN_TIMESTAMP = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

RUN_ARTIFACT_DIR = (
    Path("artifacts") / RUN_TIMESTAMP
)

ALLURE_RESULTS_DIR = (
    RUN_ARTIFACT_DIR / "allure-results"
)

TRACE_DIR = (
    RUN_ARTIFACT_DIR / "traces"
)
```

Example:

```text
artifacts/
└── 20260821_123045/
    ├── allure-results/
    └── traces/
```

One Pytest process uses one timestamp value for that execution session.

---

# 21. How Allure Results Are Automatically Redirected

The hook:

```python
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    RUN_ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    config.option.allure_report_dir = str(
        ALLURE_RESULTS_DIR
    )
```

does two things:

1. Creates the timestamped run folder.
2. Sets the Allure Pytest result directory programmatically.

Because of this, the normal test command does **not** need:

```text
--alluredir=...
```

The framework sends results to:

```text
artifacts/<timestamp>/allure-results/
```

automatically.

---

# 22. The `app` Fixture

```python
@pytest.fixture
def app(page: Page) -> Application:
    return Application(
        page,
        CONFIG["base_url"],
    )
```

The `page` argument is not another local fixture written in this repository.

It is supplied by:

```text
pytest-playwright
```

Flow:

```text
pytest-playwright
     |
     v
Playwright context
     |
     v
Playwright page
     |
     v
app fixture
     |
     v
Application(page, base_url)
     |
     +-- HomePage
     +-- LoginPage
     +-- LandingPage
     |
     v
test function
```

The test asks only for:

```python
app
```

but Pytest resolves the complete fixture dependency chain automatically.

---

# 23. Result Hook

Current hook:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(
        item,
        f"rep_{report.when}",
        report,
    )
```

Pytest has execution phases such as:

```text
setup
call
teardown
```

This hook stores reports on the test node, for example:

```text
rep_setup
rep_call
rep_teardown
```

The artifact fixture later reads `rep_setup` and `rep_call` to decide whether the test failed.

---

# 24. Automatic Evidence / Trace Fixture

The fixture is:

```python
@pytest.fixture(autouse=True)
def capture_artifacts(
    page: Page,
    context,
    request,
):
```

Because it uses:

```python
autouse=True
```

every test automatically gets this behavior.

The test does not have to write:

```python
capture_artifacts
```

as an argument.

---

# 25. `yield` Defines Setup and Teardown

The key structure is:

```python
if trace_mode != "none":
    context.tracing.start(...)

yield

# evidence / trace handling here
```

Therefore:

```text
BEFORE yield
    =
fixture setup
    =
start tracing if enabled

yield
    =
give control to test

AFTER yield
    =
fixture teardown
    =
check result
take screenshot if required
save/stop trace
attach evidence
```

This is the clearest way to identify setup/test/teardown in the framework.

---

# 26. Current Screenshot Evidence Behavior

After the test:

```python
if capture_evidence:
    screenshot = page.screenshot(
        full_page=True
    )

    allure.attach(
        screenshot,
        name="Test Evidence",
        attachment_type=
            allure.attachment_type.PNG,
    )
```

Important:

- The screenshot is captured in memory.
- It is attached to Allure.
- The current code does **not** save a separate screenshot `.png` file under `artifacts/`.

With:

```yaml
artifacts:
  evidence: all
```

every test gets screenshot evidence.

With:

```yaml
artifacts:
  evidence: fail
```

the screenshot is captured only when the stored setup/call result indicates failure.

---

# 27. Current Trace Behavior

When tracing is enabled:

```python
context.tracing.start(
    screenshots=True,
    snapshots=True,
    sources=True,
)
```

After the test, when the trace must be retained:

```python
trace_path = (
    TRACE_DIR
    / f"{request.node.name}.zip"
)

context.tracing.stop(
    path=str(trace_path)
)
```

Then the same trace is attached to Allure:

```python
allure.attach.file(
    trace_path,
    name="Playwright Trace",
    attachment_type="application/zip",
)
```

Example:

```text
artifacts/
└── 20260821_123045/
    └── traces/
        ├── test_login_page_loads[chromium].zip
        ├── test_login_validation[credentials0-chromium].zip
        └── test_login_validation[credentials1-chromium].zip
```

Actual parameterized names can vary based on Pytest-generated node names.

---

# 28. Exact Test Execution Flow

This is the complete flow a new engineer should understand.

## Phase A — Command Starts Pytest

Example:

```powershell
pytest --browser chromium
```

Pytest loads:

```text
pytest.ini
plugins
conftest.py
```

---

## Phase B — Framework Configuration Is Loaded

When `conftest.py` imports:

```python
from utilities.file_reader import CONFIG
```

`file_reader.py` executes:

```python
load_dotenv()
```

then determines:

```python
_env = os.getenv("ENV", "qa")
```

and loads:

```text
config/config_qa.yaml
```

if `ENV=qa`.

---

## Phase C — Artifact Run Folder Is Configured

`pytest_configure()` creates:

```text
artifacts/<timestamp>/
```

and tells Allure Pytest to write result data to:

```text
artifacts/<timestamp>/allure-results/
```

---

## Phase D — Pytest Collects Tests

Pytest discovers:

```text
tests/test_login.py
```

because:

```ini
testpaths = tests
```

and test functions begin with:

```text
test_
```

---

## Phase E — CSV Is Loaded During Collection

While importing `test_login.py`:

```python
read_csv("test_login.csv")
```

runs.

The utility:

1. finds `test_data/test_login.csv`
2. reads each row
3. sees `${ENV_VALID_EMAIL_ID}`
4. gets `ENV_VALID_EMAIL_ID`
5. sees `${ENV_VALID_PASSWORD}`
6. gets `ENV_VALID_PASSWORD`
7. returns the resolved rows
8. Pytest creates one parameterized execution per row

---

## Phase F — Marker Selection Is Applied

If the command is:

```powershell
pytest -m smoke --browser chromium
```

Pytest executes only tests selected by the `smoke` expression.

---

## Phase G — Playwright Fixtures Are Created

For each selected test, Pytest resolves fixture dependencies.

Conceptually:

```text
pytest-playwright
      |
      v
browser
      |
      v
context
      |
      v
page
```

The exact plugin lifecycle is handled by `pytest-playwright`.

---

## Phase H — Autouse Artifact Fixture Setup Runs

`capture_artifacts(...)` automatically runs.

It reads:

```python
CONFIG["artifacts"]["evidence"]
CONFIG["artifacts"]["trace"]
```

If trace is enabled:

```python
context.tracing.start(...)
```

executes before the test body.

---

## Phase I — `app` Fixture Is Supplied

For tests requesting:

```python
app: Application
```

the fixture returns:

```python
Application(
    page,
    CONFIG["base_url"],
)
```

The same `page` is passed to:

```text
HomePage
LoginPage
LandingPage
```

---

## Phase J — Test Body Runs

For valid login, the flow is:

```text
test_login_validation
      |
      v
app.home_page.open()
      |
      v
page.goto(base_url)
      |
      v
verify title
      |
      v
app.home_page.go_to_login()
      |
      v
click "Signup / Login"
      |
      v
app.login_page.verify_loaded()
      |
      v
verify login heading
      |
      v
app.login_page.login(email, password)
      |
      +-- fill email
      +-- fill password
      +-- click Login
      |
      v
credentials["type"] == "valid"
      |
      v
app.landing_page.verify_logged_in(...)
      |
      v
Playwright expect(...)
```

For the invalid row:

```text
credentials["type"] == "invalid"
      |
      v
app.login_page.verify_login_error(...)
      |
      v
Playwright expect(...)
```

---

## Phase K — Allure Steps Are Recorded

The test body groups execution using:

```python
with allure.step("Open the application"):
```

and similar steps.

The report therefore shows meaningful business-level steps rather than only Python stack information.

---

## Phase L — Pytest Records Test Result

`pytest_runtest_makereport` stores the result for:

```text
setup
call
teardown
```

The artifact fixture uses the stored setup/call status.

---

## Phase M — Artifact Fixture Teardown Runs

Execution returns to the code after:

```python
yield
```

The framework decides:

```python
test_failed = ...
capture_evidence = ...
save_trace = ...
```

Then it:

- captures screenshot evidence when required
- attaches screenshot to Allure
- stops tracing
- saves trace ZIP when required
- attaches saved trace to Allure

---

## Phase N — Playwright / Pytest Cleanup Completes

The `page` / `context` resources owned by `pytest-playwright` are cleaned up by their fixture lifecycle.

---

## Phase O — Allure Result Files Remain

At the end of the run:

```text
artifacts/<timestamp>/allure-results/
```

contains the machine-readable data required to render the Allure report.

If tracing was retained:

```text
artifacts/<timestamp>/traces/
```

contains ZIP traces.

---

# 29. Setup vs Test Body vs Teardown — Quick View

For a test using `app`:

```text
SETUP
------------------------------------------------
Load env/config
Resolve Pytest fixtures
Create browser context/page
Start Playwright tracing
Create Application/Page Objects

TEST BODY
------------------------------------------------
Execute test function
Run Allure steps
Call Page Objects
Interact with browser
Run Playwright assertions

TEARDOWN / EVIDENCE
------------------------------------------------
Inspect test result
Capture screenshot when configured
Stop/save trace when configured
Attach evidence to Allure
Playwright fixture cleanup
```

---

# 30. Running the Tests Locally

Run all discovered tests:

```powershell
pytest --browser chromium
```

Run headed:

```powershell
pytest --browser chromium --headed
```

Run only smoke:

```powershell
pytest -m smoke --browser chromium
```

Run only regression:

```powershell
pytest -m regression --browser chromium
```

Run one file:

```powershell
pytest tests/test_login.py --browser chromium
```

Run one test function:

```powershell
pytest tests/test_login.py::test_login_page_loads --browser chromium
```

Run tests whose name contains `login`:

```powershell
pytest -k login --browser chromium
```

Show more detailed test names/results:

```powershell
pytest -v --browser chromium
```

Stop after the first failure:

```powershell
pytest -x --browser chromium
```

Collect without executing:

```powershell
pytest --collect-only
```

---

# 31. Verify Generated Artifacts

After execution:

```powershell
Get-ChildItem .\artifacts
```

Typical structure:

```text
artifacts/
└── 20260821_123045/
    ├── allure-results/
    └── traces/
```

The `traces/` directory is created only when a trace must actually be saved.

---

# 32. Open a Playwright Trace

Example:

```powershell
playwright show-trace ".\artifacts\<timestamp>\traces\<trace-file>.zip"
```

A trace is useful for examining:

- action sequence
- DOM snapshot
- screenshots captured by tracing
- timing
- source information
- page state around the failure

---

# 33. Allure: Results vs Report

This distinction is important.

## Allure Results

Automatically produced by this framework:

```text
artifacts/<timestamp>/allure-results/
```

These are machine-readable execution files.

## Allure Report

The rendered HTML report is created from the result directory.

The current `conftest.py` and GitHub Actions workflow **do not automatically generate the static `allure-report/` folder**.

Generate it explicitly when needed.

---

# 34. Serve the Latest Allure Results Directly

First identify the latest run in PowerShell:

```powershell
$run = Get-ChildItem .\artifacts -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
```

Then:

```powershell
allure serve "$($run.FullName)\allure-results"
```

`allure serve` creates a temporary rendered report and opens it.

---

# 35. Generate a Static Allure Report Inside the Same Artifact Run

To satisfy the structure:

```text
artifacts/
└── <timestamp>/
    ├── allure-results/
    ├── traces/
    └── allure-report/
```

use:

```powershell
$run = Get-ChildItem .\artifacts -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
```

Then:

```powershell
allure generate `
    "$($run.FullName)\allure-results" `
    -o "$($run.FullName)\allure-report" `
    --clean
```

Open it:

```powershell
allure open "$($run.FullName)\allure-report"
```

This leaves the rendered report inside the same timestamped execution folder.

---

# 36. What You Should See in Allure

The current tests provide:

### Feature

```text
Authentication
```

### Stories

```text
Login Page
Login Validation
```

### Titles

```text
Verify login page loads successfully
Validate login with different credentials
```

### Steps

Examples:

```text
Open the application
Navigate to the login page
Verify the login page is displayed
Enter credentials and submit login
Verify successful login
Verify login error message
```

### Dynamic Parameter

```python
allure.dynamic.parameter(
    "Login Type",
    credentials["type"],
)
```

This records whether the parameterized execution is:

```text
valid
invalid
```

### Evidence

Depending on config:

- screenshot attachment
- Playwright trace ZIP attachment

---

# 37. Ruff Code Quality

Current `ruff.toml`:

```toml
line-length = 100

extend-exclude = [
    "artifacts/",
]

[lint]
select = ["E", "F", "I", "UP"]

[format]
quote-style = "double"
indent-style = "space"
```

Main rule groups:

| Rule Group | General purpose |
|---|---|
| `E` | Python style/error rules derived from pycodestyle |
| `F` | Pyflakes-style correctness issues |
| `I` | Import sorting |
| `UP` | Python syntax modernization |

Generated execution files under:

```text
artifacts/
```

are excluded.

Run lint:

```powershell
ruff check .
```

Check formatting:

```powershell
ruff format --check .
```

Apply formatting:

```powershell
ruff format .
```

Apply safe lint fixes when available:

```powershell
ruff check . --fix
```

Recommended local validation before commit:

```powershell
ruff format --check .
ruff check .
pytest -m smoke --browser chromium
```

---

# 38. GitHub Actions CI Flow

Current `.github/workflows/tests.yml` is named:

```yaml
name: UI Automation
```

Triggers:

```yaml
on:
  workflow_dispatch:
  push:
  pull_request:
```

So it can run:

- manually
- on push
- on pull request

---

# 39. CI Environment Variables and Secrets

The workflow defines:

```yaml
env:
  ENV: qa
  ENV_VALID_EMAIL_ID: ${{ secrets.ENV_VALID_EMAIL_ID }}
  ENV_VALID_PASSWORD: ${{ secrets.ENV_VALID_PASSWORD }}
```

Therefore GitHub repository secrets must contain:

```text
ENV_VALID_EMAIL_ID
ENV_VALID_PASSWORD
```

Do not put the real credentials into:

```text
tests.yml
test_login.csv
config_qa.yaml
```

The CI data-resolution path is:

```text
GitHub Secret
    |
    v
Workflow environment variable
    |
    v
os.getenv(...)
    |
    v
read_csv(...)
    |
    v
parameterized test
```

---

# 40. CI Steps in Exact Order

The workflow performs:

```text
1. Checkout repository
2. Setup Python 3.11
3. Restore/use pip cache when possible
4. Upgrade pip
5. Install requirements.txt
6. Install Chromium + Linux dependencies
7. Run Ruff formatting check
8. Run Ruff lint check
9. Run smoke tests with Chromium
10. Upload artifacts/ even if a previous step failed
```

The commands are:

```yaml
- name: Run Ruff
  run: |
    ruff format --check .
    ruff check .
```

Then:

```yaml
- name: Run tests
  run: pytest -m smoke --browser chromium
```

Then:

```yaml
- name: Upload test artifacts
  if: always()
  uses: actions/upload-artifact@v7
  with:
    name: test-artifacts
    path: artifacts/
    if-no-files-found: ignore
```

Because of:

```yaml
if: always()
```

GitHub attempts to upload the artifacts even when a test fails.

---

# 41. Local Execution vs CI Execution

| Area | Local | GitHub Actions |
|---|---|---|
| Environment | `.env` / shell variables | Workflow `env` |
| Valid credentials | `.env` | GitHub Secrets |
| Python | Developer venv | Python 3.11 runner setup |
| Browser | `playwright install chromium` | `playwright install --with-deps chromium` |
| Test command | Developer chooses | `pytest -m smoke --browser chromium` |
| Artifacts | `artifacts/<timestamp>/` | Same folder, then uploaded |
| Ruff | Run manually | Mandatory before tests |
| Allure static report | Generated manually if needed | Not generated by current workflow |
| Allure results | Automatic through `conftest.py` | Automatic through `conftest.py` |

---

# 42. Adding a New Test — Recommended Procedure

Assume a new requirement:

```text
Verify logout after successful login.
```

Follow this sequence.

## Step 1 — Check Existing Page Objects

The current `LandingPage` already contains:

```python
def logout(self) -> None:
    self.logout_link.click()
```

Reuse it rather than adding another direct locator in the test.

---

## Step 2 — Check Required Test Data

If the scenario uses the existing valid user, reuse the existing CSV or introduce data in a way consistent with the scenario.

Do not duplicate the real password in source code.

---

## Step 3 — Add the Test

Example pattern:

```python
@pytest.mark.smoke
@allure.feature("Authentication")
@allure.story("Logout")
@allure.title("Logged-in user can log out")
def test_logout(app: Application, ...):
    with allure.step("Open the application"):
        ...

    with allure.step("Login"):
        ...

    with allure.step("Logout"):
        app.landing_page.logout()

    with allure.step("Verify login page is displayed"):
        app.login_page.verify_loaded()
```

The exact data design should match the rest of the framework and requirement.

---

## Step 4 — Run the Specific Test

```powershell
pytest tests/test_login.py -k logout --browser chromium --headed
```

---

## Step 5 — Run Ruff

```powershell
ruff format --check .
ruff check .
```

---

## Step 6 — Run Relevant Suite

```powershell
pytest -m smoke --browser chromium
```

---

## Step 7 — Review Artifacts

Check:

```text
artifacts/<timestamp>/allure-results/
artifacts/<timestamp>/traces/
```

Generate/open Allure if needed.

---

# 43. Adding a New Page — Recommended Procedure

Example: Products Page.

## Create

```text
pages/products_page.py
```

Suggested pattern:

```python
from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_input = page.locator(
            '[data-qa="search-product"]'
        )

    def search(self, product_name: str) -> None:
        self.search_input.fill(product_name)
        ...
```

## Expose It Through `Application`

In `pages/application.py`:

```python
from pages.products_page import ProductsPage
```

and:

```python
self.products_page = ProductsPage(page)
```

## Use It in the Test

```python
app.products_page.search("Blue Top")
```

This preserves the existing framework model.

---

# 44. Adding a New CSV Data File

Suppose you add:

```text
test_data/test_product_search.csv
```

Example:

```csv
search_term,expected_product
Blue Top,Blue Top
Men Tshirt,Men Tshirt
```

Load it:

```python
@pytest.mark.parametrize(
    "product",
    read_csv("test_product_search.csv"),
)
```

Because `read_csv()` uses:

```yaml
test_data:
  dir: "test_data/"
```

you do not pass the complete `test_data/` path.

---

# 45. Adding a New Environment

Create:

```text
config/config_uat.yaml
```

Use the same expected keys:

```yaml
application:
  name: Automation Exercise

base_url: "https://uat.example.com/"

test_data:
  dir: "test_data/"

artifacts:
  evidence: fail
  trace: fail
```

Run:

```powershell
$env:ENV="uat"
pytest --browser chromium
```

The environment file name must match:

```text
config/config_<ENV>.yaml
```

---

# 46. Common Failures and Where to Look

## `Environment variable is not configured`

Example:

```text
ValueError: Environment variable is not configured: ENV_VALID_EMAIL_ID
```

Check:

```text
.env locally
GitHub Secret in CI
variable spelling
```

Remember: CSV resolution happens during test collection.

---

## `Config file not found`

Check:

```text
ENV value
config/config_<ENV>.yaml
repository root
file name
```

---

## `Test Data file not found`

Check:

```text
config_qa.yaml -> test_data.dir
test_data/test_login.csv
CSV file name passed to read_csv()
```

---

## Locator Timeout

Example symptoms:

```text
Locator.click: Timeout ...
waiting for locator(...)
```

Check:

```text
Is the correct page open?
Did navigation succeed?
Did the AUT change?
Is the locator still valid?
Is another overlay blocking interaction?
```

Fix the locator/behavior in the appropriate Page Object.

Do not first solve it by adding `time.sleep()`.

---

## Allure Command Not Found

If:

```text
allure : command not found
```

remember:

```text
pip install allure-pytest
```

does not install the Allure CLI.

Install/configure the Allure CLI separately and verify:

```powershell
allure --version
```

---

## No Trace Folder

Check:

```yaml
artifacts:
  trace: none
```

If `trace: fail`, no trace is saved for passing tests.

---

## No Screenshot File in `artifacts`

This is expected with the current implementation.

The screenshot is attached directly to Allure in memory:

```python
allure.attach(screenshot, ...)
```

It is not saved as a standalone PNG.

---

# 47. Important Current Framework Behaviors

A new engineer should know these details.

1. **Allure results are automatic.**  
   `conftest.py` redirects Allure output to the timestamped artifact run.

2. **The rendered Allure report is not automatic.**  
   Generate `allure-report/` using the Allure CLI when required.

3. **CSV data is resolved during collection.**  
   Missing environment credentials can stop collection.

4. **Valid secrets are external.**  
   The CSV contains `${...}` placeholders.

5. **Screenshot evidence is an Allure attachment.**  
   It is not currently written as a separate PNG file.

6. **Traces are real ZIP files.**  
   When retained, they are stored under `artifacts/<timestamp>/traces/` and attached to Allure.

7. **Artifact capture is autouse.**  
   Tests do not have to request the fixture.

8. **CI currently runs smoke only.**  
   The workflow command is:

   ```bash
   pytest -m smoke --browser chromium
   ```

9. **CI currently uses Playwright Chromium.**  
   It does not run the Google Chrome channel.

10. **Current failure-evidence decision uses setup/call results.**  
    `capture_artifacts` checks `rep_setup` and `rep_call`.

---

# 48. Recommended New-Joiner First Run

Use this sequence after cloning the project.

```powershell
# 1. Create environment
python -m venv .venv

# 2. Activate
.venv\Scripts\Activate.ps1

# 3. Install packages
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Install browser
playwright install chromium

# 5. Create .env with the required values
# ENV=qa
# ENV_VALID_EMAIL_ID=<secret>
# ENV_VALID_PASSWORD=<secret>

# 6. Verify test discovery
pytest --collect-only

# 7. Run one simple test headed
pytest tests/test_login.py::test_login_page_loads `
    --browser chromium `
    --headed

# 8. Run smoke
pytest -m smoke --browser chromium

# 9. Run code quality checks
ruff format --check .
ruff check .

# 10. Inspect latest artifact folder
Get-ChildItem .\artifacts
```

Then open Allure:

```powershell
$run = Get-ChildItem .\artifacts -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

allure serve "$($run.FullName)\allure-results"
```

---

# 49. Recommended Pre-Commit Validation

Before committing framework changes:

```powershell
ruff format --check .
ruff check .
pytest -m smoke --browser chromium
```

If formatting needs correction:

```powershell
ruff format .
```

Then re-run:

```powershell
ruff check .
pytest -m smoke --browser chromium
```

Review:

```powershell
git status
git diff
```

before staging/committing.

---

# 50. Framework Development Rules

For consistency, follow these rules.

## Tests

Keep in:

```text
tests/
```

Tests should explain the scenario and expected result.

Avoid embedding page-specific selector details in tests.

---

## Page Objects

Keep in:

```text
pages/
```

Page Objects should own:

- locators
- page-specific actions
- reusable page-specific validations where the current framework uses them

Do not duplicate the same locator across multiple test files.

---

## Test Data

Keep data-driven input in:

```text
test_data/
```

Do not put real secrets into CSV.

Use:

```text
${ENV_VARIABLE}
```

where secret resolution is required.

---

## Configuration

Keep environment-level settings in:

```text
config/config_<environment>.yaml
```

Do not hard-code the QA URL into every test.

---

## Utilities

Keep reusable technical file/config logic in:

```text
utilities/
```

Do not turn utilities into a dumping ground for page interactions.

---

## Fixtures / Hooks

Framework-wide execution behavior belongs in:

```text
conftest.py
```

Examples:

- shared fixtures
- tracing
- screenshot evidence
- test-result hooks
- artifact directories

---

## Secrets

Local:

```text
.env
```

CI:

```text
GitHub Secrets
```

Never commit passwords/tokens.

---

# 51. Complete Framework Mental Model

```text
Developer
   |
   | pytest -m smoke --browser chromium
   v
Pytest
   |
   +--> pytest.ini
   |
   +--> conftest.py
   |       |
   |       +--> CONFIG
   |       |     |
   |       |     +--> .env
   |       |     +--> config/config_qa.yaml
   |       |
   |       +--> artifact timestamp folder
   |       +--> page/context fixtures
   |       +--> tracing
   |       +--> app fixture
   |
   v
Collect tests/test_login.py
   |
   +--> read_csv("test_login.csv")
   |       |
   |       +--> test_data/test_login.csv
   |       +--> resolve ${ENV_*}
   |
   v
Parameterized Test Execution
   |
   v
Application
   |
   +--> HomePage
   +--> LoginPage
   +--> LandingPage
   |
   v
Playwright Page
   |
   v
Chromium
   |
   v
Automation Exercise
   |
   v
Playwright expect()
   |
   v
Pytest result
   |
   v
capture_artifacts teardown
   |
   +--> screenshot -> Allure attachment
   +--> trace.zip -> artifacts/<timestamp>/traces/
   +--> trace.zip -> Allure attachment
   |
   v
artifacts/<timestamp>/allure-results/
   |
   v
allure serve / allure generate
   |
   v
Rendered Allure Report
```

---

# 52. Quick Command Reference

| Purpose | Command |
|---|---|
| Create venv | `python -m venv .venv` |
| Activate PowerShell venv | `.venv\Scripts\Activate.ps1` |
| Install dependencies | `pip install -r requirements.txt` |
| Install Chromium | `playwright install chromium` |
| Collect tests | `pytest --collect-only` |
| Run all tests | `pytest --browser chromium` |
| Run headed | `pytest --browser chromium --headed` |
| Run smoke | `pytest -m smoke --browser chromium` |
| Run regression | `pytest -m regression --browser chromium` |
| Run one file | `pytest tests/test_login.py --browser chromium` |
| Run one test | `pytest tests/test_login.py::test_login_page_loads --browser chromium` |
| Name filter | `pytest -k login --browser chromium` |
| Open trace | `playwright show-trace <trace.zip>` |
| Ruff format check | `ruff format --check .` |
| Ruff lint | `ruff check .` |
| Ruff auto-format | `ruff format .` |
| Ruff safe fixes | `ruff check . --fix` |
| Verify Allure CLI | `allure --version` |
| Serve results | `allure serve <allure-results-path>` |
| Generate report | `allure generate <results> -o <report> --clean` |
| Open static report | `allure open <report-path>` |

---

# 53. New Joiner Checklist

Before modifying tests, a new engineer should be able to answer:

- [ ] What does `tests/test_login.py` validate?
- [ ] Where do login locators live?
- [ ] What does `Application` provide?
- [ ] Where does the base URL come from?
- [ ] How is `ENV=qa` used?
- [ ] Where do valid credentials come from locally?
- [ ] Where do valid credentials come from in GitHub Actions?
- [ ] Why does the CSV contain `${ENV_VALID_EMAIL_ID}`?
- [ ] When is `read_csv()` executed?
- [ ] Where does the Playwright `page` fixture come from?
- [ ] What does the `app` fixture return?
- [ ] What happens before and after `yield` in `capture_artifacts`?
- [ ] How is a failed test recognized?
- [ ] Where are traces stored?
- [ ] Where are screenshot attachments stored?
- [ ] Where are Allure result files stored?
- [ ] How is a rendered Allure report generated?
- [ ] Which command does CI use?
- [ ] Which files should be changed for a new page/test/data/environment?
- [ ] Which checks should pass before committing?

If these are understood, the engineer has the core knowledge required to start contributing safely to the framework.

---

# 54. Final End-to-End Summary

A normal framework execution can be summarized as:

```text
1. Developer activates .venv
2. Environment/secrets are available
3. Developer runs pytest
4. Pytest loads pytest.ini and conftest.py
5. file_reader loads .env and config_<ENV>.yaml
6. conftest creates artifacts/<timestamp>
7. Allure output is redirected to allure-results
8. Pytest discovers tests
9. test_login.py loads CSV during collection
10. CSV ${ENV_*} placeholders are resolved
11. Pytest creates parameterized executions
12. pytest-playwright creates context/page
13. capture_artifacts starts tracing if configured
14. app fixture creates Application + Page Objects
15. Test body executes Allure steps
16. Page Objects interact with Automation Exercise
17. Playwright expect assertions validate results
18. Pytest records pass/fail
19. capture_artifacts captures screenshot/trace as configured
20. Evidence is attached to Allure
21. Trace ZIP is stored under the timestamped artifacts folder
22. Allure result files remain in allure-results
23. Allure CLI serves or generates the rendered report
24. Locally, Ruff validates code quality
25. In CI, GitHub Actions performs Ruff + smoke execution and uploads artifacts
```

That is the complete execution lifecycle of the current framework.
