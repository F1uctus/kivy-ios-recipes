from __future__ import annotations

from kivy_ios.toolchain import CythonRecipe


class ThincRecipe(CythonRecipe):
    version = "8.3.10"
    url = "https://files.pythonhosted.org/packages/source/t/thinc/thinc-{version}.tar.gz"
    depends = [
        "python3",
        "numpy",
        "murmurhash",
        "cymem",
        "preshed",
        "blis",
        "srsly",
        "pydantic",
    ]

    def prebuild_platform(self, plat):
        super().prebuild_platform(plat)
        if self.has_marker("pydantic_patched"):
            return
        self.apply_patch("pydantic-beta.patch")
        self.set_marker("pydantic_patched")


recipe = ThincRecipe()

