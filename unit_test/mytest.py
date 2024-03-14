import unittest

from whispervideos.whispervid import VideoProcessor


class TestVideoProcessor(unittest.TestCase):

    def setUp(self):
        # Initialize VideoProcessor before each test
        self.processor = VideoProcessor()


    def test_process_youtube_videos(self):
        video_list = [
            # '../unit_test/how_copyright_works_.mp4',
            'https://www.youtube.com/watch?v=-DP1i2ZU9gk',
            'https://www.youtube.com/watch?v=FlGjISF3l78',  # Uncomment if you want to test with a YouTube URL
        ]
        duration = 10  # Duration in seconds, adjust as needed

        # No assertion here as we are testing if it runs without errors
        self.processor.process_youtube_videos(video_list, duration)

# This allows running the tests directly from the script
if __name__ == '__main__':
    unittest.main()
