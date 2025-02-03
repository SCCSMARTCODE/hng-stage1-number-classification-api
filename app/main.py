from fastapi import FastAPI, Response, status
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.utils import NumberAnalyzer

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def root(number: str, response: Response):
    if not number.isdigit():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "number": "alphabet",
            "error": True
        }

    headers = {"Content-Type": "application/json"}
    result = requests.get(os.getenv('NumbersAPI_URL').format(number), headers=headers)
    if result.status_code == status.HTTP_200_OK:

        analysis_result = NumberAnalyzer(int(number)).result

        properties = [analysis_result.get("type")]
        if analysis_result.get("armstrong"):
            properties.insert(0, "armstrong")

        return {
                "number": int(number),
                "is_prime": analysis_result.get("prime"),
                "is_perfect": analysis_result.get("perfect"),
                "properties": properties,
                "digit_sum": analysis_result.get("digit_sum"),
                "fun_fact": result.json().get('text')
            }

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)