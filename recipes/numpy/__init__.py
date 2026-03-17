from kivy_ios.toolchain import CythonRecipe


class NumpyRecipe(CythonRecipe):
    version = "2.3.0"
    url = "https://pypi.python.org/packages/source/n/numpy/numpy-{version}.tar.gz"
    depends = ["python3"]


recipe = NumpyRecipe()

