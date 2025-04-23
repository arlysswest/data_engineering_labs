#WORKING!!
from google.cloud import pubsub_v1
import json
import time
import os

# Set path to your credentials (if not set in shell)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/arlysswest/keys/gcloud-creds.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="/Users/arlysswest/Desktop/cs-410/data transport/data transport lab/data-engineering-spring-a049302cdbbf.json"
# Set topic path
project_id = "data-engineering-spring"  
topic_id = "MyTopic"
topic_path = f"projects/{project_id}/topics/{topic_id}"

# Create a publisher client
publisher = pubsub_v1.PublisherClient()

# Load data from file
#with open("bcsample.json") as f:
with open("vehicle_data.json") as f:
    data = json.load(f)

# Publish each record
for record in data:
    message = json.dumps(record).encode("utf-8")
    future = publisher.publish(topic_path, data=message)
    print(f"Published: {record.get('vehicle_id', 'N/A')} @ {record.get('timestamp', 'N/A')}")

print(f"Published {len(data)} records.")
