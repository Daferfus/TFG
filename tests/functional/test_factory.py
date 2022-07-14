def test_home_page_with_fixture(test_client):
    response = test_client.get('/hello')
    assert response.data == b'Hello, World!'