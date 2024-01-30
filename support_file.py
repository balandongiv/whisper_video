import re



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



