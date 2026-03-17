from __future__ import annotations

import sh

from kivy_ios.toolchain import CythonRecipe, shprint


class BlisRecipe(CythonRecipe):
    version = "1.3.3"
    url = "https://files.pythonhosted.org/packages/source/b/blis/blis-{version}.tar.gz"
    depends = ["python3"]

    def install_hostpython_prerequisites(self):
        super().install_hostpython_prerequisites()
        python = sh.Command(self.ctx.hostpython)
        shprint(python, "-m", "pip", "install", "numpy==2.3.0")

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        env["BLIS_ARCH"] = "x86_64" if plat.arch == "x86_64" else "generic"
        # Ensure distutils uses iOS sysconfig/platform tags (not host macOS tags)
        # when running build_ext under hostpython.
        sdk = env.get("PLATFORM_SDK") or "iphoneos"
        arch = env.get("ARCH") or plat.arch
        env["_PYTHON_HOST_PLATFORM"] = f"ios-13.0-{arch}-{sdk}"
        env["_PYTHON_SYSCONFIGDATA_NAME"] = "_sysconfigdata__ios_darwin"
        return env


recipe = BlisRecipe()

