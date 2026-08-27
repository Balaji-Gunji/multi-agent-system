from flask import Flask, jsonify, request
from flask_cors import CORS

from agents.coordinator import run_workflow

app = Flask(__name__)
CORS(app)


@app.get("/")
def home():
    return jsonify({
        "service": "multi-agent-backend",
        "status": "ok",
        "message": "Backend API is working",
        "endpoints": ["/api/health", "/api/workflow"]
    })


@app.get("/api/health")
def health():
    return jsonify({
        "service": "multi-agent-backend",
        "status": "ok"
    })


@app.post("/api/workflow")
def workflow():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()

    if not task:
        return jsonify({"error": "Task is required"}), 400

    try:
        return jsonify(run_workflow(task))
    except Exception as exc:
        app.logger.exception("Workflow failed")
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
