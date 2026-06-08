from fastapi import FastAPI

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