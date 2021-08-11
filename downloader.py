import logging
import asyncio

from pytube import YouTube, Channel
from tinydb import TinyDB, Query

from constants import *
from uploader import upload_to_bilibili
import video_utils

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

class Downloader:
    def __init__(self):
        self.yt_db = TinyDB(YT_DB_FILE)
        self.bl_db = TinyDB(BL_DB_FILE)
    
    def upload_video(self, yt_video, video_url, channel_id, title_prefix = '', init_tag = ''):
        Bilibili = Query()
        exist_bilibili = self.bl_db.search(Bilibili.title == yt_video.title)

        if not exist_bilibili:
            asyncio.get_event_loop().run_until_complete(upload_to_bilibili(yt_video, video_url, channel_id, title_prefix, init_tag))
        else:
            logging.info('video already upload %s', yt_video.title)

    def download_channel(self, channel_url, video_number, channel_id, title_prefix = '', init_tag = ''):
        logging.info('download_channel %s %d', channel_url, video_number)
        c = Channel(channel_url)
        for video_url in c.video_urls[:video_number]:
            logging.info('download_video %s', video_url)
            yt_video = YouTube(video_url)
            yt_video.title = video_utils.format_video_title(yt_video.title)[:80]
            Video = Query()
            exist_videos = self.yt_db.search(Video.title == yt_video.title)

            if not exist_videos:
                self.download_video(yt_video, video_url, channel_id)
            else:
                logging.info('video already existed %s', yt_video.title)

            self.upload_video(yt_video, video_url, channel_id, title_prefix, init_tag)

    def download_video(self, yt_video, video_url, channel_id):
        self.yt_db.insert(
            {
                'title': yt_video.title,
                'author': yt_video.author,
                'description': yt_video.description,
                'publish_date': str(yt_video.publish_date),
                'rating': yt_video.rating,
                'channel_id': yt_video.channel_id,
                'channel_url': yt_video.channel_url,
                'thumbnail_url': yt_video.thumbnail_url,
                'tags': ','.join([tag[:20] for tag in yt_video.keywords[:10]]),
                'video_url': video_url,
                'bilibili_channel_id': channel_id,
            }
        )

        caption = yt_video.captions.get_by_language_code('en')
        if caption:
            caption.download(title = yt_video.title, output_path = video_utils.find_videos_dir_str())

        yt_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path = video_utils.find_videos_dir_str())
