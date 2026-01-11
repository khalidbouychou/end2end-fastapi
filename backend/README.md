# FastAPI Backend

## Project Structure
- `app/`: Main application code
  - `api/`: API endpoints
  - `core/`: Configuration
  - `db/`: Database connection
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic schemas
- `tests/`: Tests

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run
```bash
uvicorn app.main:app --reload
```
