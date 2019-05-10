from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta
import requests
import youtube_dl

# Loads the .env file
load_dotenv()  # Get environment variables with VARIABLE = os.getenv("VARIABLE")


def download_clips():
    top_clips = get_top_clips()
    for clip in top_clips:
        with youtube_dl.YoutubeDL() as ydl:
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
    download_clips()
