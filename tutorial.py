import unittest

from whispervideos.whispervid import VideoProcessor

processor = VideoProcessor()
# video_list = [
#     # '../unit_test/how_copyright_works_.mp4',
#     'https://youtu.be/EpUGvLaWc2s',  # Uncomment if you want to test with a YouTube URL
# ]

video_list = [
    'https://www.youtube.com/watch?v=-DP1i2ZU9gk',
    'https://www.youtube.com/watch?v=FlGjISF3l78',  # Uncomment if you want to test with a YouTube URL
]

duration = 10  # Duration in seconds, adjust as needed

# No assertion here as we are testing if it runs without errors
processor.process_youtube_videos(video_list, duration)