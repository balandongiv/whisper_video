import logging
import os

from PIL import Image
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pytube import YouTube, Playlist

from whispervideos.support_file import clean_and_format_string, create_file_details

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_playlist_urls(playlist_url):
    """
    Retrieves all video URLs from a YouTube playlist.
    :param playlist_url: URL of the YouTube playlist.
    :return: List of video URLs in the playlist.
    """
    playlist = Playlist(playlist_url)
    video_urls = [url for url in playlist.video_urls]
    return video_urls

def process_urls(video_urls_playlist):
    """
    Processes each URL in the playlist. If it's a playlist URL, it retrieves all video URLs from it.
    :param video_urls_playlist: List of video or playlist URLs.
    :return: List of all individual video URLs.
    """
    all_video_urls = []
    for url in video_urls_playlist:
        if 'list=' in url:
            logger.info(f"Processing playlist: {url}")
            playlist_video_urls = get_playlist_urls(url)
            all_video_urls.extend(playlist_video_urls)
        else:
            logger.info(f"Adding video URL: {url}")
            all_video_urls.append(url)
    return all_video_urls

def get_youtube_video_title(url):
    """
    Retrieves the title of a YouTube video.
    :param url: URL of the YouTube video.
    :return: Title of the video.
    """
    try:
        yt = YouTube(url)
        return yt.title
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None

def format_frame_name(seconds):
    """
    Formats the frame name using a minute and second format.
    :param seconds: Time in seconds to format.
    :return: Formatted time string.
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}_{seconds:02d}.png"

def segment_audio(audio_path, aux_folder, segment_duration_seconds=20):
    """
    Segments an audio file into smaller parts based on the given duration.
    :param audio_path: Path to the audio file.
    :param aux_folder: Auxiliary folder to store segments.
    :param segment_duration_seconds: Duration of each segment in seconds.
    :return: List of paths to the audio segments.
    """
    segment_duration_ms = segment_duration_seconds * 1000
    audio = AudioSegment.from_file(audio_path)

    base_path, ext = os.path.splitext(audio_path)
    segment_dir = os.path.join(aux_folder, 'segments')
    os.makedirs(segment_dir, exist_ok=True)

    segment_paths = []
    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i:i + segment_duration_ms]
        segment_path = os.path.join(segment_dir, f"segment_{i // segment_duration_ms}{ext}")
        segment.export(segment_path, format=ext.lstrip('.'))
        segment_paths.append(segment_path)

    return segment_paths

def capture_frames(video_path, aux_folder, interval=5):
    """
    Captures frames from a video at specified intervals.
    :param video_path: Path to the video file.
    :param aux_folder: Auxiliary folder to store snapshots.
    :param interval: Interval in seconds to capture frames.
    :return: List of paths to the captured frames.
    """
    output_folder = os.path.join(aux_folder, 'snapshot')
    os.makedirs(output_folder, exist_ok=True)

    all_paths = []
    with VideoFileClip(video_path) as video:
        for i in range(0, int(video.duration), interval):
            frame_image = Image.fromarray(video.get_frame(i))
            frame_path = os.path.join(output_folder, format_frame_name(i))
            frame_image.save(frame_path)
            all_paths.append(frame_path)

    logger.info("All frames have been captured and saved.")
    return all_paths

def download_youtube_video(url, local_save_directory):
    """
    Downloads a YouTube video.
    :param url: URL of the YouTube video.
    :param local_save_directory: Directory to save the downloaded video.
    :return: Dictionary containing file details.
    """
    yt = YouTube(url)
    output_fname = clean_and_format_string(yt.title)
    file_details = create_file_details(output_fname, url, local_save_directory=local_save_directory)
    file_details['vid_fname'] = os.path.join(file_details['save_directory_aux'], f"{output_fname[:20]}.mp4")
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename=file_details['vid_fname'])

    logger.info(f"Video {yt.title} has been downloaded successfully.")
    return file_details
