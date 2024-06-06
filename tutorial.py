import unittest
'''
YOu can transcribe a video from a URL or a local file.
'''
from whispervideos.whispervid import VideoProcessor

processor = VideoProcessor()
# video_list = [
#     # '../unit_test/how_copyright_works_.mp4',
#     'https://youtu.be/EpUGvLaWc2s',  # Uncomment if you want to test with a YouTube URL
# ]
[]
video_list =  [
    # "https://www.youtube.com/watch?v=vP_VtAXpc2I",
    # "https://www.youtube.com/watch?v=6bNZUzNQFwM",
    # "https://www.youtube.com/watch?v=3BjBnLaDmjs",
    # "https://www.youtube.com/watch?v=bsQBSVJoV04",
    # "https://www.youtube.com/watch?v=UsVPN5LVw7k",
    # "https://www.youtube.com/watch?v=4kfFggpdpis",
    # "https://www.youtube.com/watch?v=m0N8c7VJj9U",
    # "https://www.youtube.com/watch?v=B4b6r8nlf2k",
    # "https://www.youtube.com/watch?v=impZHFP5j1M",
    # "https://www.youtube.com/watch?v=5QiW3PVxF0k",
    # "https://www.youtube.com/watch?v=r_H6_G87KBI",
    # "https://www.youtube.com/playlist?list=PL4E8Oh0BGkkQL_3JsD66puTRm7AfKK4hO",
    # "https://www.youtube.com/watch?v=j-WUCdL-EiA",
    # "https://www.youtube.com/watch?v=QJWu-hTff94",
    "https://www.youtube.com/c/2ChicksGoingGreen/videos",
    # "https://www.youtube.com/watch?v=f1mXHpQ64lM",
    # "https://www.youtube.com/gorgeouslygreen",
    # "https://www.youtube.com/watch?v=zNSTzaZCJBM",
    # "https://www.youtube.com/watch?v=ZEmi0hVIc1c"
]

duration = 5  # Duration in seconds, adjust as needed

# No assertion here as we are testing if it runs without errors
processor.process_youtube_videos(video_list, duration)