# Multi-Agent Studio

React + Flask multi-agent workflow application.

## Structure

- `frontend/` — React + Vite UI
- `backend/` — Flask API and agents
- `api/index.py` — Vercel Python entrypoint
- `vercel.json` — single-project Vercel configuration

## Local run

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend:
`http://127.0.0.1:5000/api/health`

### Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:
`http://localhost:5173`

For local development, set `frontend/.env` to:

```env
VITE_API_URL=http://127.0.0.1:5000
```

## Vercel

Deploy the repository root as the Vercel project root.

Do not set the Root Directory to `backend`.

The root `api/index.py` exposes the Flask app, while `frontend/dist` is the Vite output.

After deployment test:

`https://YOUR-DOMAIN.vercel.app/api/health`

Expected:

```json
{
  "service": "multi-agent-backend",
  "status": "ok"
}
```
