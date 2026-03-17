from __future__ import annotations

import sh

from kivy_ios.context_managers import cd
from kivy_ios.toolchain import CythonRecipe, shprint


class BlisRecipe(CythonRecipe):
    version = "1.3.3"
    url = "https://files.pythonhosted.org/packages/source/b/blis/blis-{version}.tar.gz"
    depends = ["python3"]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "numpy==2.3.0")

    def cythonize_build(self):
        if not self.cythonize:
            return
        # Keep module names as `cy` / `py` for kivy-ios biglink matching.
        # The default cythonize walk passes "blis/cy.pyx", which triggers
        # renaming to `blis_cy`/`blis_py` in tools/cythonize.py.
        with cd(f"{self.build_dir}/blis"):
            self.cythonize_file("cy.pyx")
            self.cythonize_file("py.pyx")

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        env["BLIS_ARCH"] = "x86_64" if plat.arch == "x86_64" else "generic"
        # blis uses BLIS_COMPILER for its internal C sources (z/*.o) and does
        # not automatically append our target flags there. Pass an explicit
        # target compiler command so these objects are built for iOS.
        sdk = env.get("PLATFORM_SDK") or "iphoneos"
        arch = env.get("ARCH") or plat.arch
        target = (
            f"{arch}-apple-ios-simulator"
            if sdk == "iphonesimulator"
            else f"{arch}-apple-ios"
        )
        env["BLIS_COMPILER"] = f"xcrun -sdk {sdk} clang -target {target}"
        # Ensure distutils uses iOS sysconfig/platform tags (not host macOS tags)
        # when running build_ext under hostpython.
        host_plat = f"ios-13.0-{arch}-{sdk}"
        env["_PYTHON_HOST_PLATFORM"] = host_plat
        env["_PYTHON_SYSCONFIGDATA_NAME"] = "_sysconfigdata__ios_darwin"
        # The sysconfigdata module isn't part of hostpython; point at the one
        # generated when building the target python3.
        env["_PYTHON_SYSCONFIGDATA_PATH"] = (
            f"{self.ctx.build_dir}/python3/{sdk}-{arch}/Python-3.13.12/build/lib.{host_plat}-3.13"
        )
        return env


recipe = BlisRecipe()

