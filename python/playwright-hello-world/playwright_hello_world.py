import argparse

from playwright.sync_api import sync_playwright

TARGET_URL = "https://projekty.muratordom.pl/"

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(
        description="""Very simple example of the 'playwright' lib usage. 
        It visits the 'projekty.muratordom.pl' page and adds first project to the shopping cart."""
    )

    # Playwright's engine browser must be installed first: 
    # `python -m playwright install`
    args_parser.add_argument("browser", help="Playwright's browser engine: webkit | chromium | firefox.")
    
    args = args_parser.parse_args()
    
    with sync_playwright() as playwright:
        playwright.chromium


# TODO
# 1. Możliwość wyboru 3 różnych silników z linii poleceń.
#   1.1 Parsowanie argumentu wejściowego za pomocą argparse (z prostą walidacją)
