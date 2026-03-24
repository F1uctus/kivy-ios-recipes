import sh

from kivy_ios.toolchain import PythonRecipe, shprint


class TypingExtensionsRecipe(PythonRecipe):
    version = "4.15.0"
    url = "https://files.pythonhosted.org/packages/source/t/typing-extensions/typing_extensions-{version}.tar.gz"
    depends = ["python3"]

    def install(self):
        # typing_extensions is pure Python and can be installed directly into
        # the built site-packages without a setup.py build step.
        shprint(
            sh.Command(self.ctx.hostpython),
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--target",
            self.ctx.site_packages_dir,
            f"typing_extensions=={self.version}",
        )


recipe = TypingExtensionsRecipe()
