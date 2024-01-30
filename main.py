import os
import re

import pandas as pd
from tqdm import tqdm

from docs_creation import add_images_to_word_document, create_docx_for_each_title
from support_file import get_current_script_directory, get_file_name_without_extension, clean_and_format_string
from transcribe_video import safe_transcribe
from video_proc import segment_audio, capture_frames, download_youtube_video, process_urls, get_youtube_video_title, \
    create_file_detail


def process_video_now(video_path,durat,max_width = 6.5,max_height = 9.0  ):
    """
        max_width = 6.5  # 8.5 inches - 1 inch margin on each side
    max_height = 9.0  # 11 inches - 1 inch margin on top and bottom

    :param video_path:
    :param durat:
    :param max_width:
    :param max_height:
    :return:
    """
    print('step 1')

    segments = segment_audio(video_path["vid_fname"],video_path['save_directory_aux'], segment_duration_seconds=durat)


    print('step 2: I am currently capturing and extracting the frame')
    all_path = capture_frames(video_path["vid_fname"], video_path['save_directory_aux'],interval=durat)

    df2 = pd.DataFrame(all_path, columns=['image_path'])

    df = pd.DataFrame(segments, columns=['SegmentPath'])

    print('step 3: Im currently segment the and make it into pandas')
    df['SegmentNumber'] = df['SegmentPath'].apply(lambda x: int(x.split('_')[-1].split('.')[0]))
    df = df.sort_values(by='SegmentNumber')
    print(' This may take some time, but i am currently whispering shhhhhh each of the segment')
    # Apply the safe_transcribe function to each item in the DataFrame column
    df['Transcription'] = df['SegmentPath'].apply(safe_transcribe)
    combined_df = pd.concat([df2, df], axis=1)



    add_images_to_word_document(combined_df, video_path['fname_word'], max_width, max_height, video_path['url'],num_images=10)


def process_video(durat, video_url,local_save_directory):

    # Rest of your existing code
    url_pattern = re.compile(r'^https?://\S+')
    if url_pattern.match(video_url):

        # video_url = youtube_video_url
        video_path = download_youtube_video(video_url,local_save_directory)
    else:
        # video_path=video_url
        # vid_name file_extension = os.path.splitext(video_url)
        vid_name=get_file_name_without_extension(video_url)
        vid_name=clean_and_format_string(vid_name)
        video_path=create_file_detail(vid_name,video_url,local_save_directory=local_save_directory)
        # video_path["vid_fname"] = os.path.join(local_save_directory,'process',output_fname)
        video_path["vid_fname"]=video_url



    if not os.path.exists(video_path["fname_word"]):

        process_video_now(video_path,durat)
    else:
        print(f"Document '{video_path['video_title_clean']}' already exists. Skipping.")

def process_youtube_videos(video_list, duration,path_docs=None):
    """
    Processes a list of YouTube video URLs.

    Args:
    processed_urls (list): A list of YouTube video URLs to process.
    duration (int): Duration for processing videos.
    """
    if path_docs is None:
        local_save_directory=get_current_script_directory()

    processed_urls = process_urls(video_list)
    # local_save_directory = '/home/rpb/IdeaProjects/my_gpu_env'

    for youtube_urlx in tqdm(processed_urls):
        try:
            # Assuming process_video is a predefined function
            process_video(duration, youtube_urlx,local_save_directory)
        except Exception as e:
            print(f"An error occurred while processing {youtube_urlx}: {e}")
            # Assuming get_youtube_video_title is a predefined function
            ytitle = get_youtube_video_title(youtube_urlx)
            # Assuming create_docx_for_each_title is a predefined function
            create_docx_for_each_title(ytitle, e, local_save_directory)

# video_list=[
    # 'brand_protection_wha.mp4',
    # 'https://youtu.be/J38Yq85ZoyY',
# ]

video_list=[
    'how_copyright_works_.mp4',
    'https://youtu.be/J38Yq85ZoyY',
]

# video_list=[
#     'https://youtu.be/J38Yq85ZoyY',
# ]





duration = 10

process_youtube_videos(video_list, duration)






