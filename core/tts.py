"""
TTS Engine

Uses OpenAI Text-to-Speech API to generate narration.

Author:
Real Animation Studio
"""

from pathlib import Path
from typing import List

from loguru import logger

from providers.openai_provider import OpenAIProvider


class TTSEngine:

    def __init__(self):

        self.ai = OpenAIProvider()

        self.output_dir = Path("output/audio")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------------------

    def generate_audio(

        self,

        text: str,

        output: Path,

        voice: str = "alloy",

    ) -> Path:

        logger.info(

            f"Generating narration: {output.name}"

        )

        self.ai.text_to_speech(

            text=text,

            voice=voice,

            output=output,

        )

        return output

    # -----------------------------------------------------

    def scene_audio(

        self,

        scene_number: int,

        narration: str,

        voice: str = "alloy",

    ) -> Path:

        filename = (

            self.output_dir

            / f"scene_{scene_number:03}.mp3"

        )

        return self.generate_audio(

            narration,

            filename,

            voice,

        )

    # -----------------------------------------------------

    def generate_story_audio(

        self,

        storyboard: List[dict],

        voice: str = "alloy",

    ):

        files = []

        for index, scene in enumerate(

            storyboard,

            start=1,

        ):

            text = scene.get(

                "dialog",

                scene.get(

                    "description",

                    ""

                ),

            )

            audio = self.scene_audio(

                index,

                text,

                voice,

            )

            files.append(audio)

        return files

    # -----------------------------------------------------

    def combine_script(

        self,

        storyboard: List[dict],

    ) -> str:

        narration = []

        for scene in storyboard:

            narration.append(

                scene.get(

                    "dialog",

                    scene.get(

                        "description",

                        ""

                    )

                )

            )

        return "\n".join(narration)

    # -----------------------------------------------------

    def full_story_audio(

        self,

        storyboard,

        voice="alloy",

    ):

        output = self.output_dir / "full_story.mp3"

        narration = self.combine_script(

            storyboard

        )

        return self.generate_audio(

            narration,

            output,

            voice,

        )


if __name__ == "__main__":

    engine = TTSEngine()

    storyboard = [

        {

            "dialog":

            "Once upon a time there was a little rabbit."

        },

        {

            "dialog":

            "The rabbit met a tiger cub."

        },

        {

            "dialog":

            "They became best friends."

        }

    ]

    engine.generate_story_audio(

        storyboard

    )

    engine.full_story_audio(

        storyboard

    )
