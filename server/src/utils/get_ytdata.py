import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = os.environ.get('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

def extract_id(link):
    # Regular expression pattern to match YouTube video and playlist URLs
    pattern = r'(?:https?://)?(?:www\.)?youtube\.com/(?:watch\?v=|playlist\?list=)([a-zA-Z0-9_-]+)'
    match = re.match(pattern, link)
    if match:
        id = match.group(1)
        if 'watch?v=' in link:
            return { "id": id, "type": 'video' }
        elif 'playlist?list=' in link:
            return { "id": id, "type": 'playlist' }
    else:
        return None

def get_hours(content_id, content_type):
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    total_seconds = 0

    nextPageToken = None
    while True:

        pl_request = None

        if content_type == 'playlist':
            pl_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=content_id,
                maxResults=50,
                pageToken=nextPageToken
            )

        pl_response = []

        if pl_request:
            pl_response = pl_request.execute()

        vid_ids = []
        if content_type == 'video':
            vid_ids.append(content_id)
        else:
            for item in pl_response['items']:
                vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = item['contentDetails']['duration']

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_seconds += video_seconds

        if pl_response:
            nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break

    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return hours + (minutes / 60)

def get_data(content_id, content_type):
    data = None
    if content_type == 'playlist':
        pl_request = youtube.playlists().list(
            part='contentDetails,snippet',
            id=content_id,
        )
        print(pl_request)
        if pl_request:
            pl_response = pl_request.execute()
            data = pl_response['items'][0]
    else:
        vid_request = youtube.videos().list(
            part="contentDetails,snippet",
            id=content_id
        )

        if vid_request:
            vid_response = vid_request.execute()
            data = vid_response['items'][0]
    
    data['hours'] = get_hours(content_id, content_type)

    return data
