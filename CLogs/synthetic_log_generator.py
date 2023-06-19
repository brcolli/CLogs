import threading
from faker import Faker
from avro_serialize import AvroSerialize


class SyntheticLogGenerator:

    def __init__(self):
        self.fake = threading.local()

    def generate_log_entry(self, num_log_words: int = 6) -> bytes:
        """
        Generate a synthetic log entry of timestamp, levels (INFO, WARNING, or ERROR), and sentences.

        :param num_log_words: Number of words per sentence
        :return: A serialized bytes string to match an AVRO JSON schema
        """
        fake = getattr(self.fake, "fake", None)
        if fake is None:
            fake = self.fake.fake = Faker()

        log_timestamp = str(fake.date_time_this_year())
        log_level = fake.random_element(['INFO', 'WARNING', 'ERROR'])
        log_message = fake.sentence(nb_words=num_log_words, variable_nb_words=True)

        # Create a dictionary representing the log entry
        log_entry = {
            "timestamp": log_timestamp,
            "level": log_level,
            "message": log_message
        }
        serialized_entry = AvroSerialize.serialize_synthetic_log(log_entry)

        return serialized_entry

    def generate_log_entries(self, num_logs: int = 10000) -> list:
        """
        Generate a list of synthetic log entries.

        :param num_logs: Number of logs to generate
        :return: A list of num_logs synthetic logs
        """
        return [self.generate_log_entry(num_log_words=10) for _ in range(num_logs)]
