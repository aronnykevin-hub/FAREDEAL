# Fare Deal Supermarket — Local Launch

A Flask app for supermarket management: catalog, inventory, sales API, deliveries, admin CRUD, and dashboard.

## Quick start

1. Requirements
   - Python 3.10+
   - pip
   - (Optional) virtualenv

2. Clone/copy the folder, then run:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   - First run creates `.env` from `.env.example`.
   - App runs at http://127.0.0.1:5000

3. Login
   - Email: `admin@faredeal.local`
   - Password: `admin123`

## Manual steps (alternative)
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env  # then edit if needed
python3 run.py
```

## Notes
- Local DB: SQLite file under `supermarket_app/supermarket.db` (configurable via `DATABASE_URL`).
- Background scheduler runs locally; disabled on Vercel.
- For persistence on Vercel, set `DATABASE_URL` to a managed Postgres and redeploy.

## Useful URLs
- `/auth/login` — sign in
- `/dashboard/` — KPIs
- `/catalog/` — products
- `/inventory/` — adjust stock
- `/deliveries/` — delivery board
- `/admin/products` — product CRUD
- `/admin/categories` — category CRUD
