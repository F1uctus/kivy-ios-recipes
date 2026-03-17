from __future__ import annotations

from kivy_ios.toolchain import CythonRecipe


class BlisRecipe(CythonRecipe):
    version = "1.3.3"
    url = "https://files.pythonhosted.org/packages/source/b/blis/blis-{version}.tar.gz"
    depends = ["python3"]

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        env["BLIS_ARCH"] = "x86_64" if plat.arch == "x86_64" else "generic"
        return env


recipe = BlisRecipe()

