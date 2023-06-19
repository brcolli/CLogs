from dotenv import dotenv_values


"""
Class to manage environment variable capturing. Should be represented as a singleton.
"""


class EnvHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        config = dotenv_values("C:\\Users\\benrc\\Documents\\CLogs\\CLogs\\.env")
        self.project_id = config["PROJECT_ID"]
