# BharatPay — Fictional Neobank & UPI Target System
> **Target System for Hackathon Project CC6-IC07: API Discovery, Security and Abuse Prevention**  
> *Notice: All accounts, balances, Aadhaar, PAN, and transactions in this application are 100% synthetic test data.*

---

## 🏛️ Architecture Overview
BharatPay represents a modern Indian fintech application designed with calm, authentic aesthetics (Inter font, soft elevation, unified brand accent, integer paise accounting). Behind the scenes, it serves as the target testbed for API security posture management:

- **Reverse Proxy / API Gateway**: Nginx on Port `80` emitting structured JSON gateway logs with response timing.
- **Backend API**: Python FastAPI on Port `8000` with SQLite + SQLAlchemy, PyJWT authentication, and structured request telemetry middleware.
- **Frontend App**: React 18 + Vite + TypeScript + Tailwind CSS with a persistent synthetic watermark and hidden red-team simulation drawer (`Shift + R`).

---

## 📂 Folder Layout
```text
/bharatpay
  ├── backend/          # FastAPI server, SQLAlchemy models, logging middleware
  ├── frontend/         # React + Vite customer dashboard & red-team drawer
  ├── nginx/            # Nginx reverse proxy config & gateway log format
  ├── seed/             # Faker-based synthetic Indian user & merchant generator
  ├── spec/             # Documented OpenAPI specification (deliberately partial)
  ├── docker-compose.yml# Multi-service stack (Nginx + Backend + Frontend + Shared Logs)
  ├── .env.example      # Safe sample environment configuration
  ├── run.sh            # One-line dev startup script (Linux/macOS)
  ├── run.ps1           # One-line dev startup script (Windows)
  └── README.md
```

---

## 🚀 Running the System

### Option 1: Docker Compose (Full Gateway & Logging Pipeline)
```bash
docker compose up --build
```
Access the application at `http://localhost`.

### Option 2: Local Development Mode
- **Windows**:
  ```powershell
  .\run.ps1
  ```
- **Linux/macOS**:
  ```bash
  ./run.sh
  ```
- Backend runs at `http://localhost:8000`
- Frontend runs at `http://localhost:5173`
