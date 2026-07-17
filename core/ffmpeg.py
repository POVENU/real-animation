"""
FFmpeg Engine

Responsible for:

- Merge Scene Videos
- Add Background Audio
- Burn Subtitles
- Export Final MP4

Author:
Real Animation Studio
"""

from pathlib import Path
from typing import List
import subprocess

from loguru import logger


class FFmpegEngine:

    def __init__(self):

        self.output_dir = Path("output")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -------------------------------------------------------

    def create_concat_file(
        self,
        videos: List[Path],
        concat_file: Path,
    ):

        concat_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            concat_file,
            "w",
            encoding="utf8",
        ) as fp:

            for video in videos:

                fp.write(
                    f"file '{video.resolve()}'\n"
                )

        return concat_file

    # -------------------------------------------------------

    def merge_videos(
        self,
        videos: List[Path],
        output: Path,
    ) -> Path:

        concat = Path("temp/videos.txt")

        self.create_concat_file(
            videos,
            concat,
        )

        command = [

            "ffmpeg",

            "-y",

            "-f",

            "concat",

            "-safe",

            "0",

            "-i",

            str(concat),

            "-c",

            "copy",

            str(output),

        ]

        logger.info(
            "Merging scene videos..."
        )

        subprocess.run(
            command,
            check=True,
        )

        return output

    # -------------------------------------------------------

    def add_audio(
        self,
        video: Path,
        audio: Path,
        output: Path,
    ) -> Path:

        command = [

            "ffmpeg",

            "-y",

            "-i",

            str(video),

            "-i",

            str(audio),

            "-c:v",

            "copy",

            "-c:a",

            "aac",

            "-shortest",

            str(output),

        ]

        logger.info(
            "Adding narration..."
        )

        subprocess.run(
            command,
            check=True,
        )

        return output

    # -------------------------------------------------------

    def burn_subtitles(
        self,
        video: Path,
        subtitles: Path,
        output: Path,
    ) -> Path:

        command = [

            "ffmpeg",

            "-y",

            "-i",

            str(video),

            "-vf",

            f"subtitles={subtitles}",

            "-c:a",

            "copy",

            str(output),

        ]

        logger.info(
            "Burning subtitles..."
        )

        subprocess.run(
            command,
            check=True,
        )

        return output

    # -------------------------------------------------------

    def build_movie(
        self,
        videos: List[Path],
        audio: Path | None = None,
        subtitles: Path | None = None,
    ) -> Path:

        merged = self.output_dir / "movie.mp4"

        self.merge_videos(
            videos,
            merged,
        )

        current = merged

        if audio:

            audio_video = self.output_dir / "movie_audio.mp4"

            self.add_audio(
                current,
                audio,
                audio_video,
            )

            current = audio_video

        if subtitles:

            subtitle_video = self.output_dir / "movie_final.mp4"

            self.burn_subtitles(
                current,
                subtitles,
                subtitle_video,
            )

            current = subtitle_video

        logger.success(
            f"Movie exported: {current}"
        )

        return current


if __name__ == "__main__":

    engine = FFmpegEngine()

    videos = [

        Path("output/video/scene_001.mp4"),

        Path("output/video/scene_002.mp4"),

        Path("output/video/scene_003.mp4"),

    ]

    audio = Path(
        "output/audio/final_audio.mp3"
    )

    subtitles = Path(
        "output/subtitles/movie.srt"
    )

    engine.build_movie(

        videos,

        audio,

        subtitles,

    )
