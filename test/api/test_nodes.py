import fastapi
import pytest
import pytest_check as check

import requests


requests.Response.json()
router = fastapi.APIRouter(
    prefix="/nodes",
    tags=["nodes"]
)

def test_query_nodes(client):
    resp = client.get("/nodes/")
    check.is_true(200 <= resp.status_code < 300)
    res = resp.json()
    check.is_true(len(res["data"]) == 5)
    check.is_true(len(res["status"]) == 6)

@pytest.mark.parametrize(
    "node_id, want_length",
    [
        ["g1-n1", 1],
        ["xx", 1],
        ["xxyy", 0],
    ]
)
def test_query_get_node(client, node_id, want_length):
    want = "g1-n1"
    resp = client.get(f"/nodes/{want}")
    check.is_true(200 <= resp.status_code < 300)

    res = resp.json()
    check.is_true(len(res["data"]) == 1)
    check.is_true(len(res["status"]) == 6)

    if want_length:
        check.is_true(res["data"][0]["id"] == want)


def test_query_related_nodes(client):
    node_id = "g1-n1"
    resp = client.get(f"/nodes/related/{node_id}")
    check.is_true(200 <= resp.status_code < 300)
    res = resp.json()
    check.is_true(len(res["data"]) == 3)
    check.is_true(len(res["status"]) == 6)

