import time
import threading

from google_pubsub_handler import GooglePubSubHandler
from synthetic_log_generator import SyntheticLogGenerator
from env_handler import EnvHandler


class CloudLogsManager:

    def __init__(self):
        eh = EnvHandler()
        self.gpsh = GooglePubSubHandler(eh.project_id)
        self.slg = SyntheticLogGenerator()

    def publish_synthetic_logs_to_pubsub(self, num_logs: int = 1000):
        """
        Publishes a number of randomly generated synthetic logs to Google's Pub/Sub.

        :param num_logs: Number of logs to generate and publish
        :return: None
        """
        # Generate log entries
        synthetic_logs = self.slg.generate_log_entries(num_logs=num_logs)
        self.gpsh.publish_log_entries('synthetic_logs', synthetic_logs)

    def _publish_log_entry_loop(self, interval: float):
        """
        A loop to run in a separate thread that publishes a synthetic log entry in a set time interval.

        :param interval: Time to wait between log generation
        :return:
        """
        while True:
            log_entry = self.slg.generate_log_entry()
            print(log_entry)
            self.gpsh.publish_log_entry('synthetic_logs', log_entry)
            time.sleep(interval)

    def start_log_stream(self, interval: float = 1.0):
        """

        :param interval:
        :return:
        """
        log_generation_thread = threading.Thread(
            target=self._publish_log_entry_loop(interval),
            daemon=True
        )
        log_generation_thread.start()

        while True:
            time.sleep(1)


if __name__ == '__main__':

    clm = CloudLogsManager()
    clm.publish_synthetic_logs_to_pubsub(10)
    results = clm.gpsh.query_synthetic_logs()
    print(results)
