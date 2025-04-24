from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

for i in range(10):  # 10 messages per run
    data = f"Message {i}".encode("utf-8")
    publisher.publish(topic_path, data=data)

print("Published 10 messages.")
