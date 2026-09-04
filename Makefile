install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

run:
	cd backend && uvicorn app.main:app --reload

build:
	cd frontend && npm run build
