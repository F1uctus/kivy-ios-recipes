import sh

from kivy_ios.toolchain import PythonRecipe, shprint


class CatalogueRecipe(PythonRecipe):
    version = "2.0.10"
    url = "https://files.pythonhosted.org/packages/source/c/catalogue/catalogue-{version}.tar.gz"
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
            f"catalogue=={self.version}",
        )


recipe = CatalogueRecipe()
