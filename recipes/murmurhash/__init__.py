from kivy_ios.toolchain import CythonRecipe


class MurmurhashRecipe(CythonRecipe):
    version = "1.0.15"
    url = "https://files.pythonhosted.org/packages/source/m/murmurhash/murmurhash-{version}.tar.gz"
    depends = ["python3"]


recipe = MurmurhashRecipe()

