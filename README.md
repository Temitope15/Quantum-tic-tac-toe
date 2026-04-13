# Quantum Tic-Tac-Toe Monorepo

This project is a monorepo containing a Python FastAPI backend and a Next.js frontend for Quantum Tic-Tac-Toe.

## Local Development

### Backend
1. `cd backend`
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Deployment

### Backend (Render)
1. Create a new **Web Service** on Render.
2. Select your repository.
3. Set **Root Directory** to `backend`.
4. Set **Build Command** to `pip install -r requirements.txt`.
5. Set **Start Command** to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
6. Add an environment variable `PYTHON_VERSION` (e.g., `3.10.0`) if needed.

### Frontend (Vercel)
1. Create a new **Project** on Vercel.
2. Select your repository.
3. Set **Root Directory** to `frontend`.
4. Vercel should automatically detect Next.js.
5. Add an **Environment Variable**:
   - `NEXT_PUBLIC_API_URL`: The URL of your Render backend (e.g., `https://your-backend.onrender.com`).
