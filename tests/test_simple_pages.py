"""This tests the pages"""

def test_base_request(client):
    """This tests that base.html is accessible"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data
