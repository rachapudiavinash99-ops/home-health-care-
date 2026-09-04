# Home Healthcare Management System

A production-style, end-to-end Home Healthcare Management System built with Python (FastAPI) and React.

## Features
- **Role-Based Access Control:** Patients, Caregivers, Doctors, Admins
- **Patient Portal:** Profiles, Care Requests, Invoices
- **Caregiver Dashboard:** Schedules, Home Visit Documentation, Vitals Logging
- **Doctor Portal:** Care Plan Generation, Prescriptions
- **Admin System:** Service Catalog, Scheduling, Dashboard Analytics

## Technology Stack
- **Backend:** Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT, Pytest
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router, Axios
- **Infrastructure:** Docker, Docker Compose, Redis

## Setup Instructions

1. **Environment Variables:**
   Copy .env.example to .env and configure your local settings.
   cp .env.example .env

2. **Docker Deployment:**
   To spin up the Postgres Database, Redis, FastAPI Backend, and React Frontend:
   docker-compose up --build -d

3. **Database Migrations:**
   Once the containers are running, execute the migrations inside the backend container:
   docker-compose exec backend alembic upgrade head

4. **Accessing the App:**
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/api/v1/openapi.json

## Testing
To run the automated test suite locally:
pytest backend/app/tests/

## Licensing
Proprietary. All rights reserved. Do not distribute.
