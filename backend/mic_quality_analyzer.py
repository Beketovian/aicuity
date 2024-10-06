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
    """
    Extract the video title from the YouTube URL using yt-dlp.
    """
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get('title', 'video')
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "video"

def download_and_trim_audio(youtube_url, output_filename):
    """
    Use yt-dlp to download the video and pipe it to ffmpeg, which trims the first 10 minutes of audio.
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
        print("Broken pipe error occurred but file was processed successfully.")
    except Exception as e:
        print(f"Error downloading and trimming audio for {youtube_url}: {e}")

def classify_static(file_path, threshold_db=60):
    """
    Detect static in a WAV file by analyzing its RMS value.
    """
    y, sr = librosa.load(file_path, sr=None)
    
    y_trimmed, index = librosa.effects.trim(y, top_db=threshold_db)
    
    total_duration = librosa.get_duration(y=y, sr=sr)
    trimmed_duration = librosa.get_duration(y=y_trimmed, sr=sr)
    silence_duration = total_duration - trimmed_duration
    
    silence_part = np.concatenate([y[:index[0]], y[index[1]:]])
    rms_silence = librosa.feature.rms(y=silence_part)
    
    mean_rms_silence = np.mean(rms_silence)
    static_detected = np.isclose(mean_rms_silence, 0.0)
    
    return static_detected, mean_rms_silence

def analyze_single_file(file_path):
    """
    Analyze a single WAV file for static noise and return the result.
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
    Analyze all WAV files in the specified directory for static noise in parallel.
    """
    wav_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.wav')]
    results = {}

    # Use ProcessPoolExecutor to analyze files in parallel
    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(analyze_single_file, file_path): file_path for file_path in wav_files}

        for future in as_completed(future_to_file):
            file_path, result = future.result()
            file_name = os.path.basename(file_path)
            results[file_name] = result

    return results

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=Wo5wuhrDHRQ"
    video_title = get_video_title(youtube_url)
    sanitized_title = "".join([c if c.isalnum() or c in " -_" else "_" for c in video_title])
    output_filename = os.path.join(output_dir, sanitized_title)

    download_and_trim_audio(youtube_url, output_filename)

    audio_results = analyze_audio_files_in_parallel(output_dir)
    
    for file_name, result in audio_results.items():
        print(f'{file_name}: {result["status"]} (RMS Value: {result["rms_value"]:.5f})')
