# ============================================================
# app.py — Flask Entry Point
# ============================================================
# This is the file you run to start the server: `python app.py`
# Its only job is to create the Flask app, configure it,
# register the routes (Blueprint), and launch the server.
#
# Think of this as the "main hub" — it doesn't contain
# any business logic itself, it just wires everything together.
# ============================================================

# Flask is the web framework. It handles incoming HTTP requests
# and lets you define what happens for each URL.
from flask import Flask

# flask_cors handles Cross-Origin Resource Sharing (CORS).
# Without this, the browser blocks our HTML frontend from
# calling the API because they're technically different "origins"
# (even on the same machine during development).
from flask_cors import CORS

# We import the Blueprint from our routes module.
# A Blueprint is a collection of routes that lives in its own file.
# This keeps app.py clean — routes are defined elsewhere.
from routes.threats import threats_bp


# Create the Flask application instance.
# __name__ tells Flask the name of the current module (used internally).
# static_folder="static" tells Flask where to find HTML/CSS/JS files.
# static_url_path="/static" sets the URL prefix for those files.
app = Flask(__name__, static_folder="static", static_url_path="/static")

# Apply CORS to the entire app so any frontend can call our API.
# In production you'd lock this down to specific domains.
CORS(app)

# Register the threats Blueprint onto the main app.
# url_prefix="/api" means every route defined in the Blueprint
# will be prefixed with /api — so /threats becomes /api/threats.
# This is a common convention to separate API routes from page routes.
app.register_blueprint(threats_bp, url_prefix="/api")


# This route handles GET requests to "/" (the root URL).
# When someone visits http://localhost:5000 in their browser,
# Flask serves the dashboard HTML file.
@app.route("/")
def index():
    return app.send_static_file("dashboard.html")


# This block only runs when you execute this file directly:
#   python app.py
# It does NOT run if this file is imported by another module.
# debug=True means Flask will auto-reload when you save changes
# and show detailed error pages — only use this in development.
# port=5000 sets which port the server listens on.
if __name__ == "__main__":
    app.run(debug=True, port=5000)
