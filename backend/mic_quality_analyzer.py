import os
import subprocess
import yt_dlp
import librosa
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

output_dir = "audio/"

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
            '-t', '600',
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
    y, sr = librosa.load(file_path, sr=None)
    y_trimmed, index = librosa.effects.trim(y, top_db=threshold_db)
    silence_part = np.concatenate([y[:index[0]], y[index[1]:]])
    rms_silence = librosa.feature.rms(y=silence_part)
    mean_rms_silence = np.mean(rms_silence)
    static_detected = np.isclose(mean_rms_silence, 0.0)
    return static_detected, mean_rms_silence

def analyze_single_file(file_path):
    try:
        has_static, rms_value = classify_static(file_path)
        return file_path, 1 if has_static else 0
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return file_path, None

def analyze_audio_files_in_parallel(directory):
    wav_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.wav')]
    results = {}

    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(analyze_single_file, file_path): file_path for file_path in wav_files}

        for future in as_completed(future_to_file):
            file_path, result = future.result()
            file_name = os.path.basename(file_path)
            results[file_name] = result
            
    results = {file_name.replace('.wav', ''): result for file_name, result in results.items()}

    return results

def process_video(video_id, output_dir):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    # video_title = get_video_title(youtube_url)
    # sanitized_title = "".join([c if c.isalnum() or c in " -_" else "_" for c in video_title])
    output_filename = os.path.join(output_dir, video_id)
    download_and_trim_audio(youtube_url, output_filename)

def process_videos_parallel(video_ids, output_dir):
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_video, video_id, output_dir): video_id for video_id in video_ids}
        for future in as_completed(futures):
            video_id = futures[future]
            try:
                future.result()
                print(f"Successfully processed video: {video_id}")
            except Exception as e:
                print(f"Error processing video {video_id}: {e}")

def analyze_static(video_ids):
    process_videos_parallel(video_ids, output_dir)
    print(output_dir)
    results = analyze_audio_files_in_parallel(output_dir)
    # os.system('rm -rf audio/')
    print(results)
    return results
