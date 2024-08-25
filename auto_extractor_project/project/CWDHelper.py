import os
import sys
import logging

def getCWD():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # If the script is packaged (i.e., running as an .exe)
    folder_to_watch = os.path.dirname(sys.executable)
    # folder_to_watch = os.path.dirname(os.path.abspath(__file__))

    # Change the current working directory to the script directory
    os.chdir(folder_to_watch)
    # folder_to_watch = os.path.dirname(os.path.abspath(__file__))
    logging.debug(f'<Executable File Location> : {os.path.abspath(__file__)}')
    logging.debug(f'<Folder to Watch> : {folder_to_watch}')
    return folder_to_watch