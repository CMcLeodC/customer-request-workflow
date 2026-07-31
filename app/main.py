from fastapi import FastAPI

app = FastAPI(title="Customer Request Workflow")


@app.get("/health")
def health_check():
    return {"status": "ok"}
