import requests
import json
import os

vehicle_ids = [2926, 2928]  
all_data = []

for vid in vehicle_ids:
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vid}"
    resp = requests.get(url)
    if resp.status_code == 200:
        all_data.extend(resp.json())
    else:
        print(f"Failed to fetch for vehicle {vid}")

# Save transit data to a proper data file
with open("vehicle_data.json", "w") as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} records to vehicle_data.json")

# Set correct credentials path for GCP
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/arlysswest/keys/gcloud-creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/arlysswest/Desktop/cs-410/data transport/data transport lab/data-engineering-spring-a049302cdbbf.json"