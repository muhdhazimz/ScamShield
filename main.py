import uvicorn
from vers import version
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import pipeline
import re

TAGS_METADATA: List[dict] = [
    {
        "name": "Detect Scam",
        "description": (
            "This API provides an endpoint for detecting scam messages. It uses a transformer-based model "
            "to classify whether a given text is related to a scam or legitimate content."
        ),
    }
]

app = FastAPI(
    debug=False,
    title="Scam Detection API",
    summary="An API for detecting scam messages in user input.",
    description="""
    The **Scam Detection API** is designed to classify text messages as either scam or legitimate. 
    This API utilizes a transformer-based model to predict whether the text is related to fraudulent content or legitimate communication.

    ### Key Features:
    - **Scam Detection**: Classify user-submitted messages as either "Scam" or "Legitimate".
    - **Text Cleaning**: The API includes automatic cleaning of input text to remove unnecessary characters and URLs before classification.

    This API can be used to integrate scam detection capabilities into any application or service requiring content moderation.
    """,
    version=version,
    openapi_tags=TAGS_METADATA,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "*",
    ],
)

classifier = pipeline("text-classification", model="scamdetect_model")


# Function for data cleaning
def clean_text(text):
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


# Define the API endpoint
@app.post("/classify")
def classify_text(input: str):
    cleaned_text = clean_text(input)
    result = classifier(cleaned_text)
    return {"label": result[0]["label"], "score": result[0]["score"]}


@app.get("/healthz", response_class=JSONResponse)
def healthz():
    """
    Health check endpoint to verify the application's status.
    Returns a 200 OK status with a message if the app is healthy.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        h11_max_incomplete_event_size=5000000000,
        timeout_keep_alive=10,
    )
