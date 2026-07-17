"""
Utility functions for Real Animation Studio.
"""

from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.progress import Progress


load_dotenv()

console = Console()


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "animation.log",
    rotation="10 MB",
    retention=10,
    enqueue=True,
)

logger.add(
    lambda msg: console.print(msg, end=""),
)


# ---------------------------------------------------------------------
# YAML
# ---------------------------------------------------------------------

def load_yaml(path: str | Path) -> dict:
    """
    Load YAML file.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------

def save_json(data: Any, file: str | Path):

    file = Path(file)

    file.parent.mkdir(parents=True, exist_ok=True)

    with open(file, "w", encoding="utf8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )


# ---------------------------------------------------------------------

def load_json(file: str | Path):

    with open(file, "r", encoding="utf8") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------

def ensure_directories():

    folders = [

        "output",

        "temp",

        "logs",

        "assets",

        "output/images",

        "output/video",

        "output/audio",

        "output/subtitles",

    ]

    for folder in folders:
        Path(folder).mkdir(
            parents=True,
            exist_ok=True,
        )


# ---------------------------------------------------------------------

def clean_temp():

    if Path("temp").exists():

        shutil.rmtree("temp")

    Path("temp").mkdir()


# ---------------------------------------------------------------------
# Timer
# ---------------------------------------------------------------------

class Timer:

    def __init__(self):

        self.start = None

    def __enter__(self):

        self.start = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        elapsed = time.time() - self.start

        logger.info(
            f"Finished in {elapsed:.2f} seconds"
        )


# ---------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------

def progress_bar():

    return Progress()


# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------

class Config:

    def __init__(self):

        self.data = load_yaml(
            "config/config.yaml"
        )

    def get(
        self,
        *keys,
        default=None,
    ):

        node = self.data

        for key in keys:

            if isinstance(node, dict):

                node = node.get(key)

            else:

                return default

            if node is None:

                return default

        return node


config = Config()


# ---------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------

def env(name: str, default=None):

    return os.getenv(name, default)


# ---------------------------------------------------------------------
# Slug
# ---------------------------------------------------------------------

def slug(text: str):

    return (

        text.lower()

        .replace(" ", "_")

        .replace("/", "_")

        .replace("\\", "_")

    )


# ---------------------------------------------------------------------
# Retry
# ---------------------------------------------------------------------

def retry(
    func,
    retries=3,
    delay=5,
):

    for attempt in range(retries):

        try:

            return func()

        except Exception as ex:

            logger.error(ex)

            if attempt == retries - 1:

                raise

            time.sleep(delay)


# ---------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------

def banner():

    console.rule("[bold blue]Real Animation Studio")
