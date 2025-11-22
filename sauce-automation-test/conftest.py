import json
import os
import datetime
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=None)
    parser.addoption("--browser", action="store", default=None, choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="session")
def config(pytestconfig):
    with open(os.path.join(pytestconfig.rootpath, "sauce-automation-test", "config.json")) as f:
        cfg = json.load(f)
    base_url = pytestconfig.getoption("base_url") or cfg.get("base_url")
    browser = pytestconfig.getoption("browser") or cfg.get("browser")
    headless = pytestconfig.getoption("headless") or cfg.get("headless")
    implicit_wait = cfg.get("implicit_wait", 5)
    timeout = cfg.get("timeout", 10)
    return {"base_url": base_url, "browser": browser, "headless": headless, "implicit_wait": implicit_wait, "timeout": timeout}


@pytest.fixture(scope="session")
def screenshots_dir(pytestconfig):
    dir_path = os.path.join(pytestconfig.rootpath, "sauce-automation-test", "reports", "screenshots")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


@pytest.fixture(scope="function")
def driver(config):
    logging.basicConfig(level=logging.INFO)
    if config["browser"] == "firefox":
        options = FirefoxOptions()
        if config["headless"]:
            options.add_argument("-headless")
        drv = webdriver.Firefox(options=options)
    else:
        options = ChromeOptions()
        if config["headless"]:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(config["implicit_wait"])
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call":
        return
    if rep.failed:
        drv = item.funcargs.get("driver")
        screenshots_dir = item.session.config._screenshots_dir if hasattr(item.session.config, "_screenshots_dir") else None
        if not screenshots_dir:
            screenshots_dir = os.path.join(item.session.config.rootpath, "sauce-automation-test", "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
        if drv:
            ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            fname = f"{item.name}-{ts}.png"
            path = os.path.join(screenshots_dir, fname)
            try:
                drv.save_screenshot(path)
            except Exception:
                path = None
            plugin = item.config.pluginmanager.getplugin("html")
            if plugin and path:
                extra = getattr(rep, "extra", [])
                extra.append(plugin.extras.image(path))
                rep.extra = extra


def pytest_configure(config):
    screenshots_dir = os.path.join(config.rootpath, "sauce-automation-test", "reports", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    config._screenshots_dir = screenshots_dir