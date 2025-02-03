# HNG Stage 1 Number Classification API

A public API for the HNG Stage 1 Backend task. This API takes a number as a parameter, classifies its mathematical properties, calculates its digit sum, and returns a fun fact about the number using the [Numbers API](http://numbersapi.com).

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [API Specification](#api-specification)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Backlinks](#backlinks)

## Project Description

This API is designed to classify numbers based on several mathematical properties and return additional insights:
- Whether the number is prime.
- Whether the number is perfect.
- Whether the number is an Armstrong number.
- Whether the number is odd or even.
- The sum of its digits.
- A fun fact about the number (retrieved from the Numbers API).

The API is built with a focus on clean code, proper error handling, and efficient response times.

## Features

- **Number Classification:** Identifies if a number is prime, perfect, Armstrong, and its parity.
- **Digit Sum Calculation:** Computes the sum of the digits.
- **Fun Fact Integration:** Retrieves an interesting fun fact about the number from the Numbers API.
- **Input Validation:** Returns a `400 Bad Request` for invalid input.
- **CORS Enabled:** The API handles Cross-Origin Resource Sharing, ensuring accessibility from different domains.
- **JSON Responses:** All responses are returned in JSON format.

## Technologies Used

- **Programming Language/Framework:** Python with FastAPI.
- **Deployment:** Deployed to a publicly accessible endpoint.
- **Version Control:** Git & GitHub.
- **Additional Libraries:** 
  - `requests` or an equivalent HTTP client
  - `uvicorn` for serving the app.
  - Environment management using `python-dotenv`

## API Specification

### Endpoint

**GET** `/api/classify-number?number=<number>`

### Example Request

```
GET https://your-domain.com/api/classify-number?number=371
```

### Example Response (200 OK)

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Example Response (400 Bad Request)

```json
{
    "number": "alphabet",
    "error": true
}
```

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/SCCSMARTCODE/hng-stage1-number-classification-api.git
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the root directory and add `NumbersAPI_URL="http://numbersapi.com/{}"` .

5. **Run the Application:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Usage

- **Access the API Endpoint:**  
  Navigate to `http://localhost:8000/api/classify-number?number=371` in your browser or use a tool like Postman.

- **Example with cURL:**

   ```bash
   curl -X GET "http://localhost:8000/api/classify-number?number=371"
   ```


## Deployment

The API is deployed on [Your Deployment Platform] and is accessible at:  
`https://your-deployment-domain.com/api/classify-number`

Make sure to update the deployment settings as required and verify that CORS is enabled and that the response times meet the requirements (< 500ms).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bug fixes or feature enhancements.

## License

This project is licensed under the MIT License. See the LICENSE file for details

## Backlinks

- [Python Developers on HNG](https://hng.tech/hire/python-developers)
- [C# Developers on HNG](https://hng.tech/hire/csharp-developers)
- [Golang Developers on HNG](https://hng.tech/hire/golang-developers)
- [PHP Developers on HNG](https://hng.tech/hire/php-developers)
- [Java Developers on HNG](https://hng.tech/hire/java-developers)
- [Node.js Developers on HNG](https://hng.tech/hire/nodejs-developers)
