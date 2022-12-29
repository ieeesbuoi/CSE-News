import sys
import subprocess
import os
try:
    import pip
except ImportError:
    print "Please install pip to continue."
    sys.exit(1)


# function that downloads and installs a module from pip
# the last line reruns the program so that it can load the new modules.
# TODO: find a better way to reload the modules so that the app does not restart in every missing module
def install(package):
    python = sys.executable
    if hasattr(pip, 'main'):
        pip.main(['install', package])
        os.execl(python, python, *sys.argv)
    else:
        if hasattr(pip, '_internal'):
            pip._internal.main(['install', package])

        else:
            try:
                call=subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except:
                print "cannot install module ",package,".\nPlease run the following command:\n",sys.executable.split("/")[-1]," -m pip install ",package
                exit(1)
    os.execl(python, python, *sys.argv)
