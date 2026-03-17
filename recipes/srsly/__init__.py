from kivy_ios.toolchain import CythonRecipe


class SrslyRecipe(CythonRecipe):
    version = "2.5.2"
    url = "https://files.pythonhosted.org/packages/source/s/srsly/srsly-{version}.tar.gz"
    depends = ["python3"]


recipe = SrslyRecipe()

