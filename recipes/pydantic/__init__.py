import sh
from kivy_ios.context_managers import cd

from kivy_ios.toolchain import PythonRecipe, shprint


class PydanticRecipe(PythonRecipe):
    version = "2.13.0b2"
    url = "https://github.com/pydantic/pydantic/archive/refs/tags/v{version}.zip"
    depends = ["python3", "pydantic-core"]

    def install(self):
        plat = list(self.platforms_to_build)[0]
        env = self.get_recipe_env(plat)
        build_dir = self.get_build_dir(plat)
        with cd(build_dir):
            shprint(
                sh.Command(self.ctx.hostpython),
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--prefix",
                self.ctx.python_prefix,
                ".",
                _env=env,
            )


recipe = PydanticRecipe()

