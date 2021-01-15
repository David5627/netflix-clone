import requests
from django.shortcuts import render
from django.conf import settings
from isodate import parse_duration

# Create your views here.
def index(request):
    search_url ='https://www.googleapis.com/youtube/v3/search' 
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part' : 'snippet',
        'q' : 'Action movies', 
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 9

    }

    video_ids = []
    r = requests.get(search_url, params=search_params)
    results = r.json()['items']
    for result in results:
        video_ids.append(result['id']['videoId'])


    video_params = {
        'part' : 'snippet,contentDetails',
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'id' :','.join(video_ids),
     
    }

    r = requests.get(video_url, params=video_params)
    results = r.json()['items']

    videos = []
    for result in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }', 
            'duration' : parse_duration(result['contentDetails']['duration']),
            'thumbnail' : result['snippet']['thumbnails']['high']['url'] 
        }

        videos.append(video_data)

    context = {
        'videos' : videos
    }


    return render(request, 'search/index.html', context)