import logging
import os
import re

import pandas as pd
from tqdm import tqdm

# Import your modules
from whispervideos.docs_creation import add_images_to_word_document, create_docx_for_failed_video
from whispervideos.support_file import get_filename_without_extension, \
    clean_and_format_string, get_desktop_path
from whispervideos.transcribe_video import safe_transcribe
from whispervideos.video_proc import (segment_audio, capture_frames, download_youtube_video, process_urls,
                                      get_youtube_video_title,
                                      create_file_details)

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class VideoProcessor:
    def __init__(self, local_save_directory=None):
        """
    Sets the local_save_directory to the desktop path if it's None.
    """
        if local_save_directory is None:
            self.local_save_directory = get_desktop_path()
        else:
            self.local_save_directory = local_save_directory

    def process_video_now(self, video_path, durat, max_width=6.5, max_height=9.0):
        logger.info('Step 1: Segmenting audio')
        segments = segment_audio(video_path["vid_fname"], video_path['save_directory_aux'], segment_duration_seconds=durat)

        logger.info('Step 2: Capturing and extracting frames')
        all_path = capture_frames(video_path["vid_fname"], video_path['save_directory_aux'], interval=durat)

        df2 = pd.DataFrame(all_path, columns=['image_path'])
        df = pd.DataFrame(segments, columns=['SegmentPath'])

        logger.info('Step 3: Processing segments into pandas DataFrame')
        df['SegmentNumber'] = df['SegmentPath'].apply(lambda x: int(x.split('_')[-1].split('.')[0]))
        df = df.sort_values(by='SegmentNumber')

        logger.info('Transcribing segments')
        df['Transcription'] = df['SegmentPath'].apply(safe_transcribe)
        combined_df = pd.concat([df2, df], axis=1)

        add_images_to_word_document(combined_df, video_path['filename_word'], max_width, max_height, video_path['url'], num_images=10)

    def process_video(self, durat, video_url):
        logger.info(f'Processing video URL: {video_url}')
        url_pattern = re.compile(r'^https?://\S+')

        if url_pattern.match(video_url):
            video_path = download_youtube_video(video_url, self.local_save_directory)
        else:
            vid_name = get_filename_without_extension(video_url)
            vid_name = clean_and_format_string(vid_name)
            video_path = create_file_details(vid_name, video_url, local_save_directory=self.local_save_directory)
            video_path["vid_fname"] = video_url

        if not os.path.exists(video_path["filename_word"]):
            self.process_video_now(video_path, durat)
        else:
            logger.info(f"Document '{video_path['video_title_clean']}' already exists. Skipping.")

    def process_youtube_videos(self, video_list, duration):
        processed_urls = process_urls(video_list)

        for youtube_url in tqdm(processed_urls):
            try:
                self.process_video(duration, youtube_url)
            except Exception as e:
                logger.error(f"An error occurred while processing {youtube_url}: {e}")
                ytitle = get_youtube_video_title(youtube_url)
                create_docx_for_failed_video(ytitle, e, self.local_save_directory)

