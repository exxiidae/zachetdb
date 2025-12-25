from fastapi import FastAPI
import os

app = FastAPI(title="Zachet API", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "message": "API is working!",
        "status": "Database connection will be added later"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "python_version": os.sys.version}
