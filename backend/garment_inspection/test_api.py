import requests
import json

# Base URL for the Django API
BASE_URL = "http://127.0.0.1:8000"

# Step 1: Login Supervisor
print("\n🔐 Logging in Supervisor...")
sup_login = requests.post(f"{BASE_URL}/login/", json={"username": "test_sup", "password": "Pass123!"})
if sup_login.status_code == 200:
    SUP_TOKEN = sup_login.json()["access"]
    SUP_HEADERS = {"Authorization": f"Bearer {SUP_TOKEN}", "Content-Type": "application/json"}
    print("✅ Supervisor login successful.")
else:
    print("❌ Supervisor login failed.")
    print(sup_login.text)
    SUP_HEADERS = {}

# Step 2: Login Inspector
print("\n🔐 Logging in Inspector...")
insp_login = requests.post(f"{BASE_URL}/login/", json={"username": "test_insp", "password": "Pass123!"})
if insp_login.status_code == 200:
    INSP_TOKEN = insp_login.json()["access"]
    INSP_HEADERS = {"Authorization": f"Bearer {INSP_TOKEN}", "Content-Type": "application/json"}
    print("✅ Inspector login successful.")
else:
    print("❌ Inspector login failed.")
    print(insp_login.text)
    INSP_HEADERS = {}

# Define endpoints and their test data
endpoints = [
    {"name": "Register Supervisor", "method": "post", "url": "/register/", "headers": {}, 
     "data": {"username": "test_sup", "email": "test_sup@example.com", "password": "Pass123!", "password2": "Pass123!"}},
    
    {"name": "Assign Supervisor Role", "method": "post", "url": "/api/user/assign-role/", "headers": SUP_HEADERS, 
     "data": {"role_type": "supervisor", "name": "Test Sup", "phone": "0770000000", "department": "QC"}},
    
    {"name": "Get User Role (Supervisor)", "method": "get", "url": "/api/user/role/", "headers": SUP_HEADERS},

    {"name": "Register Inspector", "method": "post", "url": "/register/", "headers": {}, 
     "data": {"username": "test_insp", "email": "test_insp@example.com", "password": "Pass123!", "password2": "Pass123!"}},
    
    {"name": "Assign Inspector Role", "method": "post", "url": "/api/user/assign-role/", "headers": INSP_HEADERS, 
     "data": {"role_type": "inspector", "name": "Test Insp", "phone": "0771111111"}},
    
    {"name": "Get User Role (Inspector)", "method": "get", "url": "/api/user/role/", "headers": INSP_HEADERS},

    {"name": "List Defects", "method": "get", "url": "/defects/", "headers": INSP_HEADERS},
    
    {"name": "Create Defect", "method": "post", "url": "/defects/", "headers": INSP_HEADERS, 
     "data": {"defect_type": "Tear", "severity": "High"}},

    {"name": "List Inspections", "method": "get", "url": "/inspections/", "headers": INSP_HEADERS},
    
    {"name": "Create Inspection", "method": "post", "url": "/inspections/", "headers": INSP_HEADERS, 
     "data": {"cli_inspector": 2, "supervisor": 2, "fabric_defect": 1, "status": "Pending"}},

    {"name": "List Flags", "method": "get", "url": "/flags/", "headers": INSP_HEADERS},
    
    {"name": "Create Flag", "method": "post", "url": "/flags/create/", "headers": INSP_HEADERS, 
     "data": {
         "operator_id": "OP123", "machine_no": "M1", "defect": "Hole",  # Changed from "Tear" to "Hole"
         "inspected_by": "Test Insp",
         "supervisor_in_charge": "Test Sup",
         "date_of_inspection": "2025/06/23",
         "time_of_inspection": "09:00",
         "flag_type": "RED"}},

    {"name": "List Notifications", "method": "get", "url": "/notifications/?supervisor_id=2", "headers": SUP_HEADERS},
    
    {"name": "Read Notification", "method": "post", "url": "/notifications/1/read/", "headers": SUP_HEADERS},
    
    {"name": "Read All Notifications", "method": "post", "url": "/notifications/read-all/", "headers": SUP_HEADERS, 
     "data": {"supervisor_id": 2}},

    {"name": "Inspector Dashboard", "method": "get", "url": "/inspectors/dashboard/?inspector_id=2&date=2025-06-23", "headers": INSP_HEADERS},
    
    {"name": "Supervisor Dashboard", "method": "get", "url": "/supervisors/dashboard/?supervisor_id=2&date=2025-06-23", "headers": SUP_HEADERS},
]

# Run tests
for ep in endpoints:
    print(f"\n🔹 Testing: {ep['name']}")
    full_url = BASE_URL + ep["url"]
    method = ep["method"]
    kwargs = {"headers": ep.get("headers", {})}
    if "data" in ep:
        kwargs["json"] = ep["data"]
    try:
        response = getattr(requests, method)(full_url, **kwargs)
        print(f"Status: {response.status_code}")
        try:
            print("Response:", json.dumps(response.json(), indent=2))
        except:
            print("Raw response:", response.text)
    except Exception as e:
        print("❌ Error:", str(e))
