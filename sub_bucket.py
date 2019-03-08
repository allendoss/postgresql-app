import os
from google.cloud import pubsub_v1

project_id = 'curv-pose'
topic = 'testtopic'
sub = 'subber'

subscriber = pubsub_v1.SubscriberClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic,  # Set this to something appropriate.
)
subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=project_id,
    sub=sub,  # Set this to something appropriate.
)
# subscriber.create_subscription(
#     name=subscription_name, topic=topic_name)

def callback(message):
    print(message.data)
    message.ack()

future = subscriber.subscribe(subscription_name, callback)

try:
    future.result()
except KeyboardInterrupt:
    future.cancel()