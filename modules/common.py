"""\
Simple module for commonly used function across differenc modules.
"""

import os

def does_file_exist(file_path):

    return os.path.isfile(file_path)

def clear_name(id, ext, name):

    return name.replace(id+'_', '').replace('.'+ext, '')