# Run locally

Backend:
```
cd backend
../.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

Frontend:
```
cd frontend
npm run dev
```
Then open http://localhost:5173

Tests:
```
cd backend
../.venv/bin/python -m pytest -q
```

Frontend build:
```
cd frontend
npm run build
```