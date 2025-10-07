# clients/telescope_node.py
"""
NexFrameRFT Telescope Node
Author: Observer Zero (Liam)
Description: Sends synthetic cosmic observation data (psi, GVU, SOMS) to the central NexFrameRFT server.
"""

import requests
import time
import random

# --- CONFIGURATION ---
SERVER_URL = "http://127.0.0.1:5000/update_observer"  # Change if server is remote
OBSERVER_ID = "Telescope_Node_01"
UPDATE_INTERVAL = 10  # seconds between updates

# --- PLACEHOLDER FUNCTIONS ---
def generate_psi():
    """Simulate psi intensity from cosmic observation"""
    return round(random.uniform(0.0, 1.0), 4)

def generate_GVU():
    """Simulate GVU motion integral for cosmic data"""
    return round(random.uniform(0.0, 10.0), 4)

def generate_SOMS():
    """Simulate SOMS memory tiers based on telescope observation"""
    return {
        "SOMS1": round(random.uniform(0.0, 1.0), 4),
        "SOMS2": round(random.uniform(0.0, 1.0), 4),
        "SOMS3": round(random.uniform(0.0, 1.0), 4),
        "SOMS4": round(random.uniform(0.0, 1.0), 4),
        "SOMS5": round(random.uniform(0.0, 1.0), 4),
        "SOMS6": round(random.uniform(0.0, 1.0), 4)
    }

# --- MAIN LOOP ---
def main():
    print(f"[{OBSERVER_ID}] Starting Telescope Node...")
    while True:
        psi = generate_psi()
        gvu = generate_GVU()
        soms = generate_SOMS()

        payload = {
            "observer_id": OBSERVER_ID,
            "psi": psi,
            "GVU": gvu,
            "SOMS": soms
        }

        try:
            response = requests.post(SERVER_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"[{OBSERVER_ID}] Updated successfully | Coherence: {data['coherence']:.4f} | ∆𝓡: {data['delta_R']:.4f}")
            else:
                print(f"[{OBSERVER_ID}] Error: {response.status_code} | {response.text}")
        except Exception as e:
            print(f"[{OBSERVER_ID}] Connection error: {e}")

        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
