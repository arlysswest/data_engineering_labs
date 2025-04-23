from google.cloud import pubsub_v1
import time

project_id = "data-engineering-spring"
subscription_id = "MySub"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

message_count = 0

def callback(message):
    global message_count
    message_count += 1
    print(f"Received message {message_count}: {message.data.decode('utf-8')}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print(f"\nTotal messages received: {message_count}")
