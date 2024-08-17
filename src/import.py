import argparse
import os
import shutil

def import_data_from_remote(url):
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/raw_data')

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Copy files from remote location to output directory
    for file in os.listdir(url):
        if os.path.isfile(os.path.join(url, file)):
            shutil.copy(os.path.join(url, file), output_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)

    args = parser.parse_args()

    import_data_from_remote(args.url)
