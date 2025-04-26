# Audio to Text Microservice

A FastAPI microservice that transcribes audio files into text using Faster-Whisper ASR models.
Developed and tested with **Python 3.11**.

## 📂 Database Choice

This project currently uses **SQLite** for simplicity and fast local development.

- SQLite is lightweight and requires no server setup.
- Switching to **PostgreSQL** is very easy:
  - Update the `DATABASE_URL` in `.env`:
    ```
    DATABASE_URL=postgresql+psycopg2://user:password@hostname:port/database_name
    ```
  - SQLAlchemy will automatically connect to the new database.
  
- I used SQLite initially for fast prototyping, but designed the project to easily switch to PostgreSQL or any relational database using SQLAlchemy.

## Features

- Upload an audio file to `/analyze` and get back:
  - Transcribed text
  - Audio duration
  - Processing time
- `/stats` endpoint to get:
  - Total API calls
  - Median processing time
  - Median audio length
- Uses SQLite for storing transcriptions
- Fully dockerized for easy deployment
- Unit tested with pytest

## Setup Locally

1. Clone the repo:
   ```
    git clone https://github.com/yourusername/audio-analytics.git
    cd audio-analytics
    ```
   
2. Create and activate a virtual environment:
    ```
    uv venv
    source .venv/bin/activate
    ```

3. Install project dependencies:
    ```
    uv sync
    ```

4. Run the application:
    ```
    uvicorn app.main:app --reload
    ```
Server will be running at `http://127.0.0.1:8000`

## Testing the API (Swagger UI)

Once the app is running, you can test it using **Swagger UI**:

- Open your browser and go to:
`http://127.0.0.1:8000/docs`
- You will see an interactive API documentation.
- You can:
  - Upload an audio file to `/analyze`
  - Call `/stats` to view transcription statistics

## Running with Docker

1. Build the Docker image:
    ```
    docker build -t audio-analytics .
    ```
2. Run the Docker container:
    ```
    docker run -p 8000:8000 audio-analytics
    ```
App will be available at `http://localhost:8000`

It can be still tested via Swagger UI at:
`http://localhost:8000/docs`


## Running Tests

Run unit and functional tests with coverage:
    ```
    pytest --cov=app tests/
    ```
Coverage report will be printed in the terminal after tests.


## API Endpoints

| Method | Endpoint  | Description                         |
|:-------|:----------|:------------------------------------|
| POST   | `/analyze` | Upload audio file and get transcription |
| GET    | `/stats`   | Get statistics on transcriptions     |


## Note About .env File

- For demonstration purposes, the .env file is included in the repository.

- This is not a recommended best practice for production projects.

- In a real-world application, sensitive files like .env should be excluded (via .gitignore) to prevent exposing credentials.

- This .env file does not contain any sensitive information or credentials — only a local DATABASE_URL for SQLite testing.

- This is provided to make local setup and testing easier for reviewers and developers.