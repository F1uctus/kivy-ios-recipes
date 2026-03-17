from __future__ import annotations

import sh

from kivy_ios.toolchain import CythonRecipe, shprint


class BlisRecipe(CythonRecipe):
    version = "1.3.3"
    url = "https://files.pythonhosted.org/packages/source/b/blis/blis-{version}.tar.gz"
    depends = ["python3"]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "numpy==2.3.0")

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        env["BLIS_ARCH"] = "x86_64" if plat.arch == "x86_64" else "generic"
        return env


recipe = BlisRecipe()

