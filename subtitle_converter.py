import codecs
import json
from pathlib import Path
import logging

from tinydb import TinyDB, Query

from constants import *
from translator import TranslatorWrap
import video_utils

tl = TranslatorWrap()
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

def get_time_num(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.split(',')
    h, m, s, ms = [int(_) for _ in [h, m, s, ms]]
    return h * 3600.0 + m * 60.0 + s + ms / 1000.0

def srt_text2bcc_text(srt_text_list, is_translator = False):
    body = []
    body_json = {}
    state_str = 'find_index'
    contents = []
    for srt_text in srt_text_list:
        if (state_str == 'find_index'):
            state_str = 'find_times'
        elif (state_str == 'find_times'):
            times = srt_text
            start_time, end_time = times.split(' --> ')
            start_time = get_time_num(start_time)
            end_time = get_time_num(end_time)
            body_json['from'] = start_time
            body_json['to'] = end_time
            contents = []
            state_str = 'find_text'
        elif (state_str == 'find_text'):
            content = srt_text.strip()
            if (content == ''):
                contents = '\n'.join(contents)
                body_json['location'] = 2
                body_json['content'] = contents
                body.append(body_json)
                body_json = {}
                state_str = 'find_index'
            else:
                if is_translator:
                    contents.append(tl.en2zh(content))
                else:    
                    contents.append(content)
    bcc = {
        "font_size": 0.4,
        "font_color": "#FFFFFF",
        "background_alpha": 0.5,
        "background_color": "#9C27B0",
        "Stroke": "none",
        "body": body
    }
    return bcc

def srt2bcc(title, is_translator = False):
    videos_path = Path.cwd() / VIDEO_PATH
    srt_path = videos_path / (title + ' (en).srt')
    with codecs.open(srt_path, 'r', encoding='utf-8') as f:
        srt_text = f.readlines()
        bcc_text = srt_text2bcc_text(srt_text, is_translator)
        if is_translator:
            bcc_name = title + ' (zh).bcc'
        else:
            bcc_name = title + '.bcc'

        with codecs.open(videos_path / bcc_name, 'w', encoding='utf-8') as f:
            json.dump(bcc_text, f, ensure_ascii=False)

if __name__ == '__main__':
    yt_db = TinyDB(YT_DB_FILE)
    for video in yt_db.all():
        srt_file = video_utils.find_startswith_file(Path.cwd() / VIDEO_PATH, video['title'])
        if srt_file and video_utils.check_file_existed_without_format(srt_file):
            zh_srt_file = video_utils.find_startswith_file(Path.cwd() / VIDEO_PATH, video['title'], '(zh).bcc')
            if not zh_srt_file:
                logging.info('converter %s' % video['title'])
                srt2bcc(video['title'], True)