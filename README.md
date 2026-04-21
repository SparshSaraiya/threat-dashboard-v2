# ThreatWatch — Cybersecurity Threat Dashboard

A Flask-based threat intelligence dashboard simulating a SOC (Security Operations Center)
real-time feed. Built for learning full-stack architecture with a cybersecurity focus.

---

## Project Structure

```
threat-dashboard/
├── app.py              # Flask entry point — wires everything together
├── routes/
│   ├── __init__.py
│   └── threats.py      # All /api/threats routes (Blueprint)
├── data/
│   ├── __init__.py
│   └── threats.py      # Simulated threat data + generation logic
├── static/
│   └── dashboard.html  # SOC frontend dashboard
└── requirements.txt
```

### Why This Structure?
This is a **layered architecture**:
- `data/` = data layer (where your data comes from — swap in a real DB later)
- `routes/` = route layer (HTTP endpoints — only handles request/response logic)
- `static/` = presentation layer (what the user sees)
- `app.py` = entry point (wires everything together)

Each layer only talks to the one below it. This is what "modular" and "scalable" means.

---

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Flask
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/threats` | All threat events (supports query filters) |
| GET | `/api/threats/<id>` | Single threat by ID |
| GET | `/api/threats/summary` | Aggregated stats for metric cards |

### Query Parameters for `/api/threats`
```
?severity=HIGH          Filter by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
?status=ACTIVE          Filter by status (ACTIVE, INVESTIGATING, RESOLVED, FALSE_POSITIVE)
?category=Web Attack    Filter by attack category
```

### Example Responses

**GET /api/threats**
```json
{
  "count": 25,
  "threats": [
    {
      "id": 1,
      "type": "SQL Injection",
      "severity": "HIGH",
      "status": "ACTIVE",
      "source_ip": "185.220.101.42",
      "target_ip": "10.0.3.14",
      "affected_system": "db-server-02",
      "category": "Web Attack",
      "mitre_technique": "T1190",
      "timestamp": "2025-04-19T14:32:11Z",
      "event_count": 237
    }
  ]
}
```

**GET /api/threats/summary**
```json
{
  "total_threats": 25,
  "by_severity": { "HIGH": 6, "CRITICAL": 2, "MEDIUM": 9, "LOW": 7, "INFO": 1 },
  "by_status": { "ACTIVE": 8, "INVESTIGATING": 6, "RESOLVED": 9, "FALSE_POSITIVE": 2 },
  "by_category": { "Web Attack": 8, "Reconnaissance": 4, ... }
}
```

---

## Key Concepts to Know

**Flask Blueprint** — A way to organize routes into separate modules instead of
dumping everything in `app.py`. The `threats_bp` Blueprint handles all `/api/threats`
routes and gets registered onto the main app in `app.py`.

**CORS (Cross-Origin Resource Sharing)** — The `flask-cors` library allows the
HTML frontend to call the API even though they're technically different "origins"
during development.

**Separation of Concerns** — Each file has one job. `data/threats.py` knows about
data. `routes/threats.py` knows about HTTP. Neither knows about the other's internals.

**REST API Design** — Using HTTP GET with clean URLs and proper 404 responses
when a resource isn't found (`/api/threats/999` returns a 404 error JSON).

**MITRE ATT&CK Framework** — The technique IDs (T1190, T1110, etc.) reference the
real-world MITRE ATT&CK matrix, the industry standard for classifying threat behaviors.
