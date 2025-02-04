from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
import httpx  # Async HTTP client to avoid blocking I/O
from math import isqrt
import uvicorn

app = FastAPI()

# Enable CORS for all origins (adjust allowed origins for production as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Utility Functions
# ----------------------------

def is_even(num: int) -> bool:
    """Return True if the number is even."""
    return num % 2 == 0


def is_perfect(num: int) -> bool:
    """
    Check if a number is a perfect square.
    (Note: Only non-negative numbers can be perfect squares.)
    """
    if num < 0:
        return False
    root = isqrt(num)
    return root * root == num


def is_prime(num: int) -> bool:
    """Return True if the number is prime."""
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def digit_sum(num: int) -> int:
    """Return the sum of the digits of the absolute value of the number."""
    return sum(int(digit) for digit in str(abs(num)))


def is_armstrong(num: int) -> bool:
    """Return True if the number is an Armstrong number."""
    abs_num = abs(num)
    digits = str(abs_num)
    power = len(digits)
    return abs_num == sum(int(digit) ** power for digit in digits)


async def get_fact(num: int, fact_type: str = "math") -> str:
    """
    Asynchronously fetch a fun fact about the number from Numbers API.

    Allowed fact_type values: "math", "trivial", "year", "date".
    Returns a fallback message if the call fails.
    """
    if fact_type not in ["math", "trivial", "year", "date"]:
        return "Unsupported fact type."
    url = f"http://numbersapi.com/{num}/{fact_type}?json"
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                return data.get("text", "No fun fact available.")
            else:
                return "No fun fact available."
        except httpx.RequestError:
            return "No fun fact available."


# ----------------------------
# Endpoints
# ----------------------------

@app.get("/")
async def root():
    """Root endpoint: returns a welcome message."""
    return {"message": "WELCOME TO HNG-12 Stage 1 Root"}


@app.get("/api/")
async def api_root():
    """API root endpoint: returns a welcome message."""
    return {"message": "WELCOME TO HNG-12 Stage 1 API Root"}


@app.get("/api/classify-number")
async def classify_number_endpoint(number: str, response: Response):
    """
    Classifies the provided number and returns:
      - Whether it is prime.
      - Whether it is a perfect square.
      - The sum of its digits.
      - Its properties: parity (even/odd) and Armstrong (if applicable).
      - A fun fact fetched asynchronously from the Numbers API.

    If the provided 'number' cannot be converted to an integer, returns a 400 error.
    """
    try:
        num = int(number)
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "number": 'alphabet',
            "error": True,
        }

    # Build the properties list
    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    properties.append("even" if is_even(num) else "odd")
    if is_perfect(num):
        properties.append("perfect square")

    # Fetch the fun fact asynchronously
    fun_fact = await get_fact(num, fact_type="math")

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "digit_sum": digit_sum(num),
        "properties": properties,
        "fun_fact": fun_fact
    }


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)
