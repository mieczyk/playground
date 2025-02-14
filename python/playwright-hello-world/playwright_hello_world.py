import argparse
import sys

# Playwright supports async version as well.
from playwright.sync_api import sync_playwright

TARGET_URL = "https://projekty.muratordom.pl/"

SUPPORTED_BROWSERS = ["webkit", "chromium", "firefox"]
SUPPORTED_BROWSERS_INFO = str.join("|", SUPPORTED_BROWSERS)

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(
        description="""Very simple example of the 'playwright' lib usage. 
        It visits the 'projekty.muratordom.pl' page and adds first project to the shopping cart."""
    )
    # Playwright's engine browser must be installed first:
    # `python -m playwright install`
    args_parser.add_argument(
        "browser", help=f"Playwright's browser engine: {SUPPORTED_BROWSERS_INFO}."
    )
    args = args_parser.parse_args()

    sanitized_browser_engine_name = args.browser.strip().lower()

    if sanitized_browser_engine_name not in SUPPORTED_BROWSERS:
        print(f"Invalid browser name. Supported browsers: {SUPPORTED_BROWSERS_INFO}")
        sys.exit(1)

    with sync_playwright() as playwright:
        engine = getattr(playwright, sanitized_browser_engine_name)
        # If headless=True (defaul), no browser UI is visible.
        browser = engine.launch(headless=False)
        # Create a new isolated context.
        # It won't share cookies/cache with other browser contexts.
        context = browser.new_context()

        page = context.new_page()
        page.goto(TARGET_URL)

        # Accept cookies consent if the popup is visible.
        accept_button = page.locator("button", has_text="Akceptuj")
        if accept_button.is_visible():
            accept_button.click()

        # Make the link to projects list visible.
        top_menu_link = (
            page.locator("css=li.menu-element")
            .get_by_role("link")
            .and_(page.get_by_text("Projekty domów"))
        )
        top_menu_link.hover()

        # The `has_text` parameter searches for a substring (case-insensitive).
        # >>> page.locator("a", has_text="substring")
        # If the exact matching is needed, we can use the XPath locator.
        #   normalize-space -> XPath function that strips leading and trailing white-space characters.
        projects_link = page.locator(
            "xpath=//a[normalize-space(text())='Projekty domów parterowych']"
        )
        projects_link.click()

        # Go to the first project on the list.
        first_project_teaser = (
            page.locator("css=div.filters-results__container__slots")
            .locator("css=div.filters_result_teaser")
            .first
        )
        first_project_link = first_project_teaser.get_by_role("link").first
        first_project_link.click()

        context.close()
        browser.close()
