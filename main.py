"""
main auxiliary module to run detections
"""

import os
import argparse
import scenedetector
import scenesetting
import scenepicture
import sceneexposition
import logging

def process_video(args):
  """
  process video specified in args.video_filename
  """

  # started
  logger = logging.getLogger('vsi_application')
  logger.debug("process_video(): started")

  scenedet = scenedetector.SceneDetector(args.video_filename)
  scene_list = scenedet.get_scenes_list()
  logger.debug('scene_list')

  # Setting – Where are we? (Image classifier telling where are we, what are seeing: desert, nature, a room, etc.)
  sceneset = scenesetting.SceneSettingDetector()

  # Exposition – Necessary information. Quick and Clever
  sceneexp = sceneexposition.SceneExpositionDetector()

  # show list of scenes obtained
  logger.info('List of scenes obtained:')
  for i, scene in enumerate(scene_list):
      logger.info('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        i+1,
        scene[0].get_timecode(), scene[0].get_frames(),
        scene[1].get_timecode(), scene[1].get_frames(),))

  # for each scene...
  for scene_index, scene in enumerate(scene_list):

    # the scene number
    scene_number = scene_index + 1

    # extract picture from scene
    scenepic = scenepicture.ScenePictureExtractor(args.video_filename, scene_number, scene, args.output_dirname)
    picture_filename = scenepic.get_picture_filename()
    msg = '   *** processing scene picture: "{}" number {}/{}'.format(picture_filename, scene_number, len(scene_list))
    logger.debug(msg)

    # Setting – Where are we? (Image classifier telling where are we, what are seeing: desert, nature, a room, etc.)
    sceneset.detect(picture_filename)
    scene_categories = sceneset.get_categories()

    # Exposition – Necessary information. Quick and Clever
    sceneexp.detect(picture_filename)

  # finished
  logger.debug("process_video(): finished")

def main():
  """
  main function
  """

  # setup logger
  logger = logging.getLogger('vsi_application')
  logger.setLevel(logging.DEBUG)
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  # start app and parse args
  logger.debug('App started')
  parser = argparse.ArgumentParser(description='Show video scene inventory.')
  parser.add_argument('video_filename', type=str, help='pass a video as input')
  parser.add_argument('output_dirname', type=str, help='specify where to store output results')
  args = parser.parse_args()

  # make output dir
  args.output_dirname = os.path.join(args.output_dirname, os.path.basename(args.video_filename))
  os.makedirs(args.output_dirname)

  # process video
  process_video(args)

  # finished
  logger.debug('App finished')
