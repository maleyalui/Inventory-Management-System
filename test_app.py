import pytest
from unittest.mock import patch
from app import app,fetch_product_details

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
def test_get_single_item(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    
def test_add_item(client):
    payload = {"product_name": "Test Milk", "stock": 10, "price":500}
    response = client.post('/inventory', json=payload)
    assert response.status_code == 201
    assert response.json['product_name'] == "Test Milk"
    
def test_update_item(client):
    payload = {'stock': 100}
    response = client.patch('/inventory/1', json=payload)
    assert response.json['stock'] == 100
    
def test_delete_item(client):
    response = client.delete('/inventory/1')
    assert response.status_code == 200
    
@patch('app.requests.get')
def test_fetch_product_details(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product":{
            "product_name": "Mock Almond Milk",
            "brands": "MockBrand",
            "ingredients_text": "Water, almonds"
        }
    }
    result = fetch_product_details(barcode=123456)
    assert result["product_name"] == "Mock Almond Milk"