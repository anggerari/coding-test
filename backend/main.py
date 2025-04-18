from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
import uvicorn
import json
import os
from typing import Any, Dict, Optional

app = FastAPI(
    title="Salesperson Dashborad API [coding-test]",
    description="This is an API for testing dummy data and AI placeholder logic.",
    version="1.0.0",
)

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
DUMMY_DATA_PATH = os.path.join(os.path.dirname(__file__), "../dummyData.json")


def load_dummy_data(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load and return JSON data from the given file path.
    Returns None if the file doesn't exist or can't be parsed.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from {file_path}")
    return None


@app.get("/api/data", summary="Sales Rep Data", tags=["Dummy Data"])
def get_data() -> Dict[str, Any]:
    """
    Endpoint: GET /api/data
    Returns the contents of the dummyData.json file.
    """
    data = load_dummy_data(DUMMY_DATA_PATH)
    if data is None:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dummy data."
        )
    return data


@app.post("/api/ai", summary="Ask AI", tags=["AI"])
async def ai_endpoint(request: Request) -> Dict[str, str]:
    """
    Endpoint: POST /api/ai
    Accepts a JSON body with a 'question' field and returns a placeholder answer.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload."
        )

    user_question = body.get("question", "")
    if not user_question:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Missing 'question' in request body."
        )

    # Placeholder logic – replace this with real AI call if needed
    return {"answer": f"This is a placeholder answer to your question: {user_question}"}


if __name__ == "__main__":
    # Run the FastAPI app with hot reload (for development)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
