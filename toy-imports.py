# Breakthrough/PySceneDetect
from __future__ import print_function
import os
import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector

# GKalliatakis/Keras-VGG16-places365
import os
import numpy as np
from urllib.request import urlopen
from PIL import Image
from cv2 import resize
import sys
from vgg16_places_365 import VGG16_Places365

# oarriaga/face_classification
import sys
import cv2
from keras.models import load_model
import numpy as np
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input

# matterport/Mask_RCNN
# Root directory of the project
ROOT_DIR = os.path.abspath(".")
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco
