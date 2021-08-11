from tinydb import TinyDB, Query

from constants import *
from downloader import Downloader

ch_db = TinyDB(CH_DB_FILE)

if __name__ == '__main__':
  downloader = Downloader()
  Channel = Query()
  channels = ch_db.search(Channel.channel_url == 'https://www.youtube.com/channel/UCsooa4yRKGN_zEE8iknghZA')
  for channel in channels:
    downloader.download_channel(channel['channel_url'], channel['batch_number'], channel['bilibili_channel_id'], '[TED演讲] ', 'TED')