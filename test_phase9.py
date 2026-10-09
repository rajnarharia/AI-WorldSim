import requests
import json

base_url = "http://localhost:8000/api/experiments"

print("1. Fetching experiments...")
exps = requests.get(base_url).json()
if not exps:
    print("No experiments found! Run test_phase8.py first.")
    exit(1)

exp = exps[0]
print(f"Using experiment: {exp['id']} - {exp['name']}")

print("2. Generating report...")
res = requests.post(f"{base_url}/{exp['id']}/generate-report")
print(res.json())

print("3. Fetching generated report...")
res = requests.get(f"{base_url}/{exp['id']}/report")
report = res.json()
print("Overview:", report.get("overview"))
print("Findings:", report.get("findings"))
print("Conclusion:", report.get("conclusion"))

print("4. Testing JSON Export...")
res = requests.get(f"{base_url}/{exp['id']}/export/json")
print("JSON length:", len(res.content))

print("5. Testing CSV Export...")
res = requests.get(f"{base_url}/{exp['id']}/export/csv")
print("CSV length:", len(res.content))
if len(res.content) < 50:
    print("CSV Content:", res.text)

print("6. Testing PDF Export...")
res = requests.get(f"{base_url}/{exp['id']}/export/pdf")
print("PDF length:", len(res.content))
if len(res.content) < 150:
    print("PDF Text Content:", res.text)

print("Phase 9 E2E Test Complete!")
