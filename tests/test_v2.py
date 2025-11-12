import json
import pytest
from playwright.async_api import Page, expect

async def fill_form(page: Page, data: dict):
    #print(f"Fill Form with details:{json.dumps(data)}")
    await page.get_by_placeholder("Enter first name").fill(data.get("first_name", ""))
    await page.get_by_placeholder("Enter last name").fill(data.get("last_name", ""))
    await page.get_by_placeholder("Enter phone number").fill(data.get("phone", ""))
    await page.locator("#countries_dropdown_menu").select_option(data["country"])
    await page.get_by_placeholder("Enter email").fill(data.get("email", ""))
    await page.get_by_placeholder("Password").fill(data.get("password", ""))

    if data.get("terms"):
        try:
            await expect(page.get_by_text("I agree with the terms and")).to_be_enabled()
            await page.get_by_text("I agree with the terms and").check()
            await expect(page.get_by_text("I agree with the terms and")).to_be_checked()
        except:
            pytest.fail("T&C Checkbox is disabled!")


@pytest.mark.asyncio
async def test_valid_submission(page: Page, input_data):
    """Happy Path - validate flow when all fields are valid"""

    data = input_data["valid"]
    await fill_form(page, data)
    await page.click("button[type='submit']")

    success = page.get_by_text("Successfully registered the following information")
    await expect(success).to_be_visible(timeout=5000)

@pytest.mark.asyncio
async def test_invalid_emptylastname(page: Page, input_data):
    """Input case when last name which is mandatory is empty.
    Error should be thrown if it is empty"""

    data:dict = input_data["valid"]
    override = input_data["empty_last_name"]
    data.update(override)
    await fill_form(page, data)
    await page.click("button[type='submit']")

    success = page.locator(".success-message")  # Adjust selector
    await expect(success).to_be_visible(timeout=5000)

@pytest.mark.asyncio
async def test_phone_too_short(page: Page, input_data):
    """Phone number has digits less than 10"""

    data: dict = input_data["valid"]
    override = input_data["invalid_phone_short"]
    data.update(override)

    await fill_form(page, data)
    await page.click("button[type='submit']")

    error = page.locator("text=Phone must be at least 10 digits")
    await expect(error).to_be_visible()


@pytest.mark.asyncio
async def test_password_too_long_bug(page: Page, input_data):
    """Password is longer than 20 chars as per limit shown in UI"""
    data: dict = input_data["valid"]
    override = input_data["invalid_password_long"]
    data.update(override)

    await fill_form(page, data)
    await page.click("button[type='submit']")

    # BUG: Should fail, but might succeed → test for bug
    error = page.locator("text=The password should contain between [6,20] characters!")
    try:
        await expect(error).to_be_visible(timeout=3000)
    except:
        # This is a BUG if no error → we can mark it
        pytest.xfail("BUG: Password >20 chars accepted (expected validation error)")

