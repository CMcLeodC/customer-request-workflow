from fastapi import FastAPI
from app.schemas.customer_request import CustomerRequestCreate

app = FastAPI(title="Customer Request Workflow")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/requests", status_code=201)
def create_customer_request(request: CustomerRequestCreate):
    return request
