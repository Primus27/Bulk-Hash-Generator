"""
Title: Hash all files found in a directory or image
Author: Primus27
Version: 1.0
"""

# Import packages
import os
import argparse
from pathlib import Path
from title_generator import TitleGen
import hashlib
from datetime import datetime
try:
    from termcolor import colored as colour
except ImportError:
    exit("termcolor' module is missing.")

# Current program version
current_version = 1.0


def enum_files(folder_path):
    """
    Enumerates files in a path.
    :param folder_path: Root folder path for enumeration.
    :return: List containing all files in a folder.
    """
    # List of all files in path
    f_list = []
    # Enumerate files
    for root, dirs, files in os.walk(folder_path, topdown=True):
        for file in files:
            # Generate the absolute/relative path for each file
            file_path = os.path.join(root, file)
            # File exists (it should) and has a size greater than 0KB
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                f_list.append(file_path)
    return f_list


def get_file_hash(file_path, mode, blocksize=8192):
    """
    Generate a hash for a given file
    :param file_path: File to hash
    :param mode: Hashing mode
    :param blocksize: Size of chunks
    :return: File hash
    """
    hash_obj = hashlib.new(mode)
    with open(file_path, "rb") as file:
        chunk = file.read(blocksize)
        while chunk:
            hash_obj.update(chunk)
            chunk = file.read(blocksize)
    return hash_obj.hexdigest()


def file_output(obj):
    """
    Outputs list results to a file
    :param obj: Object to be output
    """
    try:
        # Open file and append
        with open(file_output_name, "a") as f:
            # Write to file if obj has data
            if isinstance(obj, list):
                for file in obj:
                    for i, item in enumerate(file):
                        if i == 0:
                            f.writelines(f"\n{item}\n")
                        else:
                            f.writelines(f"{item}\n")
                f.writelines("\n")
                print(colour("\n[*] File saved under '{f}'".format(
                    f=file_output_name)), "yellow")
            else:
                f.writelines(f"{obj}\n")
    # Inadequate permission to access location / save to location
    except PermissionError:
        if isinstance(obj, list):
            print(colour("[*] Error saving log - Permission denied"), "red")
    # Could not find path
    except OSError:
        if isinstance(obj, list):
            print(colour("[*] Error saving log - Path issues"), "red")


def main():
    """
    Main method
    """
    # Output title card
    title = TitleGen(text="Multi Hash", author="Primus27").title
    print(title)

    start_time = datetime.now()
    temp_msg = f"[*] Hashing started at: {start_time}\n"
    print(colour(temp_msg, "yellow"))
    if file_output_flag:
        file_output(temp_msg)

    # Enumerate files in path
    file_list = enum_files(user_path)

    # Files successfully hashed
    hashed_count = 0

    results_list = []

    # Calculate hashes and output
    for index, file in enumerate(file_list):
        path_str = f"PATH: {file}"
        print(path_str)
        local_hash_count = 0

        if file_output_flag:
            result = [path_str]

        for hash_type in user_hashes:
            file_hash = get_file_hash(file, hash_type)
            hash_str = f"{hash_type.upper()}: {file_hash}"
            print(hash_str)

            if file_output_flag:
                result.append(hash_str)

            if file_hash:
                local_hash_count += 1

        if file_output_flag:
            results_list.append(result)

        if local_hash_count == len(user_hashes):
            hashed_count += 1
        print()

    if file_output_flag:
        file_output(results_list)

    end_time = datetime.now()
    temp_msg = f"[*] {hashed_count}/{len(file_list)} files successfully hashed"
    if hashed_count == len(file_list):
        print(colour(temp_msg, "green"))
    else:
        print(colour(temp_msg, "red"))
    if file_output_flag:
        file_output(f"\n{temp_msg}")

    print(colour(f"[*] Hashing finished at {end_time}", "yellow"))
    print(colour(f"[*] Completion time: {end_time-start_time}", "yellow"))


if __name__ == '__main__':
    # Define argument parser
    parser = argparse.ArgumentParser()
    # Remove existing action groups
    parser._action_groups.pop()

    # Create a required and optional group
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    # Define arguments
    required.add_argument("-P", "--path", action="store", default="",
                          dest="user_path",
                          help="Scan path (absolute or relative)",
                          required=True)
    required.add_argument("-A", "--algorithm", nargs="*", action="store",
                          default=[], dest="algorithm",
                          help="Declare algorithms", required=True)
    optional.add_argument("-F", "--fileout", action="store_true",
                          dest="file_output_flag", help="Enable file output")
    optional.add_argument("-FN", "--filename", action="store",
                          default="", dest="file_output_name",
                          help="Declare a custom filename for file output")
    optional.add_argument("--version", action="version",
                          version="%(prog)s {v}".format(v=current_version),
                          help="Display program version")
    args = parser.parse_args()

    # Hashes to be used
    available_hashes = list(hashlib.algorithms_guaranteed)
    user_input = []
    user_input.extend(args.algorithm)
    user_input = [i.lower() for i in user_input]
    user_hashes = [user_hash for user_hash in user_input if
                   user_hash in available_hashes]

    # Folder path to hash (Relative (current) or Absolute)
    user_path = Path(args.user_path)

    # Output results to file
    if len(args.file_output_name) == 0:
        date_time = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")
        file_output_name = f"hashes-{date_time}.txt"
    else:
        file_output_name = args.file_output_name

    # Declare custom filename for output file
    file_output_flag = args.file_output_flag

    # Run main method
    main()
