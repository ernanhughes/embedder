import os
import os.path
import sys
from pathlib import Path
from tempfile import gettempdir
from typing import Any

from click import UsageError

import logging
import logging.config
from datetime import datetime as date_time
from logging import Handler

from dotenv import load_dotenv
load_dotenv()

CONFIG_FOLDER = os.path.expanduser("~/.config")
EMBEDDER_CONFIG_FOLDER = Path(CONFIG_FOLDER) / "embedder"
TEMP_DATA_PATH = Path(gettempdir()) / "data"
CACHE_PATH = Path(gettempdir()) / "cache"

def get_default_data_dir(app_name: str) -> Path:
    """
    Get the user data directory for the current system platform.

    Linux: ~/.local/share/<app_name>
    macOS: ~/Library/Application Support/<app_name>
    Windows: C:/Users/<USER>/AppData/Roaming/<app_name>

    :param app_name: Application Name will be used to specify directory
    :type app_name: str
    :return: User Data Path
    :rtype: Path
    """
    home = Path.home()

    system_paths = {
        "win32": home / f"AppData/Roaming/{app_name}",
        "linux": home / f".local/share/{app_name}",
        "darwin": home / f"Library/Application Support/{app_name}",
    }

    data_path = system_paths[sys.platform]
    return data_path

DEFAULT_CONFIG = {
    "ENV": "development",
    "OLLAMA_HOST": "localhost:11434",
    "BASEDIR": os.path.abspath(os.path.dirname(__file__)),
    "USE_DATABASE": "false",
    "SCHEMA_FILE": "schema.sql",
    "DATABASE_PATH": os.environ.get("DATABASE_PATH", "embedder.sqlite"),
    "DATABASE_URL": os.environ.get("DATABASE_URL", "sqlite:///embedder.sqlite"),
    "OLLAMA_URL": os.environ.get("OLLAMA_URL", "http://127.0.0.1:5000"),
    "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama3.1"),
    "DATA_DIR": Path(get_default_data_dir("embedder")),
    "LOG_FILE": str(os.environ.get("LOG_FILENAME", "embedder.log")),
    "LOG_LEVEL": str(os.environ.get("LOG_LEVEL", "embedder.log")),
}


class Config(dict):
    def __init__(self, config_path: Path, **defaults: Any):
        self.config_path = config_path
        print(f"Config path: {config_path}")
        if self._exists():
            self._read()
            has_new_config = False
            for key, value in defaults.items():
                if key not in self:
                    has_new_config = True
                    self[key] = value
                    print("Key: {key} Value:{value}")
            if has_new_config:
                self._write()
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            super().__init__(**defaults)
            self._write()
        setup_logging(self["LOG_LEVEL"])

    def _exists(self) -> bool:
        return os.path.isfile(self.config_path)

    def _write(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as file:
            string_config = ""
            for key, value in self.items():
                string_config += f"{key}={value}\n"
            file.write(string_config)

    def _read(self) -> None:
        with open(self.config_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    self[key] = value

    def get(self, key: str) -> str:  # type: ignore
        # Prioritize environment variables over config file.
        value = super().get(key) or os.getenv(key)
        if not value:
            raise UsageError(f"Missing config key: {key}")
        return value

    def setup_logging(self, default_level:str=logging.INFO):
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                },
                "file": {
                    "level": "DEBUG",
                    "class": "logging.FileHandler",
                    "filename": "app.log",
                    "formatter": "standard",
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": default_level,
            },
        }
        logging.config.dictConfig(log_config)


class DatabaseHandler(Handler):
    def __init__(self, db_file: str = "embedder_log.sqlite"):
        super().__init__()
        self.db_file = db_file
        self.db_file = connect(self.db_file)
        self.db_file.execute(
            "CREATE TABLE IF NOT EXISTS logs (date TEXT, "
            "time TEXT, lvl INTEGER, lvl_name TEXT, msg TEXT, "
            "logger TEXT, lineno INTEGER)"
        )

    def emit(self, record):
        """
        Conditionally emit the specified logging record.

        Emission depends on filters which may have been added to the handler.
        Wrap the actual emission of the record with acquisition/release of
        the I/O thread lock. Returns whether the filter passed the record for
        emission.
        """
        self.db_file.execute(
            "INSERT INTO logs VALUES (:1,:2,:3,:4, :5, :6, :7)",
            (
                date_time.now().strftime("%A, the %d of %B, %Y"),
                date_time.now().strftime("%I:%M %p"),
                record.levelno,
                record.levelname,
                record.msg,
                record.name,
                record.lineno,
            ),
        )
        self.db_file.commit()
        self.db_file.close()







appConfig = Config(EMBEDDER_CONFIG_FOLDER, **DEFAULT_CONFIG)
