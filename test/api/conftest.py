import pytest

from fastapi.testclient import TestClient

from app import app
import pypendency.models.graph as pmg
from pypendency.models.generics import BaseNode


@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def client (test_client, prepared_container):
    return client
