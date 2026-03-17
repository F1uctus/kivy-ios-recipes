from kivy_ios.toolchain import PythonRecipe


class RequestsRecipe(PythonRecipe):
    version = "2.32.5"
    url = "https://files.pythonhosted.org/packages/source/r/requests/requests-{version}.tar.gz"
    depends = ["python3"]


recipe = RequestsRecipe()

