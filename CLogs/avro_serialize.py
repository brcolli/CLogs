import json


class AvroSerialize:

    @staticmethod
    def serialize_synthetic_log(log: dict) -> bytes:
        """
        Serializes a dictionary to a JSON byte.

        :param log: Dictionary with {str: str} mapping and keys timestamp,  level, message
        :return: Serialized JSON bytes representation of dictionary
        """
        return json.dumps(log).encode('utf-8')
