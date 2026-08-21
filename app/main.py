from fastapi import FastAPI, Depends, HTTPException
from app.schemas.customer_request import (
    CustomerRequestCreate,
    CustomerRequestRead,
)
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.customer_request import CustomerRequest
from sqlalchemy import select

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


@app.get("/requests/{request_id}", response_model=CustomerRequestRead)
def get_customer_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    db_request = db.get(CustomerRequest, request_id)

    if db_request is None:
        raise HTTPException(
            status_code=404,
            detail="Customer request not found",
        )

    return db_request


@app.get("/requests", response_model=list[CustomerRequestRead])
def list_customer_requests(
    db: Session = Depends(get_db),
):
    return db.scalars(select(CustomerRequest)).all()