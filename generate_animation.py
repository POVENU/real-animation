"""
Real Animation Studio

Main Pipeline

Workflow

Story
 ↓
Storyboard
 ↓
Characters
 ↓
Images
 ↓
Kling Animation
 ↓
Voice
 ↓
Subtitles
 ↓
Movie

Author:
Venugopal
"""

from pathlib import Path
from loguru import logger
import argparse
import sys
import shutil

from core.storyboard import StoryboardEngine
from core.character_manager import CharacterManager
from core.image_generator import ImageGenerator
from core.video_generator import VideoGenerator
from core.tts import TTSEngine
from core.subtitle_generator import SubtitleGenerator
from core.audio import AudioEngine
from core.ffmpeg import FFmpegEngine

from core.utils import (

    banner,

    ensure_directories,

    clean_temp,

)

##########################################################################
# Animation Pipeline
##########################################################################

class AnimationPipeline:

    def __init__(self):

        banner()

        ensure_directories()

        self.storyboard = StoryboardEngine()

        self.characters = CharacterManager()

        self.images = ImageGenerator()

        self.video = VideoGenerator()

        self.tts = TTSEngine()

        self.subtitle = SubtitleGenerator()

        self.audio = AudioEngine()

        self.ffmpeg = FFmpegEngine()

##########################################################################

    def create_story(

        self,

        topic,

        language,

        duration,

    ):

        logger.info(

            "Generating Story..."

        )

        project = self.storyboard.create_project(

            topic=topic,

            language=language,

            duration=duration,

        )

        return project

##########################################################################

    def create_character_images(

        self,

        project,

    ):

        logger.info(

            "Generating Character Reference Images..."

        )

        return self.images.generate_all_characters(

            project["character_sheets"]

        )

##########################################################################

    def create_scene_images(

        self,

        project,

    ):

        logger.info(

            "Generating Scene Images..."

        )

        return self.images.generate_all_scenes(

            project["scene_prompts"]

        )

##########################################################################

    def animate_scenes(

        self,

        project,

        scene_images,

    ):

        logger.info(

            "Animating scenes using Kling..."

        )

        return self.video.render_storyboard(

            project["storyboard"],

            scene_images,

        )

##########################################################################

    def create_audio(

        self,

        project,

    ):

        logger.info(

            "Generating narration..."

        )

        narration = self.tts.full_story_audio(

            project["storyboard"]

        )

        return narration

##########################################################################

    def create_subtitles(

        self,

        project,

    ):

        logger.info(

            "Generating subtitles..."

        )
##########################################################################

    def create_final_audio(

        self,

        narration_file,

        background_music=None,

    ):

        logger.info(

            "Preparing final audio..."

        )

        if background_music is None:

            background_music = Path(

                "assets/music/background.mp3"

            )

        output = Path(

            "output/audio/final_audio.mp3"

        )

        if background_music.exists():

            return self.audio.merge_music(

                narration_file,

                background_music,

                output,

            )

        logger.warning(

            "Background music not found. Using narration only."

        )

        return narration_file

##########################################################################

    def build_movie(

        self,

        videos,

        audio,

        subtitles,

    ):

        logger.info(

            "Building final movie..."

        )

        return self.ffmpeg.build_movie(

            videos=videos,

            audio=audio,

            subtitles=subtitles,

        )

##########################################################################

    def run(

        self,

        topic,

        language="English",

        duration="short",

    ):

        logger.info(

            "=" * 60

        )

        logger.info(

            "REAL ANIMATION STUDIO STARTED"

        )

        logger.info(

            "=" * 60

        )

        ##################################################

        project = self.create_story(

            topic,

            language,

            duration,

        )

        ##################################################

        self.create_character_images(

            project

        )

        ##################################################

        scene_images = self.create_scene_images(

            project

        )

        ##################################################

        rendered_videos = self.animate_scenes(

            project,

            scene_images,

        )

        ##################################################

        narration = self.create_audio(

            project

        )

        ##################################################

        subtitles = self.create_subtitles(

            project

        )

        ##################################################

        final_audio = self.create_final_audio(

            narration

        )

        ##################################################

        final_movie = self.build_movie(

            rendered_videos,

            final_audio,

            subtitles,

        )

        ##################################################

        logger.success(

            "=" * 60

        )

        logger.success(

            "PROJECT COMPLETED SUCCESSFULLY"

        )

        logger.success(

            f"Output : {final_movie}"

        )

        logger.success(

            "=" * 60

        )

        return final_movie

