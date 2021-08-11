import re
from pathlib import Path
import cv2
import os

from constants import *

def find_startswith_file(start, name, endwith = SUBTITLE_FORMAT):
    for _, _, files in os.walk(start):
        for file in files:
            if file.startswith(name) and file.endswith(endwith):
                return file
    return None

def check_file_existed(video_title, format):
    return find_path(video_title, format).exists()

def check_file_existed_without_format(video_title):
    file_path = Path.cwd() / VIDEO_PATH / video_title
    return file_path.exists()

def check_video_existed(video_title):
    return find_path(video_title, VIDEO_FORMAT).exists()

def find_videos_dir_str():
    videos_path = Path.cwd() / VIDEO_PATH
    if not videos_path.exists():                   
        videos_path.mkdir()
    return str(videos_path)

def find_path(video_title, format):
    videos_path = Path.cwd() / VIDEO_PATH
    if not videos_path.exists():                   
        videos_path.mkdir()
    return videos_path / ('%s.%s' % (video_title, format))

def format_video_title(video_title):
    return re.sub(r'\s+', ' ', re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\u00A0\u0020\u3000])", '', video_title)).strip()

def find_path_str(video_title, format):
    return str(find_path(video_title, format))

def screenshot_video_frame(video_title):
    video = cv2.VideoCapture(find_path_str(video_title, VIDEO_FORMAT))  # 读取视频
    video.set(cv2.CAP_PROP_POS_MSEC, 1000 * 10)  # 设置读取位置，1000毫秒
    ret, frame = video.read()  # 读取当前帧，rval用于判断读取是否成功
    if ret:
        cv2.imwrite(find_path_str(video_title, PICTURE_FORMAT), frame)  # 将当前帧作为图片保存到 cover_path