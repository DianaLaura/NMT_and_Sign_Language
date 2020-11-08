import unittest
from datetime import datetime, time, timedelta
from data_loading_extraction import frames
from data_loading_extraction import frames

class frames_test(unittest.TestCase):

    def test_conversion_to_50_fps(self):
    
        time = datetime.strptime('02:30:06:49', '%H:%M:%S:%f')

        self.assertEquals(frames.timestamp_to_50_fps(time), 450349)
    
    def test_fps_50_to_fps_30(self):
        self.assertEquals(frames.fps_50_to_fps_30(716),430)