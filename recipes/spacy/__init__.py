from __future__ import annotations

from kivy_ios.toolchain import CythonRecipe


class SpacyRecipe(CythonRecipe):
    version = "3.8.11"
    url = "https://files.pythonhosted.org/packages/source/s/spacy/spacy-{version}.tar.gz"
    depends = [
        "python3",
        "numpy",
        "cymem",
        "preshed",
        "thinc",
        "blis",
        "murmurhash",
        "srsly",
        "pydantic",
    ]

    def prebuild_platform(self, plat):
        super().prebuild_platform(plat)
        if self.has_marker("pydantic_patched"):
            return
        self.apply_patch("pydantic-beta.patch")
        self.set_marker("pydantic_patched")


recipe = SpacyRecipe()

