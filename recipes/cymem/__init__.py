from kivy_ios.toolchain import CythonRecipe


class CymemRecipe(CythonRecipe):
    version = "2.0.13"
    url = "https://files.pythonhosted.org/packages/source/c/cymem/cymem-{version}.tar.gz"
    depends = ["python3"]


recipe = CymemRecipe()

