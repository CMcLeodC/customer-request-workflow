from fastapi import FastAPI, Depends
from app.schemas.customer_request import (
    CustomerRequestCreate,
    CustomerRequestRead,
)
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.customer_request import CustomerRequest

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Request Workflow")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/requests", status_code=201, response_model=CustomerRequestRead)
def create_customer_request(
    request: CustomerRequestCreate,
    db: Session = Depends(get_db),
):
    db_request = CustomerRequest(**request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request