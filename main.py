import os
import re

import pandas as pd
import whisper
from tqdm import tqdm

from docs_creation import add_images_to_word_document, create_docx_for_each_title
from video_proc import segment_audio, capture_frames, download_youtube_video, process_urls, get_youtube_video_title, \
    create_file_detail

model = whisper.load_model("small")




def safe_transcribe(path):
    try:
        # Attempt to transcribe
        return model.transcribe(path, language="en")
    except Exception as e:
        # If transcription fails, handle the exception
        print(f"Error transcribing {path}: {e}")
        return f"Error transcribing {path}: {e}"


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

    segments = segment_audio(video_path["vid_fname"], segment_duration_seconds=durat)


    print('step 2: I am currently capturing and extracting the frame')
    all_path = capture_frames(video_path["vid_fname"], interval=durat, output_folder=video_path['video_title_clean'])

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


def process_video(durat, video_url):

    # Rest of your existing code
    url_pattern = re.compile(r'^https?://\S+')
    if url_pattern.match(video_url):

        # video_url = youtube_video_url
        video_path = download_youtube_video(video_url)
    else:
        # video_path=video_url
        video_path=create_file_detail(video_url,url='From local download')





    if not os.path.exists(video_path["fname_word"]):

        process_video_now(video_path,durat)
    else:
        print(f"Document '{video_path['video_title_clean']}' already exists. Skipping.")

# video_urls_playlist=[
    # 'brand_protection_wha.mp4',
    # 'https://youtu.be/J38Yq85ZoyY',
# ]

# video_urls_playlist=[
#     'brand_protection_wha.mp4',
#     'https://youtu.be/J38Yq85ZoyY',
# ]

video_urls_playlist=[
    'https://youtu.be/J38Yq85ZoyY',
]

processed_urls = process_urls(video_urls_playlist)

duration = 10


for youtube_urlx in tqdm(processed_urls):
    local_save_directory = '/home/rpb/IdeaProjects/my_gpu_env'
    try:
        process_video(duration, youtube_urlx)
    except Exception as e:
        print(f"An error occurred while processing {youtube_urlx}: {e}")
        ytitle = get_youtube_video_title(youtube_urlx)
        create_docx_for_each_title(ytitle, e,local_save_directory)


# print(processed_urls)



