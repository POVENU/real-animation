"""
Storyboard Generator
Creates story, storyboard, scene metadata and character list.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

from loguru import logger

from providers.openai_provider import OpenAIProvider
from core.utils import save_json


class StoryboardEngine:

    def __init__(self):

        self.ai = OpenAIProvider()

    # --------------------------------------------------------

    def generate_story(
        self,
        topic: str,
        language: str = "English",
        duration: str = "short",
    ) -> str:

        logger.info("Generating Story...")

        return self.ai.create_story(
            topic=topic,
            language=language,
            duration=duration,
        )

    # --------------------------------------------------------

    def generate_storyboard(
        self,
        story: str,
    ) -> List[Dict[str, Any]]:

        logger.info("Generating Storyboard...")

        storyboard = self.ai.create_storyboard(story)

        return storyboard

    # --------------------------------------------------------

    def extract_characters(
        self,
        storyboard: List[Dict[str, Any]],
    ) -> List[str]:

        characters = []

        for scene in storyboard:

            for char in scene.get("characters", []):

                if char not in characters:

                    characters.append(char)

        logger.info(
            f"Found {len(characters)} characters"
        )

        return characters

    # --------------------------------------------------------

    def estimate_duration(
        self,
        storyboard,
    ):

        total = 0

        for scene in storyboard:

            total += int(
                scene.get("duration", 8)
            )

        return total

    # --------------------------------------------------------

    def generate_character_sheets(
        self,
        characters,
    ):

        sheets = {}

        for character in characters:

            logger.info(
                f"Generating Character Sheet: {character}"
            )

            sheet = self.ai.create_character_sheet(
                character
            )

            sheets[character] = sheet

        return sheets

    # --------------------------------------------------------

    def generate_scene_prompts(
        self,
        storyboard,
        character_sheets,
    ):

        prompts = []

        for scene in storyboard:

            prompt = self.ai.create_scene_prompt(

                scene,

                "\n\n".join(character_sheets.values())

            )

            prompts.append(prompt)

        return prompts

    # --------------------------------------------------------

    def save_project(
        self,
        story,
        storyboard,
        characters,
        character_sheets,
        prompts,
    ):

        project = {

            "story": story,

            "storyboard": storyboard,

            "characters": characters,

            "character_sheets": character_sheets,

            "scene_prompts": prompts,

        }

        save_json(
            project,
            "output/project.json",
        )

        logger.success(
            "Project saved."
        )

    # --------------------------------------------------------

    def create_project(
        self,
        topic,
        language="English",
        duration="short",
    ):

        story = self.generate_story(

            topic,

            language,

            duration,

        )

        storyboard = self.generate_storyboard(

            story

        )

        characters = self.extract_characters(

            storyboard

        )

        character_sheets = self.generate_character_sheets(

            characters

        )

        prompts = self.generate_scene_prompts(

            storyboard,

            character_sheets,

        )

        self.save_project(

            story,

            storyboard,

            characters,

            character_sheets,

            prompts,

        )

        logger.success("Storyboard Complete")

        logger.info(

            f"Estimated Runtime : "

            f"{self.estimate_duration(storyboard)} sec"

        )

        return {

            "story": story,

            "storyboard": storyboard,

            "characters": characters,

            "character_sheets": character_sheets,

            "scene_prompts": prompts,

        }


if __name__ == "__main__":

    engine = StoryboardEngine()

    engine.create_project(

        topic="A rabbit saves a lost tiger cub in a magical forest.",

        language="English",

        duration="short",

    )
