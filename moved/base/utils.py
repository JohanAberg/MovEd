import os
import sys

LAUNCH_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

def get_icon_path(name=''):
    dir_path = '%s/icons/%s' % (LAUNCH_DIR, name)
    print dir_path
    return dir_path