import os
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import allure
import allure_commons
import pytest
from playwright.sync_api import Page

from pages.application import Application
from utilities.api_client import create_user, delete_user
from utilities.data_generator import build_unique_user
from utilities.file_reader import CONFIG, read_csv

# Shared across all xdist workers: master process sets this env var first,
# workers inherit it and os.environ.setdefault becomes a no-op.
RUN_TIMESTAMP = os.environ.setdefault(
    "PYTEST_RUN_TIMESTAMP", datetime.now().strftime("%Y%m%d_%H%M%S")
)
RUN_ARTIFACT_DIR = Path(CONFIG["artifacts"]["root_dir"]) / RUN_TIMESTAMP
ALLURE_RESULTS_DIR = RUN_ARTIFACT_DIR / CONFIG["artifacts"]["allure_dir"]
TRACE_DIR = RUN_ARTIFACT_DIR / CONFIG["artifacts"]["trace_dir"]


class StepScreenshotPlugin:
    """Attaches a screenshot inside each allure.step() block when it closes."""

    def __init__(self, page: Page, evidence_mode: str) -> None:
        self._page = page
        self._evidence_mode = evidence_mode

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb) -> None:
        if self._evidence_mode == "fail" and exc_type is None:
            return
        try:
            screenshot = self._page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    RUN_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    config.option.allure_report_dir = str(ALLURE_RESULTS_DIR)


@pytest.fixture
def app(page: Page) -> Application:
    return Application(page, CONFIG["base_url"])


@pytest.fixture
def new_user() -> dict[str, str]:
    template = read_csv("registration.csv")[0]
    return build_unique_user(template)


@pytest.fixture
def registered_user(new_user: dict[str, str]) -> Generator[dict[str, str], None, None]:
    """Creates a user via API (instant) instead of the slow UI registration flow."""
    create_user(new_user)
    yield new_user
    delete_user(new_user["email"], new_user["password"])


@pytest.fixture(autouse=True)
def configure_page(page: Page) -> None:
    page.set_default_timeout(CONFIG["timeouts"]["default"])
    page.set_default_navigation_timeout(CONFIG["timeouts"]["navigation"])
    close_ad = page.get_by_text("Close", exact=True)
    page.add_locator_handler(close_ad, lambda locator: locator.click())


@pytest.fixture(autouse=True)
def step_screenshots(page: Page, configure_page) -> Generator[None, None, None]:
    """Registers the per-step screenshot plugin. Depends on configure_page to ensure
    page timeout is set before any screenshot attempt."""
    evidence_mode = CONFIG["artifacts"]["evidence"]
    plugin = StepScreenshotPlugin(page, evidence_mode)
    allure_commons.plugin_manager.register(plugin)
    yield
    allure_commons.plugin_manager.unregister(plugin)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def capture_artifacts(
    page: Page,
    context,
    request,
    configure_page,
    step_screenshots,
) -> Generator[None, None, None]:
    """Handles Playwright tracing. Depends on configure_page and step_screenshots
    to guarantee execution order: configure → screenshot plugin → tracing."""
    trace_mode = CONFIG["artifacts"]["trace"]

    if trace_mode != "none":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    setup_report = getattr(request.node, "rep_setup", None)
    call_report = getattr(request.node, "rep_call", None)

    test_failed = any(
        report is not None and report.failed for report in (setup_report, call_report)
    )

    save_trace = trace_mode == "all" or (trace_mode == "fail" and test_failed)

    if trace_mode != "none":
        if save_trace:
            TRACE_DIR.mkdir(parents=True, exist_ok=True)
            trace_path = TRACE_DIR / f"{request.node.name}.zip"
            context.tracing.stop(path=str(trace_path))
            allure.attach.file(
                trace_path,
                name="Playwright Trace",
                attachment_type="application/zip",
            )
        else:
            context.tracing.stop()
