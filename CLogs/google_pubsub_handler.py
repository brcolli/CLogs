from google.cloud import pubsub_v1
from google.cloud import bigquery


class GooglePubSubHandler:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.bigquery_client = bigquery.Client()

    def publish_log_entry(self, topic_name: str, entry: bytes):
        """
        Publish a single entry.

        :param topic_name: Topic to publish to (ex. synthetic_logs)
        :param entry: Entry byte to publish to Google Pub/Sub
        :return: None
        """
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        self.publisher.publish(topic_path, entry)

    def publish_log_entries(self, topic_name: str, entries: list[bytes]):
        """
        Publish a list of entries.

        :param topic_name: Topic to publish to (ex. synthetic_logs).
        :param entries: List of entry bytes to publish to Google Pub/Sub
        :return: None
        """
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        publish_futures = []

        for entry in entries:
            message_future = self.publisher.publish(topic_path, entry)
            publish_futures.append(message_future)

        # Ensure all published appropriately
        for future in publish_futures:
            future.result()

    @staticmethod
    def callback(message):
        """
        Process the received log message, then acknowledges it.

        :param message: Message received from Pub/Sub
        :return:
        """
        print(f"Received message: {message.data}")
        message.ack()  # Acknowledge the message to remove it from the subscription

    def _subscribe_to_synthetic_logs(self) -> str:
        return self.subscriber.subscription_path(self.project_id, 'synthetic_logs_pull')

    def _pull_subscription_messages(self, subscription_path: str):
        self.subscriber.subscribe(subscription_path, callback=GooglePubSubHandler.callback)

    def pull_synthetic_logs(self):
        self._pull_subscription_messages(self._subscribe_to_synthetic_logs())

    def query_synthetic_logs(self) -> list:
        """
        Get all synthetic logs in the BigQuery CLogs.synthetic_logs table.

        :return: A list of all the logs in the BigQuery table
        """

        query_job = self.bigquery_client.query(f"""
        SELECT *
        FROM `{self.project_id}.CLogs.synthetic_logs`
        """)
        results = query_job.result()
        return list(results)
