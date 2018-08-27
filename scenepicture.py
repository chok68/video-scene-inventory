import logging
import cv2
import os

class ScenePictureExtractor:
  """
  Extract a picture from a passed scene time
  """
  logger = None
  video_filename = None
  output_dirname = None
  picture_filename = None # saved picture filename (this script output)
  scene = None
  scene_index = None

  def __init__(self, video_filename, scene_index, scene, output_dirname):
    # started
    self.logger = logging.getLogger('vsi_application.scenepicture.ScenePictureExtractor')
    self.logger.info('__init__(): started')
    self.logger.debug(video_filename)
    self.video_filename = video_filename
    self.scene = scene
    self.scene_index = scene_index
    self.output_dirname = output_dirname

    # run
    self.run()

    # finished
    self.logger.info('__init__(): finished')

  def get_picture_filename(self):
    return self.picture_filename

  def run(self):
    self.logger.info('run(): started')
    self.logger.debug('   opening video...')

    # create output dir
    try:
      os.mkdir(self.output_dirname)
    except:
      pass

    # calculate center frame
    center_frame_num = self.scene[0].frame_num + int((self.scene[1].frame_num - self.scene[0].frame_num) / 2)
    self.logger.debug('   center_frame_num ' + str(center_frame_num))

    # capture specific frame
    count = 0
    cap = cv2.VideoCapture(self.video_filename)
    while cap.isOpened():
      # Extract the frame
      ok, frame = cap.read()

      if not ok:
        break

      if count == center_frame_num:
        #scene_filename = 'scene-center-frame-%#05d.jpg' % (count+1)
        scene_filename = 'scene-' + f'{self.scene_index:05}' + '--' + self.scene[0].get_timecode() + '--' + self.scene[1].get_timecode()
        scene_filename = scene_filename.replace(':', '-')
        scene_filename = scene_filename.replace('.', '-')
        scene_filename = scene_filename + '.jpg'
        self.picture_filename = os.path.join(self.output_dirname, scene_filename)
        cv2.imwrite(self.picture_filename, frame)
        self.logger.debug('   saved scene picture: ' + self.picture_filename)

      count = count + 1
      #self.logger.debug('   on frame: ' + str(count))

    self.logger.info('run(): finished')
