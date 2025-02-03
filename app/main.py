from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import httpx  # Using httpx for asynchronous HTTP calls
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from app.utils import NumberAnalyzer

load_dotenv()

app = FastAPI()

# Optimized CORS configuration (remains the same for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, consider restricting this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Greeting(BaseModel):
    message: str


@app.get("/", response_model=Greeting)
async def read_root():
    return Greeting(message="Hello, welcome to the FastAPI app!")


@app.get("/api/classify-number", status_code=status.HTTP_200_OK)
async def classify_number(number: str, response: Response):
    # Robust input validation using try/except rather than isdigit()
    try:
        n = int(number)
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "number": "alphabet",
            "error": True
        }

    # Use asynchronous HTTP client for non-blocking I/O
    numbers_api_url = os.getenv('NumbersAPI_URL').format(n)
    async with httpx.AsyncClient() as client:
        result = await client.get(numbers_api_url, headers={"Content-Type": "application/json"})

    # If external API fails, forward the error code
    if result.status_code != status.HTTP_200_OK:
        response.status_code = result.status_code
        return {
            "number": n,
            "error": True
        }

    # Perform local analysis
    analysis_result = NumberAnalyzer(n).result

    # Construct properties list: add "armstrong" if applicable
    properties = []
    if analysis_result.get("armstrong"):
        properties.append("armstrong")
    # Always include parity ("odd" or "even") – simplified below
    properties.append("even" if n % 2 == 0 else "odd")

    return {
        "number": n,
        "is_prime": analysis_result.get("prime"),
        "is_perfect": analysis_result.get("perfect"),
        "properties": properties,
        "digit_sum": analysis_result.get("digit_sum"),
        "fun_fact": result.json().get("text")
    }


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)
