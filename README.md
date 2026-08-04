# AI Customer Request & Implementation Workflow

A FastAPI portfolio project for tracking customer requests from intake through implementation.

## Local setup:
1. Create local environment: 
```bash
python3 -m venv .venv
```
2. Activate Local Environment:
```bash
source .venv/bin/activate
```
3. Install requirements.txt: 
```bash
pip install -r requirements.txt
```

## Run the application:
```bash
uvicorn app.main:app --reload
```
Health check: http://127.0.0.1:8000/health
Interactive API docs: http://127.0.0.1:8000/docs

## Run the tests:
```bash
python -m pytest
```