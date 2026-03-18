from __future__ import annotations

import sh
from fnmatch import filter as fnmatch_filter
from os import walk
from os.path import join

from kivy_ios.toolchain import CythonRecipe, shprint


class PreshedRecipe(CythonRecipe):
    version = "3.0.12"
    url = "https://files.pythonhosted.org/packages/source/p/preshed/preshed-{version}.tar.gz"
    depends = ["python3", "cymem", "murmurhash"]
    cythonize = False

    def install_hostpython_prerequisites(self):
        python = sh.Command(self.ctx.hostpython)
        shprint(
            python,
            "-m",
            "pip",
            "install",
            "cymem==2.0.13",
            "murmurhash==1.0.15",
        )
        # Use generated C sources from the sdist instead of re-cythonizing.
        shprint(python, "-m", "pip", "uninstall", "-y", "Cython")

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


recipe = PreshedRecipe()

