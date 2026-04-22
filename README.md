# Smart Coach Recommendation

A simple full-stack demo that recommends coaches based on athlete filters and personalized preferences.

## Tech Stack
- React frontend
- FastAPI backend
- CSV-based mock data

## Project Structure
- `frontend/` — React app
- `src/` — FastAPI backend and matching logic
- `data/` — mock coach data
- `docs/` — project notes and walkthrough docs

## Requirements
Make sure you have:
- Python installed
- Node.js and npm installed

## Setup and Run
```bash
pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
uvicorn src.api:app --host 127.0.0.1 --port 8000
