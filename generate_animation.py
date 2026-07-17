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

        return self.subtitle.create_story_srt(

            project["storyboard"]

        )
