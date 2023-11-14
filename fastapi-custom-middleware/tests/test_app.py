import time
from fastapi.testclient import TestClient
from fastapi_custom_middleware.app import app
from http import HTTPStatus

client = TestClient(app)

ENDPOINTS = ["/info", "/v2/info"]

def test_add_timestamp_header_to_each_response():
    timestamp = 1699973537

    for endpoint in ENDPOINTS:
        response = client.get(f"{endpoint}?timestamp={timestamp}")

        assert response.status_code == HTTPStatus.OK
        assert response.headers["X-Timestamp"] == str(timestamp)

def test_add_current_timestamp_to_each_request_if_missing():
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)

        assert response.status_code == HTTPStatus.OK
        
        # TODO: mock time.time()
        assert response.headers["X-Timestamp"] == str(int(time.time()))


def test_rate_limiting_middleware():
    pass