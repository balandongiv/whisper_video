import os
import re


def get_file_name_without_extension(file_path):
    """
    Returns the file name without the extension from the given file path.

    Args:
    file_path (str): The full path of the file.

    Returns:
    str: The file name without the extension.
    """
    # Extract the base name (file name with extension)
    base_name = os.path.basename(file_path)

    # Split the base name into file name and extension, and return just the file name
    file_name_without_extension, _ = os.path.splitext(base_name)

    return file_name_without_extension

def create_file_detail(output_fname, url='From Local Video',local_save_directory=None):
    """
    Create file details for saving and return as a dictionary.
    """
    # local_save_dir = '/home/rpb/IdeaProjects/my_gpu_env'
    # gdrive = '/content/drive/MyDrive/'

    save_directory_aux = os.path.join(local_save_directory,'process',output_fname)

    if not os.path.exists(save_directory_aux):
        os.makedirs(save_directory_aux)
        # print(f"Directory '{save_directory_aux}' created.")
    # vid_fname = f"{output_fname[:20]}.mp4"
    fname_word = os.path.join(local_save_directory, f"{output_fname}.docx")

    return {
        'url': url,
        'video_title_clean': output_fname,
        # 'vid_fname': vid_fname,
        'fname_word': fname_word,
        'save_directory_aux':save_directory_aux
    }
def get_current_script_directory():
    """
    Returns the directory in which the current script is running.
    """
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)

    # Extract the directory from the absolute path
    current_directory = os.path.dirname(current_script_path)

    return current_directory

def clean_and_format_string(input_string):
    # Remove special characters and spaces, and replace them with underscores
    cleaned_string = re.sub(r'[^a-zA-Z0-9]+', '_', input_string)

    # Remove leading and trailing underscores
    cleaned_string = cleaned_string.strip('_')

    # Convert to lowercase if needed
    formatted_string = cleaned_string.lower()
    # Optionally, you can also limit the length of the file name
    max_length = 255  # Maximum file name length for most file systems

    return formatted_string[:max_length]



