from __future__ import annotations

import sh
from fnmatch import filter as fnmatch_filter
from os import walk
from os.path import join

from kivy_ios.toolchain import CythonRecipe, shprint


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

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "--upgrade", "cython")

    def biglink(self):
        dirs = []
        for root, _, filenames in walk(self.build_dir):
            if fnmatch_filter(filenames, "*.so.libs"):
                dirs.append(root)
        if not dirs:
            return
        cmd = sh.Command(join(self.ctx.root_dir, "tools", "biglink"))
        shprint(cmd, join(self.build_dir, f"lib{self.name}.a"), *dirs)

    def prebuild_platform(self, plat):
        super().prebuild_platform(plat)
        if self.has_marker("pydantic_patched"):
            return
        self.apply_patch("pydantic-beta.patch")
        self.set_marker("pydantic_patched")


recipe = ThincRecipe()

