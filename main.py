from dotenv import load_dotenv
import os
from os import listdir
from datetime import datetime, timezone, timedelta, date
import requests
import youtube_dl
import ffmpeg


# Loads the .env file
load_dotenv()  # Get environment variables with VARIABLE = os.getenv("VARIABLE")

# Todo: Add thumbnail generator
# Todo: Add title generator, description generator
# Todo: needs an ffmpeg script to combine the clips together

def combine_clips():
    x = datetime.now()
    todays_date = x.strftime("%d-%m-%Y")
    stream_list = []
    for file in listdir(f'/home/jacob/files/twitch/{todays_date}'):
        stream_list.append(ffmpeg.input(f'/home/jacob/files/twitch/{todays_date}/{file}'))
    
    ffmpeg.concat(*stream_list).output('output.mp4').run()



def download_clips():
    top_clips = get_top_clips()
    x = datetime.now()
    todays_date = x.strftime("%d-%m-%Y")
    ydl_opts = {
        'outtmpl': f'~/files/twitch/{todays_date}/%(title)s',
        'format': '720'
    }

    for clip in top_clips:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Todo: figure out how to name files specific names
            ydl.download([clip['url']])


def get_top_clips():
    # started_at variable will be one day before, while ended_at time will be
    # the current time
    end_time = datetime.now(timezone.utc).astimezone()
    start_time = datetime.now(timezone.utc).astimezone() - timedelta(days=1)

    streamer_ids = os.getenv("STREAMER_IDS").split()
    url = "https://api.twitch.tv/helix/clips"
    params = {
        'first': 21//len(streamer_ids),
        'started_at': start_time.isoformat(),
        'ended_at': end_time.isoformat()
    }
    headers = {
        "Client-id": os.getenv("CLIENT_ID")
    }

    clip_list = []
    for streamer_id in streamer_ids:
        params['broadcaster_id'] = streamer_id

        response = requests.get(url, params=params, headers=headers).json()
        clip_list += response['data']

    return clip_list


if __name__ == '__main__':
    combine_clips()