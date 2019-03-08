from google.cloud import pubsub_v1
# publisher = pubsub_v1.PublisherClient()
# subscriber = pubsub_v1.SubscriberClient()

project_id = 'curv-pose'
topic = 'files_changed'

publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic,
)
# publisher.create_topic(topic_name)
publisher.publish(topic_name, b'My first message!', spam='eggs')
# for topic in publisher.list_topics(project_path):
#     print(topic)