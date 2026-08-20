from datetime import datetime
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from pages.application import Application
from utilities.file_reader import CONFIG


RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_ARTIFACT_DIR = Path("artifacts") / RUN_TIMESTAMP
ALLURE_RESULTS_DIR = RUN_ARTIFACT_DIR / "allure-results"
TRACE_DIR = RUN_ARTIFACT_DIR / "traces"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    RUN_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    config.option.allure_report_dir = str(ALLURE_RESULTS_DIR)


@pytest.fixture
def app(page: Page) -> Application:
    return Application(page, CONFIG["base_url"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def capture_artifacts(page: Page, context, request):
    evidence_mode = CONFIG["artifacts"]["evidence"]
    trace_mode = CONFIG["artifacts"]["trace"]

    if trace_mode != "none":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    setup_report = getattr(request.node, "rep_setup", None)
    call_report = getattr(request.node, "rep_call", None)

    test_failed = any(report is not None and report.failed for report in (setup_report, call_report))

    capture_evidence = evidence_mode == "all" or (evidence_mode == "fail" and test_failed)
    save_trace = trace_mode == "all" or (trace_mode == "fail" and test_failed)

    if capture_evidence:
        screenshot = page.screenshot(full_page=True)
        allure.attach(screenshot, name="Test Evidence", attachment_type=allure.attachment_type.PNG)

    if trace_mode != "none":
        if save_trace:
            TRACE_DIR.mkdir(parents=True, exist_ok=True)
            trace_path = TRACE_DIR / f"{request.node.name}.zip"
            context.tracing.stop(path=str(trace_path))
            allure.attach.file(trace_path, name="Playwright Trace", attachment_type="application/zip")
        else:
            context.tracing.stop()