from os.path import join
from pathlib import Path
from typing import Dict

from UserData import UserData
from utils import initialize_keypaths


basepath: str = str(join(Path.home(), ".secrets_manager"))
print(basepath)
base_keypath: str = join(basepath, "keys")
print(base_keypath)
base_datapath: str = join(basepath, "data")
print(base_datapath)
keypaths: Dict[str, UserData] = initialize_keypaths(base_keypath, base_datapath)






    
