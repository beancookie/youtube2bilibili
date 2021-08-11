from tinydb import TinyDB, Query
from constants import CH_DB_FILE

ch_db = TinyDB(CH_DB_FILE)

if __name__ == '__main__':
    ch_db.insert_multiple([
        # {
        #   'channel_url': 'https://www.youtube.com/channel/UCtI0Hodo5o5dUb67FeUjDeA',
        #   'batch_number': 20,
        #   'bilibili_channel_id': 208,
        # },
        # {
        #   'channel_url': 'https://www.youtube.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ',
        #   'batch_number': 20,
        #   'bilibili_channel_id': 208,
        # },
        # {
        #   'channel_url': 'https://www.youtube.com/channel/UC2C_jShtL725hvbm1arSV9w',
        #   'batch_number': 1,
        #   'bilibili_channel_id': 208,
        # },
        # {
        #   'channel_url': 'https://www.youtube.com/channel/UCeYUHG6o0YguM-g23htdsSw',
        #   'batch_number': 1,
        #   'bilibili_channel_id': 208,
        # }, 
        {
            'channel_url': 'https://www.youtube.com/channel/UCsooa4yRKGN_zEE8iknghZA',
            'batch_number': 1,
            'bilibili_channel_id': 208,
        },
    ])
