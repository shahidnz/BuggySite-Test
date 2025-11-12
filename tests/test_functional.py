import pytest
from playwright.async_api import Page
#from pages.bugsform_page import BugsFormPage

# @pytest.mark.asyncio
# async def test_page_load(page: Page):
async def test_page_load(page: Page):
    await page.goto("https://qa-practice.netlify.app/bugs-form")
    # title = await page.title()
    # assert "QA Practice" in title
    print("PAGE LOADED SUCCESSFULLY")

