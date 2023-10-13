import os
import lib.settings

targetPath = lib.settings.applicationPipRootPath

print(f"pip --target {targetPath}  install wheelFile.whl")
os.system(f"pip --target {targetPath}  install PIL")

import PIL