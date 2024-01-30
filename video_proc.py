import os

from PIL import Image
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pytube import YouTube, Playlist

from support_file import clean_and_format_string, create_file_detail


def get_playlist_urls(playlist_url):
    # Create a playlist object
    playlist = Playlist(playlist_url)

    # List to store video URLs
    video_urls = []

    # Iterate through each video in the playlist
    for url in playlist.video_urls:
        # print(f'Found video URL: {url}')
        video_urls.append(url)

    return video_urls

def process_urls(video_urls_playlist):
    """
    Process each URL in the playlist, check if it's a video or playlist URL, and return all video URLs.
    """
    all_video_urls = []
    for url in video_urls_playlist:
        if 'list=' in url:
            print(f"Processing playlist: {url}")
            playlist_video_urls = get_playlist_urls(url)
            all_video_urls.extend(playlist_video_urls)
        else:
            print(f"Adding video URL: {url}")
            all_video_urls.append(url)
    return all_video_urls
def get_youtube_video_title(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        # Get the title of the video
        title = yt.title
        return title
    except Exception as e:
        return f"An error occurred: {e}"

def format_frame_name(seconds):
    """Format the frame name using minute and second format."""
    minutes = seconds // 60
    seconds = seconds % 60
    # return f"frame_{minutes:02d}_{seconds:02d}.png"
    return f"{minutes:02d}_{seconds:02d}.png"

def segment_audio(audio_path, aux_folder,segment_duration_seconds=20):
    """
    Segment audio into smaller parts based on the given duration.
    """
    segment_duration_ms = segment_duration_seconds * 1000
    audio = AudioSegment.from_file(audio_path)

    base_path, ext = os.path.splitext(audio_path)
    # segment_dir = f"{base_path}_segments"
    segment_dir=os.path.join(aux_folder,'segments')
    os.makedirs(segment_dir, exist_ok=True)

    segment_paths = []
    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i:i + segment_duration_ms]
        segment_path = os.path.join(segment_dir, f"segment_{i // segment_duration_ms}{ext}")
        segment.export(segment_path, format=ext.lstrip('.'))
        segment_paths.append(segment_path)

    return segment_paths
def get_outer_child_folder_name(path):
    # Check if the path has an extension
    if os.path.splitext(path)[1]:
        # Extract the base name without extension
        return os.path.splitext(os.path.basename(path))[0]
    else:
        # If no extension, return as is
        return path
def capture_frames(video_path, aux_folder,interval=5):
    """
    Capture frames from a video at a specified interval and save them to an output folder.
    """
    # output_folder = get_outer_child_folder_name(output_folder)
    output_folder=os.path.join(aux_folder,'snapshot')
    os.makedirs(output_folder, exist_ok=True)

    all_paths = []
    with VideoFileClip(video_path) as video:
        for i in range(0, int(video.duration), interval):
            frame_image = Image.fromarray(video.get_frame(i))
            frame_path = os.path.join(output_folder, format_frame_name(i))
            frame_image.save(frame_path)
            all_paths.append(frame_path)

    print("All frames have been captured and saved.")
    return all_paths




def download_youtube_video(url,local_save_directory):
    """
    Download a YouTube video and return file details.
    """
    yt = YouTube(url)
    output_fname = clean_and_format_string(yt.title)
    file_details = create_file_detail(output_fname, url,local_save_directory=local_save_directory)
    file_details ['vid_fname'] = os.path.join(file_details['save_directory_aux'],f"{output_fname[:20]}.mp4")
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename=file_details['vid_fname'])

    print(f"Video {yt.title} has been downloaded successfully.")
    return file_details
