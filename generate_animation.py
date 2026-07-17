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
