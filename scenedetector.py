import os

import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector

import logging

class SceneDetector:
  """
  Detect scenes changes in video
  """
  logger = None
  video_filename = None
  stats_filename = None

  def __init__(self, video_filename):
    self.logger = logging.getLogger('vsi_application.scenedetector.SceneDetector')
    self.logger.info('on __init__')
    self.video_filename = video_filename
    self.stats_filename = 'my-video-stats.csv'
    self.run()

  def get_scenes_list(self):
    return self.scene_list

  def run(self):
    self.logger.info('run(): started')
    self.logger.info("Running PySceneDetect API test...")
    self.logger.info("PySceneDetect version being used: %s" % str(scenedetect.__version__))

    # Create a video_manager point to video file testvideo.mp4
    video_manager = VideoManager([self.video_filename])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)
    # Add ContentDetector algorithm (constructor takes detector options like threshold).
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()
    print ('base_timecode', base_timecode)

    try:
      # If stats file exists, load it.
      if os.path.exists(self.stats_filename):
        # Read stats from CSV file opened in read mode:
        with open(self.stats_filename, 'r') as stats_file:
          stats_manager.load_from_csv(stats_file, base_timecode)

      # Set video_manager duration
      start_time = base_timecode

      # Set downscale factor to improve processing speed.
      video_manager.set_downscale_factor()

      # Start video_manager.
      video_manager.start()

      # Perform scene detection on video_manager.
      scene_manager.detect_scenes(frame_source=video_manager,
                                  start_time=start_time)

      # Obtain list of detected scenes.
      self.scene_list = scene_manager.get_scene_list(base_timecode)
      # Like FrameTimecodes, each scene in the scene_list can be sorted if the
      # list of scenes becomes unsorted.

      """
      # We only write to the stats file if a save is required:
      if stats_manager.is_save_required():
        with open(self.stats_filename, 'w') as stats_file:
          stats_manager.save_to_csv(stats_file, base_timecode)
      """

    finally:
      video_manager.release()
      self.logger.info('run(): finished')
