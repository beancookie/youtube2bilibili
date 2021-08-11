import logging
from pathlib import Path
import asyncio
import json
import time
import re

from bilibili_api import Credential, video
from tinydb import TinyDB, Query
from translator import TranslatorWrap

from constants import *
import video_utils
import subtitle_converter

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

SESSDATA = '*'
BILI_JCT = '*'
BUVID3 = '*'

bl_db = TinyDB(BL_DB_FILE)
translator = TranslatorWrap()

def split_description(description):
    split_list = re.split(r'\.', re.sub(r'\s+', ' ', description))
    result_description = ''
    for split_str in split_list:
        if len(result_description + split_str) < 200:
            result_description += (split_str + '.')
        else:
            break
    return result_description

async def upload_to_bilibili(yt_video, video_url, channel_id, title_prefix = '', init_tag = ''):
    logging.info('upload_to_bilibili %s %s', yt_video.thumbnail_url, yt_video.title)

    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 P1 对象
    p1 = video.VideoUploaderPageObject(video_stream=open(video_utils.find_path_str(yt_video.title, video_utils.VIDEO_FORMAT), 'rb'), title=yt_video.title, video_format=video_utils.VIDEO_FORMAT)
    tag = 'Youtube,' + init_tag
    if hasattr(yt_video, 'keywords'):
        tag += ',' + ','.join([tag[:20] for tag in yt_video.keywords[:10]])

    if hasattr(yt_video, 'tags'):
        tag += ',' + yt_video.tags
    # 视频上传配置
    config = {
        'copyright': 2, #'1 自制，2 转载。',
        'source': video_url, #'str, 视频来源。投稿类型为转载时注明来源，为原创时为空。',
        'desc': '声明：如涉及侵权敬请原作者直接联系我们删除。\n' + split_description(yt_video.description), #'str, 视频简介。',
        'desc_format_id': 0,
        'dynamic': '', #'str, 动态信息。',
        'interactive': 0,
        'open_elec': 0, #'int, 是否展示充电信息。1 为是，0 为否。',
        'no_reprint': 0, #'int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。',
        'subtitles': {
        'lan': '', #'字幕语言，不清楚作用请将该项设置为空',
        'open': 0
        },
        'tag': tag, #'str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3',
        'tid': channel_id, #'int, 分区ID。可以使用 channel 模块进行查询。',
        'title': title_prefix + yt_video.title[:70], #'视频标题',
        'up_close_danmaku': False, #'bool, 是否关闭弹幕。',
        'up_close_reply': False, #'bool, 是否关闭评论。',
    }
    # 要上传的所有分 P 列表
    pages = [p1]
    # 截取视频封面
    video_utils.screenshot_video_frame(yt_video.title)
    # 转换字幕格式
    if video_utils.check_file_existed_without_format(video_utils.find_startswith_file(Path.cwd() / VIDEO_PATH, yt_video.title)):
        subtitle_converter.srt2bcc(yt_video.title)

    if video_utils.check_video_existed(yt_video.title):
        # 初始化上传
        uploader = video.VideoUploader(cover=open(video_utils.find_path_str(yt_video.title, video_utils.PICTURE_FORMAT), 'rb'), cover_type=video_utils.PICTURE_FORMAT, pages=pages, config=config, credential=credential)
        # 开始上传
        av_info = await uploader.start()
        bl_db.insert({
            'bilibili_av': av_info,
            'title': yt_video.title,
        })
        logging.info('upload_to_bilibili success %s' % av_info)
    else:
        logging.info('upload_to_bilibili file not exists %s' % yt_video.title)


# declaringa a class
class Obj:
      
    # constructor
    def __init__(self, dict):
        self.__dict__.update(dict)

def dict2obj(dict):
      
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict), object_hook=Obj)

# if __name__ == '__main__':
#     yt_db = TinyDB(YT_DB_FILE)
#     bl_db = TinyDB(BL_DB_FILE)
#     for v in yt_db.all():
#         video_obj = dict2obj(v)
#         Bilibili = Query()
#         exist_bilibili = bl_db.search(Bilibili.title == video_obj.title)

#         if not exist_bilibili and hasattr(video_obj, 'video_url'):

#             asyncio.get_event_loop().run_until_complete(upload_to_bilibili(video_obj, video_obj.video_url, video_obj.bilibili_channel_id, '[TED演讲] ', 'TED'))
#             time.sleep(30)