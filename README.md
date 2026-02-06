# Portfolio

Personal portfolio app with a Flask backend and a redesigned UI (dark glass style) for:
- Home (`/`)
- Projects (`/projects`)
- Tools (`/tools`)
- More Tools (`/more-tools`, authenticated only)
- Contact (`/contact`)
- Login (`/login`)

The repo also contains an optional Next.js frontend in `frontend/`.

## Current Stack

- Python + Flask
- HTML templates (Jinja2)
- Tailwind CSS (CDN runtime config in templates)
- Lucide icons (CDN)
- Google Fonts (`Sora`, `Space Grotesk`)
- Optional: Next.js app (`frontend/`) with proxy rewrite to Flask

## What Was Recently Added

- New routes/pages:
  - `GET /projects` (`templates/projects.html`)
  - `GET /tools` (`templates/tools.html`)
  - `GET /more-tools` (`templates/more_tools.html`, login required)
  - `GET /login` and `GET /logout`
- Mobile nav that collapses behind a menu button (`menuToggle` / `mobileMenu`)
- Updated branding assets:
  - Header logo: `static/images/Mael Logo.png`
  - Hero image: `static/images/Mael Maitre.png`
- Contact flow hardening:
  - JSON + form payload support
  - Honeypot field (`company`)
  - Minimum message length validation
- Authentication hardening:
  - SQLite-backed users
  - Password hashing with Werkzeug
  - Account lockout after failed attempts (no IP-based restriction)

## Project Structure (Important Files)

- `main.py`: Flask app, routes, and `/send_email` API
- `get_info.py`: SMTP send logic
- `templates/index.html`: Home page
- `templates/projects.html`: Projects page (placeholder)
- `templates/tools.html`: public/private tools page
- `templates/more_tools.html`: private tools page
- `templates/login.html`: login page
- `templates/contact.html`: Contact page and frontend submit JS
- `static/images/`: image assets (logo, hero, social images, etc.)
- `env.example`: expected environment variables

## Backend Setup (Flask)

1. Create and activate venv:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Configure environment variables from `env.example`.

4. Run:
```powershell
python main.py
```

Flask runs on:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/projects`
- `http://127.0.0.1:5000/tools`
- `http://127.0.0.1:5000/login`
- `http://127.0.0.1:5000/contact`
- `http://127.0.0.1:5000/health`

## Authentication and Database

This project uses SQLite + Flask-Login.

1. Install dependencies:
```powershell
pip install -r requirements.txt
```

2. Set admin credentials in your shell (or `.env` loader if you use one):
```powershell
$env:ADMIN_USERNAME="admin"
$env:ADMIN_PASSWORD="change-this-password"
```

3. Initialize database and create admin user:
```powershell
python main.py init-db
```

4. Start app and login at `/login`.

Auth behavior:
- Failed login attempts are counted per existing user.
- After `LOGIN_MAX_ATTEMPTS`, account is locked for `LOGIN_LOCKOUT_MINUTES`.
- No IP-based rate limiting is used.

## API Contract

### `POST /send_email`

Accepted payload types:
- `application/json`
- `application/x-www-form-urlencoded`

Expected fields:
- `firstName`
- `lastName`
- `email`
- `the_email`
- `company` (honeypot, optional)

Behavior:
- If `company` has a value, request is silently accepted (`200`) as anti-bot handling.
- If `the_email` has fewer than 10 chars, returns `400`.
- On success returns `{ "ok": true }`.

## Email Delivery Modes

Control with `EMAIL_DELIVERY_MODE`:
- `mock`: does not send SMTP, logs server-side
- `smtp`: sends real email via `get_info.send_email(...)`

For SMTP mode, configure at least:
- `CONTACT_TO_ADDRESS`
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`

## Design Customization Guide

To keep the same visual style while editing content:

- Replace hero image by updating file used in `templates/index.html`:
  - `url_for('static', filename='images/Mael Maitre.png')`
- Replace header logo in templates:
  - `url_for('static', filename='images/Mael Logo.png')`
- Adjust typography/colors in each template inside:
  - `tailwind.config.theme.extend`
  - local `<style>` classes (`panel`, `soft-border`, `chip`, etc.)
- Keep responsive menu behavior by preserving:
  - `initMobileMenu("menuToggle", "mobileMenu")`
  - matching element IDs in header markup

## Optional Frontend Setup (Next.js)

If you want the Next.js version:

1. Install dependencies:
```powershell
cd frontend
npm install
```

2. Set backend URL:
```powershell
$env:BACKEND_URL="http://127.0.0.1:5000"
```

3. Run:
```powershell
npm run dev
```

Frontend URL:
- `http://localhost:3000`

## Quick Checks

- Python syntax check:
```powershell
python -m py_compile main.py get_info.py
```

- Health check:
```powershell
curl http://127.0.0.1:5000/health
```

## Notes

- CORS is enabled globally in `main.py` with `CORS(app)`.
- `main.py` reads env vars directly (no implicit `.env` loader).
