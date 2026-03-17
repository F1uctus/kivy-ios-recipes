from __future__ import annotations

from kivy_ios.toolchain import CythonRecipe


class PreshedRecipe(CythonRecipe):
    version = "3.0.12"
    url = "https://files.pythonhosted.org/packages/source/p/preshed/preshed-{version}.tar.gz"
    depends = ["python3", "cymem", "murmurhash"]


recipe = PreshedRecipe()

