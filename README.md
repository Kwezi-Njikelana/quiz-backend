# Fast API

A minimal FastAPI application.

## Prerequisites

- Python 3.13 or newer
- Git
- A terminal or command prompt

## Clone the repository

```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd fast-api
```

## Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install dependencies

This project is managed with `uv` and uses `pyproject.toml` + `uv.lock`.

```bash
python -m pip install --upgrade pip
python -m pip install uv
uv install
```

If `uv` is already installed, just run:

```bash
uv install
```

## Run the app locally

```bash
uvicorn main:app --reload
```

Open your browser and visit:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs` for Swagger UI
- `http://127.0.0.1:8000/redoc` for ReDoc

## Notes

- If your app requires a PostgreSQL database, ensure the database is running and update the connection settings in `database.py`.
- Use `deactivate` to exit the virtual environment.
