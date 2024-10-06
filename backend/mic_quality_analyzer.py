import os
import subprocess
import yt_dlp
import librosa
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

output_dir = "audio/"

###### TODO: better logging w/ frontend ######

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_video_title(youtube_url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get('title', 'video')
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "video"

def download_and_trim_audio(youtube_url, output_filename):
    """
    Download the audio from a YouTube video and trim it to the first 10 minutes w/ ffmpeg and yt-dlp. ffmpeg is highly configurable as shown below
    """
    wav_file = f"{output_filename}.wav"
    try:
        ytdlp_cmd = [
            'yt-dlp', '-f', 'bestaudio',
            '-o', '-',
            youtube_url
        ]

        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', 'pipe:0',
            '-t', '600', # here is where we trim to 600 seconds (10 minutes)
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            '-ac', '2',
            wav_file
        ]

        with subprocess.Popen(ytdlp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as ytdlp_proc:
            try:
                subprocess.run(ffmpeg_cmd, stdin=ytdlp_proc.stdout, check=True)
            except subprocess.CalledProcessError as ffmpeg_error:
                print(f"FFmpeg error: {ffmpeg_error}")
            finally:
                ytdlp_proc.stdout.close()
                ytdlp_proc.wait()
            print(f"Downloaded and trimmed first 10 minutes to {wav_file}")

    except BrokenPipeError:
        print("Broken pipe error occurred but file was processed successfully")
    except Exception as e:
        print(f"Error downloading and trimming audio for {youtube_url}: {e}")

def classify_static(file_path, threshold_db=60):
    """
    Detect static in a WAV file by analyzing its RMS value and comparing it to threshold. Very simple: we analyze areas of silence in the video and see if there is "noise" aka static
    """
    y, sr = librosa.load(file_path, sr=None)
    
    y_trimmed, index = librosa.effects.trim(y, top_db=threshold_db)
    
    total_duration = librosa.get_duration(y=y, sr=sr)
    trimmed_duration = librosa.get_duration(y=y_trimmed, sr=sr)
    silence_duration = total_duration - trimmed_duration # don't need this shit no more
    
    silence_part = np.concatenate([y[:index[0]], y[index[1]:]])
    rms_silence = librosa.feature.rms(y=silence_part)
    
    mean_rms_silence = np.mean(rms_silence)
    static_detected = np.isclose(mean_rms_silence, 0.0)
    
    return static_detected, mean_rms_silence

def analyze_single_file(file_path):
    """
    Analyze a single WAV file for static noise and return the result. We run this process parallel with others in the below function
    """
    try:
        has_static, rms_value = classify_static(file_path)
        return file_path, {
            'status': 'Static detected' if has_static else 'No static detected',
            'rms_value': rms_value
        }
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return file_path, {'status': 'Error', 'rms_value': None}

def analyze_audio_files_in_parallel(directory):
    """
    Analyze all WAV files in the specified directory for static noise in parallel. This shit goated AF like it brings down the total analysis time SIGNIFICANTLY
    """
    wav_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.wav')]
    results = {}

    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(analyze_single_file, file_path): file_path for file_path in wav_files}

        for future in as_completed(future_to_file):
            file_path, result = future.result()
            file_name = os.path.basename(file_path)
            results[file_name] = result

    return results

def process_video(video_id, output_dir):
    """
    Process a single video, downloading the audio and save as a WAV file
    """
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    video_title = get_video_title(youtube_url)
    sanitized_title = "".join([c if c.isalnum() or c in " -_" else "_" for c in video_title])
    output_filename = os.path.join(output_dir, sanitized_title)
    download_and_trim_audio(youtube_url, output_filename)

def process_videos_parallel(video_ids, output_dir):
    """
    Parallelize the above process. Again this shit goated
    """
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_video, video_id, output_dir): video_id for video_id in video_ids}
        for future in as_completed(futures):
            video_id = futures[future]
            try:
                future.result()
                print(f"Successfully processed video: {video_id}")
            except Exception as e:
                print(f"Error processing video {video_id}: {e}")

if __name__ == "__main__":
    video_ids = ['KqquwB_kHvU', 'R1RuIOyQY2k', 'm2NV1ET0ZqY', 'mfycQJrzXCA', 'kYkiDan8Cnk', 
                 'fmRHDqcodS4', '997nxyZRp2U', 'w5ebcowAJD8', 'aZZrEE_UsIk', 'uCTsmdDMq0U']
    output_dir = "audio/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    process_videos_parallel(video_ids, output_dir)

    audio_results = analyze_audio_files_in_parallel(output_dir)
    
    for file_name, result in audio_results.items():
        print(f'{file_name}: {result["status"]} (RMS Value: {result["rms_value"]:.5f})')
