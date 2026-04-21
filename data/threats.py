# ============================================================
# data/threats.py — The Data Layer
# ============================================================
# This module is responsible for one thing: providing threat data.
#
# Right now it generates fake/simulated data using Python's
# random module — this is common in portfolio projects to
# demonstrate the system without needing a real database.
#
# In a real SOC tool, you'd replace the generate_threats()
# function with a database query (PostgreSQL, MongoDB, etc.)
# or a call to a real SIEM API. The routes layer wouldn't
# need to change at all — that's the point of separation.
# ============================================================

from datetime import datetime, timedelta  # for generating realistic timestamps
import random                              # for randomizing threat attributes


# ── THREAT CATALOG ────────────────────────────────────────────
# A list of dicts describing each type of threat we can simulate.
# Each entry maps to a real attack technique from the
# MITRE ATT&CK framework (mitre.org) — an industry-standard
# library of adversary tactics and techniques.
THREAT_CATALOG = [
    {
        "type": "SQL Injection",
        "description": "Malicious SQL statements injected into input fields to manipulate the database.",
        "category": "Web Attack",
        "mitre_technique": "T1190",   # Exploit Public-Facing Application
    },
    {
        "type": "Brute Force Login",
        "description": "Repeated login attempts to guess credentials through automated tooling.",
        "category": "Credential Access",
        "mitre_technique": "T1110",   # Brute Force
    },
    {
        "type": "Port Scan",
        "description": "Systematic scan of open ports to map the target network's attack surface.",
        "category": "Reconnaissance",
        "mitre_technique": "T1046",   # Network Service Discovery
    },
    {
        "type": "XSS Attempt",
        "description": "Cross-site scripting payload injected to execute scripts in victim's browser.",
        "category": "Web Attack",
        "mitre_technique": "T1059.007",  # JavaScript execution
    },
    {
        "type": "DDoS Traffic",
        "description": "Distributed denial-of-service flood detected from multiple source IPs.",
        "category": "Impact",
        "mitre_technique": "T1498",   # Network Denial of Service
    },
    {
        "type": "Command & Control Beacon",
        "description": "Outbound beacon to known C2 infrastructure detected on internal host.",
        "category": "C2",
        "mitre_technique": "T1071",   # Application Layer Protocol
    },
    {
        "type": "Privilege Escalation",
        "description": "Attempt to gain elevated permissions beyond normal user scope.",
        "category": "Privilege Escalation",
        "mitre_technique": "T1068",   # Exploitation for Privilege Escalation
    },
    {
        "type": "Phishing URL Click",
        "description": "User navigated to a known phishing domain from corporate network.",
        "category": "Initial Access",
        "mitre_technique": "T1566.002",  # Spearphishing Link
    },
]


# ── SEVERITY LEVELS ───────────────────────────────────────────
# Standard severity tiers used in real security tooling.
SEVERITY_LEVELS  = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]

# Weights control how often each severity appears in generated data.
# Higher weight = more likely. This makes MEDIUM/LOW more common
# than CRITICAL, which reflects realistic threat distributions.
# Index matches: CRITICAL=5%, HIGH=20%, MEDIUM=35%, LOW=30%, INFO=10%
SEVERITY_WEIGHTS = [5, 20, 35, 30, 10]


# ── STATUS OPTIONS ────────────────────────────────────────────
# Lifecycle states a threat event can be in.
STATUS_OPTIONS = ["ACTIVE", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE"]
STATUS_WEIGHTS = [30, 25, 35, 10]  # weighted so ACTIVE and RESOLVED are most common


# ── AFFECTED SYSTEMS ─────────────────────────────────────────
# Simulated internal hostnames — these are realistic names you'd
# see in a corporate network inventory.
AFFECTED_SYSTEMS = [
    "web-server-01", "db-server-02", "auth-service", "api-gateway",
    "workstation-HR-04", "vpn-endpoint", "mail-server", "firewall-edge",
]


# ── HELPER FUNCTIONS ─────────────────────────────────────────

def _random_ip(internal=False):
    """
    Generate a plausible-looking IP address.
    internal=True → 10.x.x.x range (RFC 1918 private network)
    internal=False → random public-ish IP
    The leading underscore is a Python convention meaning
    "this is a private helper, not part of the public API."
    """
    if internal:
        # 10.0.x.x is a typical internal subnet range
        return f"10.0.{random.randint(1, 10)}.{random.randint(2, 254)}"
    # Avoid reserved/special ranges for external IPs (0.x, 224+)
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def _random_timestamp(hours_back=72):
    """
    Generate an ISO 8601 timestamp (e.g. "2025-04-19T14:32:11Z")
    at a random point within the last N hours.
    ISO 8601 is the international standard format for datetimes —
    you'll see it everywhere in APIs and logs.
    """
    # timedelta creates a time duration
    # random.uniform gives a float between 0 and hours_back
    offset = timedelta(hours=random.uniform(0, hours_back))
    # Subtract the offset from now to get a past timestamp
    return (datetime.utcnow() - offset).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── MAIN GENERATOR ───────────────────────────────────────────

def generate_threats(count=25):
    """
    Build and return a list of `count` simulated threat event dicts.
    Each call produces fresh randomized data.

    In a real app this function would run a SQL query like:
        SELECT * FROM threats ORDER BY timestamp DESC LIMIT 25;
    """
    threats = []

    # range(1, count+1) so IDs start at 1 instead of 0
    for i in range(1, count + 1):

        # Pick a random threat type from the catalog
        catalog_entry = random.choice(THREAT_CATALOG)

        # random.choices() respects the weights list —
        # so MEDIUM gets picked ~35% of the time, CRITICAL ~5%, etc.
        # k=1 means pick one item, [0] unpacks it from the list.
        severity = random.choices(SEVERITY_LEVELS, weights=SEVERITY_WEIGHTS, k=1)[0]
        status   = random.choices(STATUS_OPTIONS,  weights=STATUS_WEIGHTS,   k=1)[0]

        # Build the threat dict — this is the structure your API returns
        # and what the frontend JavaScript reads.
        threat = {
            "id":               i,
            "type":             catalog_entry["type"],
            "description":      catalog_entry["description"],
            "category":         catalog_entry["category"],
            "mitre_technique":  catalog_entry["mitre_technique"],
            "severity":         severity,
            "status":           status,
            "source_ip":        _random_ip(internal=False),   # attacker IP
            "target_ip":        _random_ip(internal=True),    # internal victim
            "affected_system":  random.choice(AFFECTED_SYSTEMS),
            "timestamp":        _random_timestamp(),
            "event_count":      random.randint(1, 500),  # how many times this fired
        }
        threats.append(threat)

    # Sort newest first so the dashboard shows recent events at the top
    threats.sort(key=lambda t: t["timestamp"], reverse=True)
    return threats


# ── MODULE-LEVEL DATA ─────────────────────────────────────────
# Generate the threats once when this module is first imported.
# Because Python caches imported modules, this runs exactly once
# per server session — so IDs stay stable while the server is running.
# Every time you restart `python app.py`, new random data is generated.
THREATS = generate_threats(25)
