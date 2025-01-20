from os.path import dirname, join
from logging import getLogger

logger = getLogger(__name__)

#returns JavaScript code to expand a button tree on organizations page
#returns an empty str if file could not be loaded
def get_expand_organizations() -> str:
    #finding the js file
    this_dir = dirname(__file__)
    path = join(this_dir, 'expand_organizations.js')

    try:
        with open(path, "r") as script_file:
            return script_file.read()
    except:
        logger.error(f"get_expand_tree_js : file '{path}' could not be loaded")
    return ""
