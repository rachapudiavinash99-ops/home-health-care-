@echo off
echo Starting Healthcare Frontend...
cd frontend
call npm install --no-audit --no-fund
call npm run dev -- --host 127.0.0.1
