"""
Base Provider Interface

All AI providers inherit from this class.

Providers:
    - OpenAI
    - Kling
    - Runway
    - Veo
    - PixVerse

Author:
    Real Animation Studio
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseProvider(ABC):

    def __init__(self, config: dict):

        self.config = config

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify API connectivity.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_story(
        self,
        topic: str,
        language: str,
        duration: str,
    ) -> str:
        """
        Generate story.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_character_sheet(
        self,
        description: str,
    ) -> str:
        """
        Create character sheet.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_scene_prompt(
        self,
        scene: dict,
        character_sheet: str,
    ) -> str:
        """
        Create image prompt.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        output_file: Path,
    ) -> Path:
        """
        Generate image.
        """
        raise NotImplementedError

    @abstractmethod
    def image_to_video(
        self,
        image: Path,
        prompt: str,
        duration: int,
    ) -> Any:
        """
        Convert image into animation.
        """
        raise NotImplementedError

    @abstractmethod
    def download_video(
        self,
        job_id: str,
        output: Path,
    ) -> Path:
        """
        Download rendered video.
        """
        raise NotImplementedError

    @abstractmethod
    def text_to_speech(
        self,
        text: str,
        voice: str,
        output: Path,
    ) -> Path:
        """
        Generate narration.
        """
        raise NotImplementedError
