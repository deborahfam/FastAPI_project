from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import List
import redis
import os

app = FastAPI()
cache = redis.from_url(os.environ.get('REDIS','redis://localhost:6379'))

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Order(BaseModel):
    id: int
    item: str
    quantity: int
    price: float
    status: str
    
    @validator('price')
    def price_not_negative(cls, v):
        if v < 0:
            raise ValueError('must be greater than or equal to 0')
        return v
    
    @validator('status')
    def validate_status(cls, status):
        if status not in ['completed', 'pending', 'canceled', 'all']:
            raise ValueError('Invalid status. Must be "completed", "pending", or "canceled".')
        return status

class SolutionInput(BaseModel):
    orders: List[Order]
    criterion: str

@app.post("/solution")
async def process_orders_endpoint(input_data: SolutionInput):
    # Check if the result is already cached
    cache_key = str(input_data)
    cached_result = cache.get(cache_key)
    if cached_result:
        result = float(cached_result.decode('utf-8'))
    else:
        # Compute the result using the process_orders function
        result = process_orders(input_data.orders, input_data.criterion)
        # Cache the result for future use
        cache.set(cache_key, str(result).encode('utf-8'))

    return result

def process_orders(orders: List[Order], criterion: str) -> float:
    #if criterion not in ['completed', 'pending', 'canceled', 'all']:
    #    raise ValueError("Invalid criterion. Must be 'completed', 'pending' or 'canceled'.")
    filtered_orders = []
    for order in orders:
        if criterion == 'all' or order.status == criterion:
            filtered_orders.append(order)
    total_revenue = sum([order.quantity * order.price for order in filtered_orders])
    return total_revenue
