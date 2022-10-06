import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import scene_cleaner

import imp
imp.reload(scene_cleaner)

from scene_cleaner import SceneCleaner
from utils import GenerativeArtAPI


def do_art():
    SceneCleaner()()
    GenerativeArtAPI().generate_art(3)


if __name__ == '__main__':
    do_art()

