from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime, UTC, timezone
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=Dict[str, str])
def root():
    return {
          "email": 'os.getenv("MY_GMAIL")',
          "current_datetime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
          "github_url": 'os.getenv("PROJECT_GITHUB_URL")'
        }

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)