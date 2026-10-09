import requests
import time
import json

base_url = "http://localhost:8000/api"

print("1. Creating Experiment...")
# POST /experiments
payload = {
    "name": "Phase 8 E2E",
    "population": 30,
    "runs": 1,
    "duration_days": 3
}
res = requests.post(f"{base_url}/experiments", params=payload)
exp = res.json()
print("Experiment Created:", exp)
exp_id = exp["id"]

print("2. Running Experiment...")
res = requests.post(f"{base_url}/experiments/{exp_id}/run")
print("Run Status:", res.json())

print("3. Fetching Matrix...")
res = requests.get(f"{base_url}/experiments/{exp_id}/cross-model-interactions")
matrix = res.json()
print("Matrix:", json.dumps(matrix, indent=2))

print("4. Fetching Model Comparison...")
res = requests.get(f"{base_url}/experiments/{exp_id}/comparison")
comp = res.json()
print("Comparison:", json.dumps(comp, indent=2))
