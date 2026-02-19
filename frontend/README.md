# TOM Demand Frontend (React)

React web frontend for the exposed TOM Demand API.

## Design Direction

This UI follows a CRUD dashboard approach inspired by admin layouts (sidebar navigation, data table, action cards), based on your shared references.

## Stack (stable)

- React 19.2.0
- React DOM 19.2.0
- Vite 7.3.0
- @vitejs/plugin-react 5.0.2

## Run

```bash
cd frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

## Environment Variables

- `VITE_API_BASE_URL` (default: `http://127.0.0.1:8000`)
- `VITE_API_KEY` (optional)
- `VITE_API_ROLE` (default: `admin`)

## Coverage

- CSV CRUD: read/upsert/delete/overwrite for ideas/RA/RS
- Entity tools: list/rename Requesting Areas and Revenue Streams
- Workflows: validate, prioritize, prioritize-rs, prioritize-global, compare
- Async jobs: submit/list/get status
