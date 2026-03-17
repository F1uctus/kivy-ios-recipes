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

    def get_recipe_env(self, plat):
        env = super().get_recipe_env(plat)
        sdk = env.get("PLATFORM_SDK") or "iphoneos"
        arch = env.get("ARCH") or plat.arch
        host_plat = f"ios-13.0-{arch}-{sdk}"
        env["_PYTHON_HOST_PLATFORM"] = host_plat
        env["_PYTHON_SYSCONFIGDATA_NAME"] = "_sysconfigdata__ios_darwin"
        env["_PYTHON_SYSCONFIGDATA_PATH"] = (
            f"{self.ctx.build_dir}/python3/{sdk}-{arch}/Python-3.13.12/build/lib.{host_plat}-3.13"
        )
        return env


recipe = CymemRecipe()

