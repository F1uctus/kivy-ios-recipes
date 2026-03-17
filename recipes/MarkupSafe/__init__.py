from kivy_ios.toolchain import CythonRecipe


class MarkupSafeRecipe(CythonRecipe):
    version = "3.0.3"
    url = "https://files.pythonhosted.org/packages/7e/99/7690b6d4034fffd95959cbe0c02de8deb3098cc577c67bb6a24fe5d7caa7/markupsafe-3.0.3.tar.gz"
    depends = ["python3"]


recipe = MarkupSafeRecipe()

