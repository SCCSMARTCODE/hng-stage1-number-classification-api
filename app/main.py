from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import httpx  # Using httpx for async HTTP requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from app.utils import NumberAnalyzer
import asyncio

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to known domains
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
    # Improved input validation with try/except
    try:
        n = int(number)
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "number": "alphabet",
            "error": True,
        }

    # Prepare external Numbers API URL and headers
    numbers_api_url = os.getenv("NumbersAPI_URL").format(n)
    headers = {"Content-Type": "application/json"}

    # Use async HTTP client with a timeout to avoid long blocking calls
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            result = await client.get(numbers_api_url, headers=headers)
        except httpx.RequestError as exc:
            # Return a fallback fun fact if the external API fails
            result = None

    # Check if external API call succeeded; if not, provide a fallback
    if result is None or result.status_code != status.HTTP_200_OK:
        fun_fact = "No fun fact available at the moment."
    else:
        fun_fact = result.json().get("text", "No fun fact available.")

    # Perform local analysis
    analysis_result = NumberAnalyzer(n).result

    # Build the properties list based on the analysis
    properties = []
    if analysis_result.get("armstrong"):
        properties.append("armstrong")
    properties.append("even" if n % 2 == 0 else "odd")

    return {
        "number": n,
        "is_prime": analysis_result.get("prime"),
        "is_perfect": analysis_result.get("perfect"),
        "properties": properties,
        "digit_sum": analysis_result.get("digit_sum"),
        "fun_fact": fun_fact
    }


# For local testing; ensure you deploy appropriately to Vercel
if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)
