import pytest
from fastapi.testclient import TestClient
from app.main import app, Order, process_orders

client = TestClient(app)

def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

def test_default():
    orders_data = [{
        "id": 1, 
        "item": "Laptop",
        "quantity": 1, 
        "price": 999.99, 
        "status": "completed"
        },
    
       {
           "id": 2, 
           "item": "Smartphone", 
           "quantity": 2, 
           "price": 499.95, 
           "status": "pending"
           },
       {
           "id": 3, 
           "item": "Headphones", 
           "quantity": 3, 
           "price": 99.90, 
           "status": "completed"
           },
       {
           "id": 4, 
           "item": "Mouse", 
           "quantity": 4, 
           "price": 24.99, 
           "status": "canceled"
           }
    ]
    orders = [Order(**order_data) for order_data in orders_data]
    result = process_orders(orders, 'completed')
    assert result == 1299.69

def test_negative_price():
    order_data = {
        "id": 1,
        "item": "shoes",
        "quantity": 2,
        "price": -10.0,
        "status": "completed"
    }
    with pytest.raises(ValueError):
        Order(**order_data)

def test_invalid_status():
    order_data = {
        "id": 1,
        "item": "shoes",
        "quantity": 2,
        "price": 10.0,
        "status": "invalid"
    }
    with pytest.raises(ValueError):
        Order(**order_data)

def test_valid_price():
    order_data = {
        "id": 1,
        "item": "shoes",
        "quantity": 2,
        "price": 10.0,
        "status": "completed"
    }
    order = Order(**order_data)
    assert order.price == 10.0
    
def test_zero_price():
    order_data = {
        "id": 1,
        "item": "shoes",
        "quantity": 2,
        "price": 0.0,
        "status": "completed"
    }
    order = Order(**order_data)
    assert order.price == 0.0

def test_valid_status():
    order_data = {
        "id": 1,
        "item": "shoes",
        "quantity": 2,
        "price": 10.0,
        "status": "completed"
    }
    order = Order(**order_data)
    assert order.status == "completed"

def test_all_status():
    order_data = {
        "id": 1,
        "item": "shoes",
        "quantity": 2,
        "price": 10.0,
        "status": "all"
    }
    order = Order(**order_data)
    assert order.status == "all"

def test_process_orders():
    orders_data = [
        {
            "id": 1,
            "item": "shoes",
            "quantity": 2,
            "price": 10.0,
            "status": "completed"
        },
        {
            "id": 2,
            "item": "t-shirt",
            "quantity": 3,
            "price": 5.0,
            "status": "pending"
        },
        {
            "id": 3,
            "item": "pants",
            "quantity": 1,
            "price": 20.0,
            "status": "canceled"
        }
    ]
    orders = [Order(**order_data) for order_data in orders_data]
    result = process_orders(orders, 'completed')
    assert result == 20.0

