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

    def prebuild_platform(self, plat):
        super().prebuild_platform(plat)
        # Build from generated C sources in sdist to avoid brittle transitive
        # Cython .pxd resolution across spaCy stack recipes.
        setup_py = Path(self.build_dir) / "setup.py"
        if setup_py.exists():
            setup_content = setup_py.read_text()
            replacements = {
                '"spacy/matcher/levenshtein.pyx"': '"spacy/matcher/levenshtein.c"',
                'mod_path = name.replace(".", "/") + ".pyx"': 'mod_path = name.replace(".", "/") + ".cpp"',
                "print(\"Cythonizing sources\")\n    ext_modules = cythonize(ext_modules, compiler_directives=COMPILER_DIRECTIVES)": (
                    "print(\"Using generated C/C++ sources\")\n"
                    "    ext_modules = ext_modules"
                ),
            }
            for old, new in replacements.items():
                if old in setup_content:
                    setup_content = setup_content.replace(old, new, 1)
            setup_py.write_text(setup_content)
        if self.has_marker("pydantic_patched"):
            return
        self.apply_patch("pydantic-beta.patch")
        self.set_marker("pydantic_patched")


recipe = SpacyRecipe()

