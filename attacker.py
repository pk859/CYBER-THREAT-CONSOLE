import requests
import time
import random

API_URL = "http://127.0.0.1:5000/incidents"

# --- EDITED: Using a curated list of well-known public IPs ---
# These are guaranteed to have a real-world location.
guaranteed_public_ips = [
    "8.8.8.8",       # Google DNS (USA)
    "1.1.1.1",       # Cloudflare DNS (USA)
    "208.67.222.222",# OpenDNS (USA)
    "9.9.9.9",       # Quad9 (Switzerland)
    "195.8.215.68",  # DNS.WATCH (Germany)
    "185.228.168.9", # CleanBrowsing (Netherlands)
    "1.0.0.1",       # Cloudflare Secondary (USA)
    "8.8.4.4",       # Google Secondary (USA)
    "149.112.112.112", # Quad9 Secondary (USA)
    "202.46.34.75",   # A major ISP (Japan)
    "45.33.32.156"    # Linode Server (USA)
]

# Scenarios remain the same
scenarios = [
    {
        "title": "SQL Injection Attempt", "incident_type_id": 3,
        "description_template": "WAF blocked SQL injection payload from {ip} targeting login form.",
        "target_systems": [1, 2]
    },
    {
        "title": "Cross-Site Scripting (XSS)", "incident_type_id": 3,
        "description_template": "Potential XSS attack detected in user comment field from {ip}.",
        "target_systems": [1]
    },
    {
        "title": "Ransomware Signature Detected", "incident_type_id": 1,
        "description_template": "File with '.lockbit' extension found on system ID {system_id}, initiated from {ip}.",
        "target_systems": [1, 3]
    },
    {
        "title": "Credential Phishing Email Reported", "incident_type_id": 2,
        "description_template": "User reported a phishing email from 'IT-Support' originating from {ip}.",
        "target_systems": [3]
    },
    {
        "title": "SSH Brute Force", "incident_type_id": 4,
        "description_template": "Over 100 failed SSH login attempts in 1 minute from {ip} on system ID {system_id}.",
        "target_systems": [1, 2]
    },
    {
        "title": "Data Exfiltration Alert", "incident_type_id": 3,
        "description_template": "Unusual outbound data transfer of 5GB to {ip} from HR Database.",
        "target_systems": [2]
    }
]

print("Starting RELIABLE attacker script... Press CTRL+C to stop.")
print("Simulating attacks from known public IP addresses...")

# --- Main Loop ---
while True:
    try:
        if random.random() < 0.1: 
            burst_count = random.randint(2, 3) # EDITED: Smaller burst
            print(f"\n⚡ ATTACK BURST: Simulating {burst_count} rapid events... ⚡")
            for _ in range(burst_count):
                # EDITED: Slowed down burst speed to avoid rate limiting
                time.sleep(random.uniform(1.5, 2.5))
                
                scenario = random.choice(scenarios)
                ip = random.choice(guaranteed_public_ips) # EDITED: Use the reliable IP list
                system_id = random.choice(scenario["target_systems"])
                
                payload = {
                    "title": scenario["title"],
                    "description": scenario["description_template"].format(ip=ip, system_id=system_id),
                    "system_id": system_id,
                    "incident_type_id": scenario["incident_type_id"],
                    "ip_address": ip
                }
                requests.post(API_URL, json=payload)
                print(f"  - BURST: Logged '{payload['title']}' from {payload['ip_address']}.")
            print("⚡ Burst complete. Returning to normal pace. ⚡\n")
            
        scenario = random.choice(scenarios)
        ip = random.choice(guaranteed_public_ips) # EDITED: Use the reliable IP list
        system_id = random.choice(scenario["target_systems"])

        payload = {
            "title": scenario["title"],
            "description": scenario["description_template"].format(ip=ip, system_id=system_id),
            "system_id": system_id,
            "incident_type_id": scenario["incident_type_id"],
            "ip_address": ip
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code == 201:
            print(f"SUCCESS: Logged incident '{payload['title']}' from {payload['ip_address']}.")
        else:
            print(f"ERROR: Failed to log incident. Status code: {response.status_code}")
        
        # EDITED: Slightly increased normal sleep time
        time.sleep(random.uniform(4, 8))

    except requests.exceptions.ConnectionError:
        print("ERROR: Connection to the backend server failed. Is app.py running?")
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nAttacker script stopped.")
        break