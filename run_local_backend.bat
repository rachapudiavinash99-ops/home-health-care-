@echo off
echo Starting Healthcare Backend locally with SQLite...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt aiosqlite python-dotenv email-validator pydantic[email] --upgrade
alembic upgrade head
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
