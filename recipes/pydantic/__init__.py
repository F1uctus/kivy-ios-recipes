from kivy_ios.toolchain import PythonRecipe


class PydanticRecipe(PythonRecipe):
    version = "2.13.0b2"
    url = "https://github.com/pydantic/pydantic/archive/refs/tags/v{version}.zip"
    depends = ["python3", "pydantic-core"]


recipe = PydanticRecipe()

