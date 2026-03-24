from kivy_ios.toolchain import PythonRecipe


class TypingExtensionsRecipe(PythonRecipe):
    version = "4.15.0"
    url = "https://files.pythonhosted.org/packages/source/t/typing-extensions/typing_extensions-{version}.tar.gz"
    depends = ["python3"]


recipe = TypingExtensionsRecipe()