##########################################################################

    def clean(

        self,

    ):

        logger.info(

            "Cleaning temporary files..."

        )

        clean_temp()

##########################################################################

    def verify_assets(

        self,

    ):

        folders = [

            "assets",

            "config",

            "output",

        ]

        for folder in folders:

            path = Path(folder)

            if not path.exists():

                logger.warning(

                    f"Missing folder: {folder}"

                )

        return True
     

        return self.subtitle.create_story_srt(

            project["storyboard"]

        )

##########################################################################

    def resume_project(

        self,

        project_file="output/project.json",

    ):

        import json

        file = Path(project_file)

        if not file.exists():

            logger.error(

                "No previous project found."

            )

            return None

        logger.info(

            f"Loading project: {project_file}"

        )

        with open(

            file,

            "r",

            encoding="utf8",

        ) as fp:

            project = json.load(fp)

        return project

##########################################################################

    def export_project(

        self,

        destination,

    ):

        destination = Path(destination)

        destination.mkdir(

            parents=True,

            exist_ok=True,

        )

        logger.info(

            "Exporting project..."

        )

        folders = [

            "output",

            "config",

            "logs",

        ]

        for folder in folders:

            src = Path(folder)

            dst = destination / folder

            if src.exists():

                shutil.copytree(

                    src,

                    dst,

                    dirs_exist_ok=True,

                )

        logger.success(

            "Project exported."

        )

##########################################################################

    def show_summary(

        self,

        movie,

    ):

        logger.info("")

        logger.info("=" * 70)

        logger.info("REAL ANIMATION STUDIO")

        logger.info("=" * 70)

        logger.info(f"Movie : {movie}")

        logger.info(f"Output : {Path(movie).parent}")

        logger.info("=" * 70)

##########################################################################

    def run_resume(

        self,

    ):

        project = self.resume_project()

        if project is None:

            return

        scene_images = list(

            Path("output/images").glob("scene_*.png")

        )

        rendered = self.animate_scenes(

            project,

            scene_images,

        )

        narration = self.create_audio(

            project,

        )

        subtitles = self.create_subtitles(

            project,

        )

        audio = self.create_final_audio(

            narration,

        )

        movie = self.build_movie(

            rendered,

            audio,

            subtitles,

        )

        self.show_summary(

            movie,

        )

##########################################################################

    def version(

        self,

    ):

        return "2.0.0"

##########################################################################

    def info(

        self,

    ):

        logger.info(

            f"Version : {self.version()}"

        )

        logger.info(

            "Provider : OpenAI + Kling"

        )

        logger.info(

            "Pipeline : Story -> Images -> Animation -> Audio -> Movie"

        )

##########################################################################
# CLI
##########################################################################

def build_parser():

    parser = argparse.ArgumentParser(

        description="Real Animation Studio"

    )

    parser.add_argument(

        "--topic",

        type=str,

        help="Story topic",

    )

    parser.add_argument(

        "--language",

        default="English",

    )

    parser.add_argument(

        "--duration",

        default="short",

        choices=[

            "short",

            "medium",

            "long",

        ],

    )

    parser.add_argument(

        "--resume",

        action="store_true",

    )

    parser.add_argument(

        "--export",

        type=str,

        default=None,

    )

    parser.add_argument(

        "--clean",

        action="store_true",

    )

    parser.add_argument(

        "--version",

        action="store_true",

    )

    return parser


##########################################################################

def main():

    parser = build_parser()

    args = parser.parse_args()

    pipeline = AnimationPipeline()

    if args.version:

        pipeline.info()

        sys.exit(0)

    if args.clean:

        pipeline.clean()

        logger.success(

            "Temporary files removed."

        )

        sys.exit(0)

    if args.resume:

        pipeline.run_resume()

        sys.exit(0)

    if not args.topic:

        parser.print_help()

        sys.exit(1)

    try:

        movie = pipeline.run(

            topic=args.topic,

            language=args.language,

            duration=args.duration,

        )

        if args.export:

            pipeline.export_project(

                args.export

            )

        pipeline.show_summary(

            movie

        )

    except KeyboardInterrupt:

        logger.error(

            "Cancelled by user."

        )

        sys.exit(1)

    except Exception as ex:

        logger.exception(ex)

        sys.exit(1)


##########################################################################

if __name__ == "__main__":

    main()
