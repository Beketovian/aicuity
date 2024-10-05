from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return transcript


