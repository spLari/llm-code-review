# How to use:
# To overwrite the original files:
# python remove_characters.py origin_path

# To save in new folder:
# remove_characters.py origin_path -d destination_path

import argparse
import os
import re

# Function to create the destination folder.
def create_destination_folder(destination_folder):
    if destination_folder:
        os.makedirs(destination_folder, exist_ok=True)

# Function to remove characters.
def remove_characters(file):
    # Remove all @@ and the content between it.
    file = re.sub(r'@@.*?@@', '', file)

    # Remove the + or - in the beginning of the lines.
    file = re.sub(r'^[\+\-]\s?', ' ', file, flags=re.MULTILINE)

    return file

# Function to process the file to be adjusted.
def adjust_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        cleaned_content = remove_characters(content)

        return cleaned_content
    else:
        return [False, file_path]

# Function to save the processed file after remove the characters.
def save_file(file_name, destination_folder, file_path, cleaned_file):
    if destination_folder:
        destination_path = os.path.join(destination_folder, file_name)
    else:
        # overwrite the original file
        destination_path = file_path

    with open(destination_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_file)

# Main function.
def process_files(content_folder, destination_folder=None):
    create_destination_folder(destination_folder)
    num_files = 0

    for file_name in os.listdir(content_folder):
        file_path = os.path.join(content_folder, file_name)
        cleaned_file = adjust_file(file_path)

        if isinstance(cleaned_file, list):
            print("An error occurred processing the file: " + file_path)
            break
        else:
            save_file(file_name, destination_folder, file_path, cleaned_file)
            num_files +=1

    print(str(num_files) + " were processed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove characters @@...@@ and -/+")
    parser.add_argument("origin", help="Origin directory of files")
    parser.add_argument("-d", "--destination", help="Output directory (optional). If not given, overwrite the original files.")

    args = parser.parse_args()

    process_files(args.origin, args.destination)
