from youtube_transcript_api import YouTubeTranscriptApi


video_id = "vHx2YwT3GrY"
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])