# ============================================================
# routes/threats.py — The Route Layer (API Endpoints)
# ============================================================
# This file defines all the URL endpoints related to threats.
# It uses a Flask "Blueprint" so it can live in its own file
# instead of cluttering app.py.
#
# IMPORTANT: This file only handles HTTP logic:
#   - Which URL maps to which function
#   - Reading query parameters from the request
#   - Returning JSON responses with the right status codes
#
# It does NOT define or store data — it imports that from
# data/threats.py. That separation is what "modular" means.
# ============================================================

# Blueprint: a mini Flask app you can register onto the main app.
# jsonify: converts a Python dict/list into a proper JSON HTTP response.
# request: lets us read query parameters like ?severity=HIGH
from flask import Blueprint, jsonify, request

# Import the shared threat data from the data layer.
# THREATS is a list of dicts generated when the app starts.
from data.threats import THREATS


# Create the Blueprint. The name "threats" is used internally by Flask.
# In app.py we register this with url_prefix="/api", so all routes
# here become /api/threats, /api/threats/<id>, etc.
threats_bp = Blueprint("threats", __name__)


# ── ROUTE 1: Get all threats ──────────────────────────────────
# The @threats_bp.route decorator maps this function to a URL.
# methods=["GET"] means this only responds to HTTP GET requests
# (what your browser does when you visit a URL).
@threats_bp.route("/threats", methods=["GET"])
def get_threats():
    """
    GET /api/threats
    Returns all threat events as JSON.

    Optional query parameters for filtering:
      ?severity=HIGH         → only HIGH severity threats
      ?status=ACTIVE         → only ACTIVE status threats
      ?category=Web Attack   → only that attack category
    """

    # Start with a copy of all threats so we don't modify the original list.
    threats = THREATS.copy()

    # request.args is a dict of query parameters from the URL.
    # .get("severity", "") returns "" if the param isn't in the URL.
    # .upper() normalizes it so "high" and "HIGH" both work.
    severity_filter = request.args.get("severity", "").upper()
    status_filter   = request.args.get("status", "").upper()
    category_filter = request.args.get("category", "")

    # List comprehension filtering — only keep threats that match.
    # These only run if the filter was actually provided in the URL.
    if severity_filter:
        threats = [t for t in threats if t["severity"] == severity_filter]
    if status_filter:
        threats = [t for t in threats if t["status"] == status_filter]
    if category_filter:
        threats = [t for t in threats if t["category"].lower() == category_filter.lower()]

    # jsonify() converts the dict to a JSON HTTP response.
    # Flask automatically sets Content-Type: application/json.
    # Default HTTP status is 200 OK (success).
    return jsonify({
        "count": len(threats),   # how many results came back
        "threats": threats        # the actual list of threat dicts
    })


# ── ROUTE 2: Get one threat by ID ─────────────────────────────
# <int:threat_id> is a URL variable. Flask extracts the number
# from the URL and passes it as the threat_id parameter.
# int: means Flask will reject non-numeric values automatically.
@threats_bp.route("/threats/<int:threat_id>", methods=["GET"])
def get_threat_by_id(threat_id):
    """
    GET /api/threats/1
    Returns a single threat event matching the given ID.
    Returns HTTP 404 if no threat with that ID exists.
    """

    # next() walks through THREATS and returns the first match.
    # The second argument (None) is the default if nothing matches.
    # This is more efficient than looping and collecting all matches
    # since we only want one result.
    threat = next((t for t in THREATS if t["id"] == threat_id), None)

    # If no match was found, return an error response.
    # The second argument to jsonify() sets the HTTP status code.
    # 404 = "Not Found" — a standard HTTP error code.
    if threat is None:
        return jsonify({"error": f"Threat with id {threat_id} not found"}), 404

    # Return the single threat dict as JSON with default 200 OK.
    return jsonify(threat)


# ── ROUTE 3: Summary/stats for the dashboard metric cards ─────
@threats_bp.route("/threats/summary", methods=["GET"])
def get_summary():
    """
    GET /api/threats/summary
    Returns aggregated counts used to populate the metric cards
    at the top of the dashboard (total, by severity, by status, etc.)
    """

    # These dicts will hold our counts as we loop through threats.
    severity_counts = {}
    status_counts   = {}
    category_counts = {}

    # Loop through every threat and tally up the counts.
    # dict.get(key, 0) returns 0 if the key doesn't exist yet,
    # then we add 1. This avoids a KeyError on the first occurrence.
    for t in THREATS:
        severity_counts[t["severity"]] = severity_counts.get(t["severity"], 0) + 1
        status_counts[t["status"]]     = status_counts.get(t["status"], 0) + 1
        category_counts[t["category"]] = category_counts.get(t["category"], 0) + 1

    return jsonify({
        "total_threats": len(THREATS),
        "by_severity":   severity_counts,
        "by_status":     status_counts,
        "by_category":   category_counts,
    })
