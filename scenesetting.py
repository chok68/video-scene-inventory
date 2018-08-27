import os
import numpy as np
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont
from cv2 import resize
import sys

from vgg16_places_365 import VGG16_Places365
import logging

class SceneSettingDetector:
  """
  Detect scenes setting (place detection using places365)
  """
  logger = None
  model = None
  categories = None

  NUMBER_OF_PREDICTIONS = 5

  def __init__(self):

    # started
    self.logger = logging.getLogger('vsi_application.scenesetting.SceneSettingDetector')
    self.logger.info('__init__(): started')

    ### init
    self.model = VGG16_Places365(weights='places')
    file_name = 'categories_places365.txt'
    if not os.access(file_name, os.W_OK):
      synset_url = 'https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt'
      #os.system('wget ' + synset_url)
    classes = list()
    with open(file_name) as class_file:
        for line in class_file:
            classes.append(line.strip().split(' ')[0][3:])
    self.categories = tuple(classes)

    # finished
    self.logger.info('__init__(): finished')

  def get_categories(self):
    return self.categories
    
  def detect(self, picture_filename):
    self.logger.info('detect(): started')

    image = Image.open(picture_filename)
    image = np.array(image, dtype=np.uint8)
    image = resize(image, (224, 224))
    image = np.expand_dims(image, 0)

    preds = self.model.predict(image)[0]
    top_preds = np.argsort(preds)[::-1][0:self.NUMBER_OF_PREDICTIONS]

    self.logger.info('--SCENE CATEGORIES:')
    # output the prediction
    for i in range(0, 5):
        self.logger.info(self.categories[top_preds[i]])

    # save into image
    img = Image.open(picture_filename)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("arial.ttf", 16)
    text_y = 20
    for i in range(0, 5):
      # draw.text((x, y),"Sample Text",(r,g,b))
      draw.text((0, text_y), self.categories[top_preds[i]], (255,255,255), font=font)
      text_y = text_y + 20
    output_picture_filename = picture_filename + '-setting.jpg'
    img.save(output_picture_filename)

    self.logger.info('detect(): finished')
