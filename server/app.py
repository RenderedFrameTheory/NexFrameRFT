# server/app.py
"""
NexFrameRFT Central Server
Author: Observer Zero (Liam)
Description: Starter RFT AI hub for collecting observer inputs,
computing basic coherence, storing ledger snapshots, and serving clients.
"""

import os
import json
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify

# --- CONFIGURATION ---
DATA_DIR = "data/snapshots"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- FLASK APP ---
app = Flask(__name__)

# In-memory storage for simplicity
universe_state = {
    "observers": {},  # {observer_id: {psi, GVU, SOMS}}
    "coherence": 0.0,
    "delta_R": 0.0
}

# --- HELPER FUNCTIONS ---
def hash_snapshot(snapshot):
    """Return SHA-512 hash of a snapshot dictionary"""
    snapshot_json = json.dumps(snapshot, sort_keys=True).encode()
    return hashlib.sha512(snapshot_json).hexdigest()

def save_snapshot(snapshot):
    """Save snapshot with timestamp and hash"""
    timestamp = datetime.utcnow().isoformat()
    snapshot_hash = hash_snapshot(snapshot)
    filename = os.path.join(DATA_DIR, f"{timestamp}_{snapshot_hash[:8]}.json")
    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)
    return filename, snapshot_hash

def compute_coherence():
    """Placeholder: compute global coherence between observers"""
    num = len(universe_state["observers"])
    if num == 0:
        return 0.0
    # Placeholder simple average for now
    return sum([obs.get("psi", 0) for obs in universe_state["observers"].values()]) / num

def compute_delta_R():
    """Placeholder: compute ∆𝓡"""
    # Simple placeholder based on coherence
    return universe_state["coherence"] * 0.01

# --- ROUTES ---
@app.route("/update_observer", methods=["POST"])
def update_observer():
    """
    Receive observer data:
    JSON expected: {"observer_id": str, "psi": float, "GVU": float, "SOMS": dict}
    """
    data = request.json
    observer_id = data.get("observer_id")
    if not observer_id:
        return jsonify({"error": "observer_id required"}), 400

    universe_state["observers"][observer_id] = {
        "psi": data.get("psi", 0.0),
        "GVU": data.get("GVU", 0.0),
        "SOMS": data.get("SOMS", {})
    }

    # Update global metrics
    universe_state["coherence"] = compute_coherence()
    universe_state["delta_R"] = compute_delta_R()

    # Save snapshot
    filename, snapshot_hash = save_snapshot(universe_state)

    return jsonify({
        "message": "Observer updated",
        "coherence": universe_state["coherence"],
        "delta_R": universe_state["delta_R"],
        "snapshot_file": filename,
        "snapshot_hash": snapshot_hash
    })

@app.route("/get_snapshot", methods=["GET"])
def get_snapshot():
    """Return the latest universe state"""
    return jsonify(universe_state)

@app.route("/history", methods=["GET"])
def history():
    """List all saved snapshots"""
    files = sorted(os.listdir(DATA_DIR))
    return jsonify({"snapshots": files})

# --- MAIN ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
