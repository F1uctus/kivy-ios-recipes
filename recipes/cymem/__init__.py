import sh

from kivy_ios.toolchain import CythonRecipe, shprint


class CymemRecipe(CythonRecipe):
    version = "2.0.13"
    url = "https://files.pythonhosted.org/packages/source/c/cymem/cymem-{version}.tar.gz"
    depends = ["python3"]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "--upgrade", "cython")


recipe = CymemRecipe()

