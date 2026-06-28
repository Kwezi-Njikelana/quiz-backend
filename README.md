# Quiz Backend

A compact FastAPI backend for storing quiz questions and their answer choices. The
API exposes CRUD endpoints for questions, keeps choices linked to each question,
and stores data in a SQL database through SQLAlchemy.

## What It Does

- Create quiz questions with multiple answer choices
- Mark one or more choices as correct
- Read all questions or a single question by ID
- Read choices for a question
- Update a question and replace its choices
- Delete a question
- Serve interactive API docs through FastAPI

## Tech Stack

| Layer | Tooling |
| --- | --- |
| API | FastAPI |
| Database ORM | SQLAlchemy |
| Validation | Pydantic |
| Database driver | psycopg2 |
| Environment config | python-dotenv |
| Package management | uv |

## Project Structure

```text
.
|-- database.py      # Database engine, session, and SQLAlchemy base
|-- main.py          # FastAPI app, CORS, schemas, and routes
|-- models.py        # SQLAlchemy models for questions and choices
|-- pyproject.toml   # Project metadata and dependencies
|-- uv.lock          # Locked dependency versions
`-- README.md
```

## Prerequisites

- Python 3.13 or newer
- PostgreSQL, or another SQLAlchemy-compatible database configured through
  `DATABASE_URL`
- `uv` for dependency management

Install `uv` if you do not already have it:

```bash
python -m pip install --upgrade pip
python -m pip install uv
```

## Getting Started

Clone the project and enter the app directory:

```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd quiz-backend
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/quiz_db
```

Start the API:

```bash
uv run uvicorn main:app --reload
```

The app will be available at:

- API docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

The database tables are created automatically when the app starts.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/questions` | Get all questions |
| `GET` | `/questions/{question_id}` | Get one question by ID |
| `POST` | `/questions` | Create a question and its choices |
| `PUT` | `/questions/{question_id}` | Update a question and replace its choices |
| `DELETE` | `/questions/{question_id}` | Delete a question |
| `GET` | `/choices/{question_id}` | Get choices for a question |

## Request Examples

Create a question:

```bash
curl -X POST http://127.0.0.1:8000/questions \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "What is the capital city of South Africa?",
    "choices": [
      { "choice_text": "Pretoria", "is_correct": true },
      { "choice_text": "Cape Town", "is_correct": false },
      { "choice_text": "Johannesburg", "is_correct": false },
      { "choice_text": "Durban", "is_correct": false }
    ]
  }'
```

Get all questions:

```bash
curl http://127.0.0.1:8000/questions
```

Get choices for a question:

```bash
curl http://127.0.0.1:8000/choices/1
```

Update a question:

```bash
curl -X PUT http://127.0.0.1:8000/questions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Which city is South Africa's administrative capital?",
    "choices": [
      { "choice_text": "Pretoria", "is_correct": true },
      { "choice_text": "Bloemfontein", "is_correct": false },
      { "choice_text": "Cape Town", "is_correct": false }
    ]
  }'
```

Delete a question:

```bash
curl -X DELETE http://127.0.0.1:8000/questions/1
```

## CORS

The backend currently allows requests from:

- `http://localhost:5173`
- `http://localhost:3000`

These origins are configured in `main.py`.

## Notes

- `DATABASE_URL` is required because `database.py` creates the SQLAlchemy engine
  from that environment variable.
- The FastAPI app is configured with `root_path="/api"` for deployments that sit
  behind a reverse proxy or API gateway.
- There is no authentication layer yet, so keep this API behind trusted network
  boundaries until auth is added.
