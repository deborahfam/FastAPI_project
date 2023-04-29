from fastapi import FastAPI
from typing import List as List

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/solution")
async def process_orders_endpoint(data: dict):
    orders = data["orders"]
    criterion = data["criterion"]
    revenue = process_orders(orders, criterion)
    return {"revenue": revenue}

def process_orders(orders: List[dict], criterion: str) -> float:
    order_statuses = ["completed", "pending", "canceled"]

    if criterion not in order_statuses + ["all"]:
        raise ValueError(f"Invalid criterion: {criterion}. Must be one of {order_statuses} or 'all'.")

    filtered_orders = [order for order in orders if criterion == "all" or order["status"] == criterion]

    total_revenue = sum(order["quantity"] * order["price"] for order in filtered_orders)
    
    return total_revenue