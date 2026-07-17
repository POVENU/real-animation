"""
Audio Engine

- Merge narration
- Add background music
- Normalize volume
- Fade In / Fade Out

Author:
Real Animation Studio
"""

from pathlib import Path
from typing import List

from pydub import AudioSegment
from loguru import logger


class AudioEngine:

    def __init__(self):

        self.output_dir = Path("output/audio")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------------------

    def load(self, file: Path) -> AudioSegment:

        return AudioSegment.from_file(file)

    # -----------------------------------------------------

    def normalize(
        self,
        audio: AudioSegment,
    ) -> AudioSegment:

        change = -20 - audio.dBFS

        return audio.apply_gain(change)

    # -----------------------------------------------------

    def fade(
        self,
        audio: AudioSegment,
        fade_in=1000,
        fade_out=1000,
    ):

        return (

            audio

            .fade_in(fade_in)

            .fade_out(fade_out)

        )

    # -----------------------------------------------------

    def merge_music(

        self,

        narration_file: Path,

        music_file: Path,

        output: Path,

        music_volume=-20,

    ) -> Path:

        narration = self.load(

            narration_file

        )

        music = self.load(

            music_file

        )

        music = (

            music

            - abs(music_volume)

        )

        if len(music) < len(narration):

            repeat = (

                len(narration)

                // len(music)

            ) + 1

            music = music * repeat

        music = music[:len(narration)]

        final = narration.overlay(

            music

        )

        final = self.normalize(

            final

        )

        final = self.fade(

            final

        )

        output.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        final.export(

            output,

            format="mp3",

        )

        logger.success(

            f"Audio exported : {output}"

        )

        return output

    # -----------------------------------------------------

    def merge_multiple(

        self,

        narration_files: List[Path],

        output: Path,

    ):

        combined = AudioSegment.empty()

        for file in narration_files:

            combined += self.load(file)

        combined.export(

            output,

            format="mp3",

        )

        return output

    # -----------------------------------------------------

    def silence(

        self,

        seconds=2,

    ):

        return AudioSegment.silent(

            duration=seconds * 1000

        )


if __name__ == "__main__":

    engine = AudioEngine()

    narration = Path(

        "output/audio/full_story.mp3"

    )

    music = Path(

        "assets/music/background.mp3"

    )

    output = Path(

        "output/audio/final_audio.mp3"

    )

    if narration.exists() and music.exists():

        engine.merge_music(

            narration,

            music,

            output,

        )
