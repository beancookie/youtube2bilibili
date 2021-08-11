import unittest
import re
import video_utils

VIDEO_TITLE = 'The Cost of Genius Inside The Queens Gambit  Netflix'

class TestVideoUtils(unittest.TestCase):
    def test_check_video_existed(self):
        self.assertTrue(video_utils.check_video_existed(VIDEO_TITLE))
        self.assertFalse(video_utils.check_video_existed(''))

    def test_screenshot_video_frame(self):
        video_utils.screenshot_video_frame(VIDEO_TITLE)
        self.assertTrue(video_utils.find_path(VIDEO_TITLE, video_utils.PICTURE_FORMAT).exists())

if __name__ == '__main__':
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\u00A0\u0020\u3000])", '', '#Tokyo2020: Highlights from the first-ever space Olympics!人')
    # unittest.main()