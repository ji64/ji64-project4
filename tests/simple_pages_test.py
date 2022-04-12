"""This tests the pages"""

def base_request_test(client):
    """This tests that base.html is accessible"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data
