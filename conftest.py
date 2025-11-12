import pytest
import json
from pathlib import Path
from playwright.async_api import async_playwright, Page

with open(Path(__file__).parent / "config/config.json") as f:
    conf = json.load(f)
    print(json.dumps(conf))

@pytest.fixture
def config():
        return conf

@pytest.fixture
def input_data():
    with open(Path(__file__).parent / "tests/input.json") as f:
        d =  json.load(f)
        print(json.dumps(d))
        return d

@pytest.fixture
async def playwright():
    p = await async_playwright().start()
    yield p
    await p.stop()

@pytest.fixture
async def browser(playwright):
    browser = await playwright.chromium.launch(headless=False)
    yield browser
    await browser.close()

@pytest.fixture
async def context(browser):
    context = await browser.new_context(viewport={"width": 1280, "height": 720})
    yield context
    await context.close()


@pytest.fixture
async def page(context) -> Page:
    page = await context.new_page()
    await page.goto(conf["base_url"])
    print(f"Page loaded with Base URL: {conf["base_url"]}")
    yield page
    await page.close()