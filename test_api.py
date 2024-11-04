"""importing pytest and requests to test endpoints"""
import requests
import pytest

VERSION_ENDPOINT='http://127.0.0.1:8000/version'
TEMPERATURE_ENDPOINT='http://127.0.0.1:8000/temperature'

def test_get_version():
    """testing version endpoint"""
    response = requests.get(VERSION_ENDPOINT,timeout=30)
    assert response.status_code==200
    print(response)

def test_get_temperature():
    """testing temperature endpoint"""
    response2 = requests.get(TEMPERATURE_ENDPOINT,timeout=30)
    assert response2.status_code==200
    print(response2)
    