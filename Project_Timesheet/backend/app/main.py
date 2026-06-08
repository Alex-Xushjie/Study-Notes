from fastapi import FastAPI

from app.database import Base, engine
from app import models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Timesheet System API")


@app.get("/")
def read_root():
    return {
        "message": "Timesheet API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/db-test")
def db_test():
    return {
        "message": "Database connection is ready"
    }