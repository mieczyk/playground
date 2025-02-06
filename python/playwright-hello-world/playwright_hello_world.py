import argparse
import sys

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
        print(engine)
