import time

from http import HTTPStatus
from unittest import mock

from fastapi.testclient import TestClient

from fastapi_custom_middleware.app import app

client = TestClient(app)

ENDPOINTS = ["/info", "/v2/info"]


def test_add_timestamp_header_to_each_response():
    timestamp = 1699973537

    for endpoint in ENDPOINTS:
        response = client.get(f"{endpoint}?timestamp={timestamp}")

        assert response.status_code == HTTPStatus.OK
        assert response.headers["X-Timestamp"] == str(timestamp)


@mock.patch("time.time", mock.MagicMock(return_value=1699973555))
def test_add_current_timestamp_to_each_request_if_missing():
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)

        assert response.status_code == HTTPStatus.OK
        assert response.headers["X-Timestamp"] == "1699973555"


def test_rate_limiting_middleware():
    # Make sure requests from previous tests won't be taken into rate limit calculations.
    time.sleep(1) 

    for _ in range(0, 10):
        response = client.get(ENDPOINTS[0])
        assert response.status_code == HTTPStatus.OK
    
    response = client.get(ENDPOINTS[0])
    assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS