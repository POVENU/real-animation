"""
Subtitle Generator

Creates SRT subtitle files for the rendered movie.

Author:
Real Animation Studio
"""

from pathlib import Path
from typing import List

import srt
from datetime import timedelta

from loguru import logger


class SubtitleGenerator:

    def __init__(self):

        self.output_dir = Path("output/subtitles")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------------------

    def create_scene_srt(

        self,

        scene_number: int,

        text: str,

        duration: int,

    ) -> Path:

        output = (

            self.output_dir

            / f"scene_{scene_number:03}.srt"

        )

        subtitle = srt.Subtitle(

            index=1,

            start=timedelta(seconds=0),

            end=timedelta(seconds=duration),

            content=text,

        )

        with open(

            output,

            "w",

            encoding="utf8",

        ) as fp:

            fp.write(

                srt.compose([subtitle])

            )

        logger.info(

            f"Created {output.name}"

        )

        return output

    # -----------------------------------------------------

    def create_story_srt(

        self,

        storyboard: List[dict],

    ) -> Path:

        subtitles = []

        current = 0

        index = 1

        for scene in storyboard:

            duration = int(

                scene.get(

                    "duration",

                    5,

                )

            )

            text = scene.get(

                "dialog",

                scene.get(

                    "description",

                    "",

                )

            )

            subtitles.append(

                srt.Subtitle(

                    index=index,

                    start=timedelta(

                        seconds=current

                    ),

                    end=timedelta(

                        seconds=current + duration

                    ),

                    content=text,

                )

            )

            current += duration

            index += 1

        output = (

            self.output_dir

            / "movie.srt"

        )

        with open(

            output,

            "w",

            encoding="utf8",

        ) as fp:

            fp.write(

                srt.compose(subtitles)

            )

        logger.success(

            "Movie subtitle generated."

        )

        return output

    # -----------------------------------------------------

    def create_from_dialogues(

        self,

        dialogues: List[str],

        duration: int = 5,

    ) -> Path:

        storyboard = []

        for line in dialogues:

            storyboard.append(

                {

                    "dialog": line,

                    "duration": duration,

                }

            )

        return self.create_story_srt(

            storyboard

        )


if __name__ == "__main__":

    subtitles = SubtitleGenerator()

    demo = [

        {

            "dialog":

            "Once upon a time there lived a rabbit.",

            "duration": 6,

        },

        {

            "dialog":

            "He met a tiger cub in the forest.",

            "duration": 7,

        },

        {

            "dialog":

            "They became best friends.",

            "duration": 5,

        },

    ]

    subtitles.create_story_srt(

        demo

    )
