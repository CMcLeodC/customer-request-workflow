from fastapi import FastAPI, Depends, HTTPException
from app.schemas.customer_request import (
    CustomerRequestCreate,
    CustomerRequestRead,
    CustomerRequestStatusUpdate
)
from app.schemas.request_analysis import RequestAnalysisRead
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.customer_request import CustomerRequest
from app.models.request_analysis import RequestAnalysis
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


ALLOWED_STATUS_TRANSITIONS = {
    "new": {"reviewing", "rejected"},
    "reviewing": {"approved", "rejected"},
    "approved": {"in_progress"},
    "in_progress": {"completed"},
    "completed": set(),
    "rejected": set()
}


@app.patch("/requests/{request_id}", response_model=CustomerRequestRead)
def update_customer_request_status(
    request_id: int,
    status_update: CustomerRequestStatusUpdate,
    db: Session = Depends(get_db),
):
    db_request = db.get(CustomerRequest, request_id)

    if db_request is None:
        raise HTTPException(
            status_code=404,
            detail="Customer request not found",
        )

    current_status = db_request.status
    allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(current_status, set())

    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Cannot change status from "
                f"{current_status} to {status_update.status}"
            ),
        )

    db_request.status = status_update.status

    db.commit()
    db.refresh(db_request)
    return db_request


@app.post(
    "/requests/{request_id}/analysis",
    status_code=201,
    response_model=RequestAnalysisRead,
)
def analyse_customer_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    db_request = db.get(CustomerRequest, request_id)

    if db_request is None:
        raise HTTPException(
            status_code=404,
            detail="Customer request not found",
        )

    existing_analysis = db.scalar(
        select(RequestAnalysis).where(
            RequestAnalysis.customer_request_id == request_id
        )
    )

    if existing_analysis is not None:
        raise HTTPException(
            status_code=409,
            detail="Request analysis already exists",
        )

    analysis = RequestAnalysis(
        customer_request_id=db_request.id,
        summary=db_request.request_text,
        category="other",
        suggested_urgency=db_request.urgency,
        implementation_notes="Manual review required",
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis