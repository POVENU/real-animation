"""
Character Manager

Maintains consistent character appearance across scenes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


class CharacterManager:

    def __init__(self):

        self.characters: Dict[str, dict] = {}

    # --------------------------------------------------------

    def add_character(
        self,
        name: str,
        sheet: str,
    ):

        self.characters[name] = {

            "name": name,

            "sheet": sheet,

            "reference_image": None,

            "scene_count": 0,

            "locked": True,

        }

    # --------------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self.characters

    # --------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> dict:

        return self.characters[name]

    # --------------------------------------------------------

    def update_reference_image(
        self,
        name: str,
        image_path: str,
    ):

        if name not in self.characters:

            raise ValueError(
                f"{name} not found."
            )

        self.characters[name]["reference_image"] = image_path

    # --------------------------------------------------------

    def increase_scene_count(
        self,
        name: str,
    ):

        if name in self.characters:

            self.characters[name]["scene_count"] += 1

    # --------------------------------------------------------

    def get_reference_prompt(
        self,
        name: str,
    ) -> str:

        if name not in self.characters:

            raise ValueError(name)

        return self.characters[name]["sheet"]

    # --------------------------------------------------------

    def build_scene_prompt(
        self,
        names: List[str],
    ) -> str:

        prompt = []

        for name in names:

            if name in self.characters:

                prompt.append(

                    self.characters[name]["sheet"]

                )

        return "\n\n".join(prompt)

    # --------------------------------------------------------

    def save(
        self,
        file="output/characters.json",
    ):

        Path(file).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            file,
            "w",
            encoding="utf8",
        ) as fp:

            json.dump(

                self.characters,

                fp,

                indent=4,

                ensure_ascii=False,

            )

    # --------------------------------------------------------

    def load(
        self,
        file="output/characters.json",
    ):

        with open(
            file,
            "r",
            encoding="utf8",
        ) as fp:

            self.characters = json.load(fp)

    # --------------------------------------------------------

    def summary(self):

        print("=" * 60)

        print("Characters")

        print("=" * 60)

        for char in self.characters.values():

            print(

                f"{char['name']}"

                f" | Scenes : {char['scene_count']}"

            )

        print("=" * 60)


if __name__ == "__main__":

    manager = CharacterManager()

    manager.add_character(

        "Rabbit",

        "Small white rabbit with blue scarf.",

    )

    manager.add_character(

        "Tiger",

        "Cute orange tiger cub.",

    )

    manager.increase_scene_count("Rabbit")

    manager.summary()

    manager.save()
