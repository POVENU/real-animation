"""
Video Generator

Converts scene images into animated video clips
using the configured video provider.

Author:
Real Animation Studio
"""

from pathlib import Path
from typing import List

from loguru import logger

from providers.kling_provider import KlingProvider


class VideoGenerator:

    def __init__(self):

        self.provider = KlingProvider()

        self.output_dir = Path("output/video")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ----------------------------------------------------

    def render_scene(
        self,
        image: Path,
        prompt: str,
        duration: int = 5,
    ) -> Path:

        logger.info(
            f"Rendering {image.name}"
        )

        job = self.provider.image_to_video(
            image=image,
            prompt=prompt,
            duration=duration,
        )

        output = (
            self.output_dir
            / f"{image.stem}.mp4"
        )

        self.provider.download_video(
            job,
            output,
        )

        logger.success(
            f"Finished {output.name}"
        )

        return output

    # ----------------------------------------------------

    def render_project(
        self,
        images: List[Path],
        prompts: List[str],
        duration: int = 5,
    ) -> List[Path]:

        videos = []

        for image, prompt in zip(images, prompts):

            video = self.render_scene(
                image=image,
                prompt=prompt,
                duration=duration,
            )

            videos.append(video)

        return videos

    # ----------------------------------------------------

    def render_storyboard(
        self,
        storyboard: list,
        images: List[Path],
    ) -> List[Path]:

        videos = []

        for scene, image in zip(
            storyboard,
            images,
        ):

            prompt = scene.get(
                "description",
                "",
            )

            duration = int(
                scene.get(
                    "duration",
                    5,
                )
            )

            video = self.render_scene(
                image=image,
                prompt=prompt,
                duration=duration,
            )

            videos.append(video)

        return videos

    # ----------------------------------------------------

    def verify_output(
        self,
        videos: List[Path],
    ) -> bool:

        for video in videos:

            if not video.exists():

                logger.error(
                    f"Missing: {video}"
                )

                return False

        return True


if __name__ == "__main__":

    generator = VideoGenerator()

    images = [

        Path("output/images/scene_001.png"),

        Path("output/images/scene_002.png"),

        Path("output/images/scene_003.png"),

    ]

    prompts = [

        "Rabbit walking through magical forest.",

        "Tiger appears behind rabbit.",

        "Rabbit smiles.",

    ]

    videos = generator.render_project(

        images,

        prompts,

    )

    print(videos)
