from __future__ import annotations

import sh
from fnmatch import filter as fnmatch_filter
from os import walk
from os.path import join
from pathlib import Path

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
        # Preshed's setup.py still imports Cython.Build even when compiling from
        # generated C sources, so keep a compatible Cython installed.
        shprint(python, "-m", "pip", "install", "Cython==3.0.11")

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        site_packages = self.ctx.site_packages_dir
        current = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            f"{site_packages}:{current}" if current else site_packages
        )
        return env

    def prebuild_platform(self, plat):
        super().prebuild_platform(plat)
        # In CI, kivy-ios may uninstall Cython between dependency setup and
        # compilation. Preshed can build from generated C sources, so make the
        # setup import resilient when Cython is unavailable.
        setup_py = Path(self.build_dir) / "setup.py"
        if not setup_py.exists():
            return
        setup_content = setup_py.read_text()
        needle = "from Cython.Build import cythonize\n"
        replacement = (
            "try:\n"
            "    from Cython.Build import cythonize\n"
            "except ModuleNotFoundError:\n"
            "    def cythonize(modules, **kwargs):\n"
            "        return modules\n"
        )
        if needle in setup_content and "def cythonize(modules, **kwargs):" not in setup_content:
            setup_py.write_text(setup_content.replace(needle, replacement, 1))

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

