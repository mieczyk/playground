import requests
import time
from difflib import SequenceMatcher
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

URLS = [
    "https://www.se.pl",
    "https://www.eska.pl",
    "https://muratordom.pl"
]

ORIGIN_DATACENTER = "SM"
TARGET_DATACENTER = "OVH"

# If diff ratio is below this threshold, we consider the sites' content
# as significally different.
RATIO_THRESHOLD = 90.0

def main():
    for url in URLS:
        timestamp = time.time()
        url = add_version_to_url(url, str(timestamp))

        origin_response = requests.get(
            url, headers=prepare_request_headers(ORIGIN_DATACENTER), verify=False
        )
        
        target_response = requests.get(
            "https://onet.pl", headers=prepare_request_headers(TARGET_DATACENTER), verify=False
        )

        ratio = SequenceMatcher(None, origin_response.text, target_response.text).ratio()

        if ratio < RATIO_THRESHOLD:
            print(f"[OK] {url}")
        else:
            print(f"[DIFF RATIO {ratio}] {url}")

def add_version_to_url(url: str, version: str) -> str:
    # In order to omit the server's cache.
    return f"{url}?v={version}"

def prepare_request_headers(datacenter: str) -> dict:
    return {
        f"X-{datacenter}": "yes-please"
    }

if __name__ == "__main__":
    main()