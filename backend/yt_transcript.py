from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except:
        return [{"text":"", "start":0.0, "duration":0.0}]
    return transcript


