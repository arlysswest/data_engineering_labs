from google.cloud import pubsub_v1
import json
import time

project_id = "data-engineering-spring"  
topic_id = "MyTopic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Load data from bcsample.json
#with open("bcsample.json", "r") as f:
#with open("/Users/arlysswest/Desktop/cs-410/data transport lab/bcsample.json", "r") as f:
#with open("/Users/arlysswest/Desktop/cs-410/bcsample.json", "r") as f:
#with open("./bcsample.json", "r") as f:
with open("/Users/arlysswest/Desktop/cs-410/data transport/data transport lab/bcsample.json", "r") as f:
#with open("/Users/arlysswest/Desktop/cs-410/data transport/*lab/bcsample.json", "r") as f:
    records = json.load(f)
    #file_contents = f.read()
    ##print(file_contents)  # Check the content of the file
    #records = json.loads(file_contents)  # Try to load the JSON
    #print(records)

# Publish each record
for record in records:
    data_str = json.dumps(record)
    data = data_str.encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published: {data_str}")
    time.sleep(0.1)  # Optional: simulate streaming
