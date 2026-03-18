import sh
from fnmatch import filter as fnmatch_filter
from os import walk
from os.path import join

from kivy_ios.toolchain import CythonRecipe, shprint


class MurmurhashRecipe(CythonRecipe):
    version = "1.0.15"
    url = "https://files.pythonhosted.org/packages/source/m/murmurhash/murmurhash-{version}.tar.gz"
    depends = ["python3"]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "Cython==3.0.11")

    def biglink(self):
        dirs = []
        for root, _, filenames in walk(self.build_dir):
            if fnmatch_filter(filenames, "*.so.libs"):
                dirs.append(root)
        if not dirs:
            return
        cmd = sh.Command(join(self.ctx.root_dir, "tools", "biglink"))
        shprint(cmd, join(self.build_dir, f"lib{self.name}.a"), *dirs)


recipe = MurmurhashRecipe()

