import unittest

from bilibili_api import channel

class TestDownloader(unittest.TestCase):
    def get_channel(self):
        self.assertIsNotNone(channel.get_channel_info_by_name('影视杂谈'))

if __name__ == '__main__':
    # print(channel.get_channel_info_by_name('影视杂谈'))
    # print(channel.get_channel_info_by_name('校园学习'))
    print(channel.get_channel_info_by_name('游戏'))

    unittest.main()