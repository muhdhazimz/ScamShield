# Scam Detection API and Streamlit UI

## Overview

This repository provides a **Scam Detection API** built using **FastAPI** for detecting scam messages, and a **Streamlit UI** to interact with the API. The model used for scam detection is a fine-tuned transformer-based **distilbert-base-uncased** model. 

### Key Features
- **Scam Detection API**: Classifies messages as either "Scam" or "Legitimate" using a fine-tuned **DistilBERT** model.
- **Streamlit Interface**: Provides an easy-to-use interface to interact with the scam detection model.
- **Docker Support**: Easily deploy the API and the UI using Docker.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/muhdhazimz/ScamShield.git
    ```

2. Navigate into the project directory:
    ```bash
    cd ScamShield
    ```

3. Install required dependencies (optional if running via Docker):
    ```bash
    pip install -r requirements.txt
    ```

## Prerequisites

- **Python 3.11 or later**

## Usage

### Running with Docker Compose

1. **Build and start both services** (FastAPI and Streamlit):
    ```bash
    docker-compose build
    docker-compose up
    ```

2. This will:
    - Build the FastAPI API container (using `main.py`).
    - Build the Streamlit container (using `streamlit/Dockerfile`).
    - Start both services and make them available at:
      - FastAPI API: `http://localhost:8000/docs`
      - Streamlit UI: `http://localhost:8501`

### Running the API (FastAPI) Independently using Docker

1. **Build and run the FastAPI** (using `Dockerfile`):
    ```bash
    docker build -t fastapi-app -f Dockerfile .
    docker run -p 8000:8000 fastapi-app
    ```

2. Alternatively, you can run the FastAPI service using `uvicorn`:
    ```bash
    python3 main.py
    ```

3. The FastAPI API will be accessible at:
    - API Documentation: `http://localhost:8000/docs`

### Running Streamlit Independently

1. **Start the FastAPI server** (make sure FastAPI is running on `localhost:8000`):
    ```bash
    python3 main.py
    ```

2. **Run the Streamlit application**:
    - Navigate to the `streamlit` folder:
      ```bash
      cd streamlit
      ```
    - Run the Streamlit app:
      ```bash
      streamlit run app.py
      ```

3. The Streamlit UI will be accessible at:
    - `http://localhost:8501`

### Fine Tuning the Model Locally

If you wish to fine-tune the model or use the model independently:

1. You can start training the model using the provided Jupyter notebook `fine_tuning_model.ipynb`.

2. After fine-tuning, the model will be saved into the `scamdetect_model/` folder.

## API Endpoints

### Classify Text

- **POST** `/classify`
  - Classifies a given message as "Scam" or "Legitimate".

  **Request Body**:
  ```json
  {
    "input": "Your message here"
  }

    ```

### Report
For a detailed report on fine tuning the model, data preprocessing, and evaluation, please refer to (REPORT.md).

### Project Structure

```
./
│ 
├── scamdetect_model/
│   ├── config.json
│   ├── model.safetensors
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   ├── training_args.bin
│   └── vocab.txt
│
├── streamlit/
│   │
│   ├── app.py
│   ├── data.db
│   └── Dockerfile
│
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── Dockerfile
├── README.md
├── docker-compose.yaml
├── main.py
├── requirements.txt
├── fine_tune_model.ipynb
├── sms_scam_detection_dataset_merged_with_lang.csv
└── vers.py
```