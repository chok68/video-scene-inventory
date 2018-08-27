import logging
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
ROOT_DIR = os.path.abspath(".")
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco
from PIL import Image, ImageDraw, ImageFont

class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

class SceneExpositionDetector:
  """
  Detect scene exposition – Necessary information. Quick and Clever
  """
  logger = None

  def __init__(self):
    self.logger = logging.getLogger('vsi_application.sceneexposition.SceneExpositionDetector')
    self.logger.info('on __init__')

    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Local path to trained weights file
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    # Download COCO trained weights from Releases if needed
    if not os.path.exists(COCO_MODEL_PATH):
        utils.download_trained_weights(COCO_MODEL_PATH)

    # set properties
    config = InferenceConfig()
    config.display()

    # Create model object in inference mode.
    self.model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # Load weights trained on MS-COCO
    self.model.load_weights(COCO_MODEL_PATH, by_name=True)

    # COCO Class names
    # Index of the class in the list is its ID. For example, to get ID of
    # the teddy bear class, use: class_names.index('teddy bear')
    self.class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                   'bus', 'train', 'truck', 'boat', 'traffic light',
                   'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                   'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                   'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                   'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                   'kite', 'baseball bat', 'baseball glove', 'skateboard',
                   'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                   'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                   'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                   'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                   'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                   'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                   'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                   'teddy bear', 'hair drier', 'toothbrush']

    
  def get_scenes_list(self):
    return self.scene_list

  def detect(self, picture_filename):
    self.logger.info('detect(): started')

    # Run Object Detection
    image = skimage.io.imread(picture_filename)
    results = self.model.detect([image], verbose=1)

    # open image to get figsize
    img = Image.open(picture_filename).convert('RGBA')

    # plot results
    r = results[0]
    _, ax = plt.subplots(1, figsize=(16, 16))
    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                self.class_names, r['scores'], ax=ax)

    output_picture_filename = picture_filename + '-exposition.jpg'
    plt.savefig(output_picture_filename)

    # finished
    self.logger.info('detect(): finished')
