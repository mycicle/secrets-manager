import os
from os.path import join
from loguru import logger
from typing import Dict, List

from UserData import UserData

def initialize_keypaths(base_keypath: str, base_datapath: str):

    # check if the keypath and datapaths exist, if not create a new directory to match
    if not os.path.exists(base_keypath):
        logger.warning(f"base_keypath {base_keypath} does not exist. Creating directory")
        os.makedirs(base_keypath)
    if not os.path.exists(base_datapath):
        logger.warning(f"base_datapath {base_datapath} does not exist. Creating directory")
        os.makedirs(base_datapath)

    # initialize output dict
    output: Dict[str, UserData] = {}
    # keys and databases are filenames of the form username.extension and should match
    # i.e for every username.db there is a username.key
    keys: List[str] = [filename for filename in os.listdir(base_keypath) if filename.split('.')[-1] == "key"]
    databases: List[str] = [filename for filename in os.listdir(base_datapath) if filename.split('.')[-1] == "db"]

    # if the above constraint is met then the two lists of paths should be the same length
    if len(databases) != len(keys):
        raise ValueError("Keys and databases out of sync")
    # for each username in the keys list there should be a matching db file, if not then an error is raised
    for key in keys:
        if '.'.join([key.split('.')[0], "db"]) not in databases:
            raise ValueError("Keys and databases out of sync ")
    
    # now that we know keys and databases represent the same users and are in sync
    # we can build our output paths using the usernames and known extensions
    # each entry of output should look like this
    # mycicle: UserData({
    #   keypath: /home/mycicle/.secrets_manager/keys/mycicle.key
    #   datapath: /home/mycicle/.secrets_manager/data/mycicle.data
    # })
    # the path should update to the correct "home" directory for the user's OS
    # and the "/" should be properly replaced with a "\" on Windows
    for key in keys:
        username: str = key.split('.')[0]
        output[username] = UserData(join(base_keypath, key), join(base_datapath, '.'.join([username, "db"])))
    
    return output