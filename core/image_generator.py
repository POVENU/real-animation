"""
Image Generator

Generates:

- Character Reference Images
- Scene Images
- Maintains Character Consistency

Author:
Real Animation Studio
"""

from pathlib import Path
from typing import Dict, List

from loguru import logger

from providers.openai_provider import OpenAIProvider
from core.character_manager import CharacterManager


class ImageGenerator:

    def __init__(self):

        self.ai = OpenAIProvider()

        self.character_manager = CharacterManager()

        self.output_dir = Path("output/images")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------------------------------

    def generate_character_reference(

        self,

        name: str,

        sheet: str,

    ) -> Path:

        logger.info(
            f"Generating reference image : {name}"
        )

        filename = (

            self.output_dir

            / f"{name.lower()}_reference.png"

        )

        self.ai.generate_image(

            prompt=sheet,

            output_file=str(filename),

            size="1024x1536",

        )

        self.character_manager.add_character(

            name,

            sheet,

        )

        self.character_manager.update_reference_image(

            name,

            str(filename),

        )

        return filename

    # ---------------------------------------------------------

    def generate_scene_image(

        self,

        scene_number: int,

        prompt: str,

    ) -> Path:

        logger.info(

            f"Generating Scene {scene_number}"

        )

        filename = (

            self.output_dir

            / f"scene_{scene_number:03}.png"

        )

        self.ai.generate_image(

            prompt,

            str(filename),

            size="1024x1536",

        )

        return filename

    # ---------------------------------------------------------

    def generate_all_characters(

        self,

        character_sheets: Dict[str, str],

    ):

        references = {}

        for name, sheet in character_sheets.items():

            image = self.generate_character_reference(

                name,

                sheet,

            )

            references[name] = image

        self.character_manager.save()

        return references

    # ---------------------------------------------------------

    def generate_all_scenes(

        self,

        prompts: List[str],

    ):

        images = []

        for index, prompt in enumerate(

            prompts,

            start=1,

        ):

            image = self.generate_scene_image(

                index,

                prompt,

            )

            images.append(image)

        return images

    # ---------------------------------------------------------

    def create_project_images(

        self,

        character_sheets,

        prompts,

    ):

        logger.info(

            "Generating Character Images"

        )

        self.generate_all_characters(

            character_sheets

        )

        logger.info(

            "Generating Scene Images"

        )

        return self.generate_all_scenes(

            prompts

        )


if __name__ == "__main__":

    generator = ImageGenerator()

    sheets = {

        "Rabbit":

            """
            Cute white rabbit

            Blue scarf

            Big eyes

            Pixar style

            """,

        "Tiger":

            """
            Cute tiger cub

            Orange fur

            Pixar style

            """

    }

    prompts = [

        "Rabbit walking inside magical forest.",

        "Tiger meets Rabbit.",

        "Rabbit hugs Tiger.",

    ]

    generator.create_project_images(

        sheets,

        prompts,

    )
