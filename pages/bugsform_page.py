import re
from playwright.async_api import Page, expect

class BugsFormPage(object):
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.url = f"{base_url}/bugs-form"

    async def load(self):
        await self.page.goto(self.url)

        
