from __future__ import annotations

import logging

import sh
from kivy_ios.context_managers import cd

from kivy_ios.toolchain import PythonRecipe, shprint

logger = logging.getLogger(__name__)


class PydanticCoreRecipe(PythonRecipe):
    version = "2.42.0"
    url = "https://files.pythonhosted.org/packages/source/p/pydantic-core/pydantic_core-{version}.tar.gz"
    depends = ["python3"]
    hostpython_prerequisites = ["maturin>=1.5.0"]

    def build_platform(self, plat):
        # Iterative: first use maturin to build the extension for iOS, then
        # rely on setup.py install to place it into site-packages.
        # This will likely need adjustment once CI runs.
        env = self.get_recipe_env(plat)
        shprint(sh.Command(self.ctx.hostpython), "-m", "pip", "install", "-U", "maturin", _env=env)
        # Build a wheel in-place for the target. Toolchain env provides CC/CFLAGS/LDFLAGS.
        with cd(self.build_dir):
            shprint(
                sh.Command(self.ctx.hostpython),
                "-m",
                "maturin",
                "build",
                "--release",
                "--interpreter",
                self.ctx.hostpython,
                _env=env,
            )


recipe = PydanticCoreRecipe()

