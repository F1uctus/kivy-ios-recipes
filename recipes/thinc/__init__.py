from __future__ import annotations

import sh
from fnmatch import filter as fnmatch_filter
from os import walk
from os.path import join

from kivy_ios.toolchain import CythonRecipe, shprint


class ThincRecipe(CythonRecipe):
    cythonize = False
    version = "8.3.10"
    url = "https://files.pythonhosted.org/packages/source/t/thinc/thinc-{version}.tar.gz"
    depends = [
        "python3",
        "murmurhash",
        "cymem",
        "preshed",
        "blis",
        "srsly",
        "pydantic",
        "catalogue",
        "confection",
    ]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "Cython==3.0.11")
        # Thinc cimports `blis.cy` during Cythonization; ensure hostpython has
        # the pinned blis package available so `blis/cy.pxd` resolves.
        shprint(python, "-m", "pip", "install", "blis==1.3.3")

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        site_packages = self.ctx.site_packages_dir
        current = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            f"{site_packages}:{current}" if current else site_packages
        )
        return env

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

