import logging
import os
import platform
import re

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_desktop_path():
    """
    Returns the path to the Desktop directory depending on the operating system.
    """
    system = platform.system()
    if system == "Windows":
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
    elif system == "Linux":
        desktop = os.path.join(os.environ["HOME"], "Desktop")
    else:
        raise OSError("Unsupported operating system")
    return desktop

def get_filename_without_extension(file_path):
    """
    Extracts the filename without its extension from a given file path.

    Args:
        file_path (str): The full path of the file.

    Returns:
        str: Filename without the extension.
    """
    # Extracting the base name (filename with extension)
    base_name = os.path.basename(file_path)

    # Splitting the base name into filename and extension, returning only the filename
    filename_without_extension, _ = os.path.splitext(base_name)

    return filename_without_extension

def create_file_details(output_filename, url='From Local Video', local_save_directory=None):
    """
    Creates and returns file details for saving as a dictionary.

    Args:
        output_filename (str): The base name for the output file.
        url (str, optional): The source URL of the file. Defaults to 'From Local Video'.
        local_save_directory (str, optional): The directory to save the file. Defaults to None.

    Returns:
        dict: Dictionary containing file details.
    """
    save_directory_aux = os.path.join(local_save_directory, 'process', output_filename)

    if not os.path.exists(save_directory_aux):
        os.makedirs(save_directory_aux)
        logging.info(f"Directory '{save_directory_aux}' created.")

    filename_word = os.path.join(local_save_directory, f"{output_filename}.docx")

    return {
        'url': url,
        'video_title_clean': output_filename,
        'filename_word': filename_word,
        'save_directory_aux': save_directory_aux
    }

def get_current_script_directory():
    """
    Determines the directory of the currently running script.

    Returns:
        str: Directory path of the current script.
    """
    # Retrieving the absolute path of the current script
    current_script_path = os.path.abspath(__file__)

    # Extracting the directory from the absolute path
    current_directory = os.path.dirname(current_script_path)

    return current_directory

def clean_and_format_string(input_string):
    """
    Cleans a string by removing special characters and spaces, replacing them with underscores.

    Args:
        input_string (str): The string to be cleaned.

    Returns:
        str: Cleaned and formatted string.
    """
    # Removing special characters and spaces, replacing with underscores
    cleaned_string = re.sub(r'[^a-zA-Z0-9]+', '_', input_string)

    # Removing leading and trailing underscores
    cleaned_string = cleaned_string.strip('_')

    # Converting to lowercase
    formatted_string = cleaned_string.lower()

    # Limiting the length of the filename
    max_length = 255  # Maximum filename length for most file systems

    return formatted_string[:max_length]
