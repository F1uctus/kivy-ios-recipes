import sh

from kivy_ios.toolchain import PythonRecipe, shprint


class ConfectionRecipe(PythonRecipe):
    version = "0.1.5"
    url = "https://files.pythonhosted.org/packages/source/c/confection/confection-{version}.tar.gz"
    depends = ["python3"]

    def install(self):
        shprint(
            sh.Command(self.ctx.hostpython),
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--target",
            self.ctx.site_packages_dir,
            f"confection=={self.version}",
        )


recipe = ConfectionRecipe()
