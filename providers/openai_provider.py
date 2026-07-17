"""
OpenAI Provider

Handles:
- Story generation
- Character generation
- Scene prompt generation
- Image generation

Author: Real Animation Studio
"""

from __future__ import annotations

import os
import json
import base64
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenAIProvider:
    """
    Wrapper around OpenAI APIs.
    """

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is missing."
            )

        self.client = OpenAI(api_key=api_key)

        self.chat_model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.5"
        )

        self.image_model = os.getenv(
            "IMAGE_MODEL",
            "gpt-image-1"
        )

    # ---------------------------------------------------------

    def chat(
        self,
        prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Generic text generation.
        """

        response = self.client.responses.create(
            model=self.chat_model,
            input=prompt,
            temperature=temperature,
        )

        return response.output_text

    # ---------------------------------------------------------

    def create_story(
        self,
        topic: str,
        language: str = "English",
        duration: str = "short",
    ) -> str:

        prompt = f"""
You are an award-winning animated movie writer.

Write a complete story.

Topic:
{topic}

Language:
{language}

Length:
{duration}

Requirements:

- Emotional

- Family Friendly

- Easy narration

- Multiple scenes

- Rich expressions

- Visual storytelling
"""

        return self.chat(prompt)

    # ---------------------------------------------------------

    def create_storyboard(
        self,
        story: str,
    ) -> List[Dict[str, Any]]:

        prompt = f"""
Convert the following story into JSON.

Return ONLY JSON.

Each scene should contain:

scene_number

title

description

camera

emotion

characters

dialog

duration

Story:

{story}
"""

        result = self.chat(prompt)

        try:
            return json.loads(result)

        except Exception:

            raise RuntimeError(
                "Storyboard JSON parsing failed."
            )

    # ---------------------------------------------------------

    def create_character_sheet(
        self,
        description: str,
    ) -> str:

        prompt = f"""
Create a complete animated character sheet.

Character:

{description}

Include:

Face

Hair

Eyes

Body

Dress

Shoes

Accessories

Colors

Personality

Keep the appearance consistent across all scenes.
"""

        return self.chat(prompt)

    # ---------------------------------------------------------

    def create_scene_prompt(
        self,
        scene: Dict[str, Any],
        character_sheet: str,
    ) -> str:

        prompt = f"""
Generate a cinematic image prompt.

Character Sheet:

{character_sheet}

Scene:

{json.dumps(scene, indent=2)}

Requirements:

Pixar quality

3D animation

Cinematic lighting

Soft shadows

Natural pose

Same costume

Same face

Highly detailed

No text

Ultra HD
"""

        return self.chat(prompt)

    # ---------------------------------------------------------

    def generate_image(
        self,
        prompt: str,
        output_file: str,
        size: str = "1024x1536",
    ) -> Path:
        """
        Generate a scene image.
        """

        response = self.client.images.generate(
            model=self.image_model,
            prompt=prompt,
            size=size,
        )

        image_b64 = response.data[0].b64_json

        image_bytes = base64.b64decode(image_b64)

        path = Path(output_file)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_bytes(image_bytes)

        return path

    # ---------------------------------------------------------

    def health_check(self):

        self.chat("Say hello.")

        return True
