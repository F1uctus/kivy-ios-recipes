from __future__ import annotations

import sh
from fnmatch import filter as fnmatch_filter
from os import walk
from os.path import join
from pathlib import Path

from kivy_ios.toolchain import CythonRecipe, shprint


class SpacyRecipe(CythonRecipe):
    cythonize = False
    version = "3.8.11"
    url = "https://files.pythonhosted.org/packages/source/s/spacy/spacy-{version}.tar.gz"
    depends = [
        "python3",
        "cymem",
        "preshed",
        "thinc",
        "blis",
        "murmurhash",
        "srsly",
        "pydantic",
    ]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        # SpaCy 3.8.x has Cython parser incompatibilities with newer Cython in
        # this toolchain context; keep a 0.29.x build-time Cython for spaCy.
        shprint(python, "-m", "pip", "install", "Cython==0.29.37")

    def biglink(self):
        dirs = []
        for root, _, filenames in walk(self.build_dir):
            if fnmatch_filter(filenames, "*.so.libs"):
                dirs.append(root)
        if not dirs:
            return
        cmd = sh.Command(join(self.ctx.root_dir, "tools", "biglink"))
        shprint(cmd, join(self.build_dir, f"lib{self.name}.a"), *dirs)

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        site_packages = self.ctx.site_packages_dir
        current = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            f"{site_packages}:{current}" if current else site_packages
        )
        env["CYTHON_INCLUDE_PATH"] = site_packages
        return env

    def prebuild_platform(self, plat):
        super().prebuild_platform(plat)
        python = sh.Command(self.ctx.hostpython)
        # Earlier recipes may reinstall Cython 3.x; pin again right before
        # spaCy build so Cython API/parser behavior stays stable.
        shprint(python, "-m", "pip", "install", "Cython==0.29.37")
        # Cython 0.29 rejects const assignment in this declaration while
        # compiling spaCy's pxd graph under our toolchain context.
        token_pxd = Path(self.build_dir) / "spacy" / "tokens" / "token.pxd"
        if token_pxd.exists():
            token_content = token_pxd.read_text()
            token_content = token_content.replace(
                "cdef const int MISSING_DEP = 0",
                "cdef int MISSING_DEP = 0",
            )
            token_pxd.write_text(token_content)
        if self.has_marker("pydantic_patched"):
            return
        self.apply_patch("pydantic-beta.patch")
        self.set_marker("pydantic_patched")


recipe = SpacyRecipe()

