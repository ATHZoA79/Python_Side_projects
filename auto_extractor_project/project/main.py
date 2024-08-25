import shutil
import os
import sys
import logging
import patoolib
import rarfile
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from CWDHelper import getCWD

def extract_rar(file_path, output_dir):
    try:
        # Open the rar file
        with rarfile.RarFile(file_path) as rf:
            # Extract all files
            rf.extractall(path=output_dir)
            logging.info(f"Extracted {file_path} to {output_dir}")

    except rarfile.BadRarFile:
        logging.error(f"File is not a valid RAR archive: {file_path}")
    except rarfile.RarFile as e:
        # Check if the exception is related to password protection
        if 'password' in str(e).lower():
            logging.warning(f"Skipping {file_path}, password is required.")
        else:
            logging.error(f"Failed to extract {file_path}: {e}")

class FileMoveHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))
            logging.info(f'<Operating File name> : {file_name}\nFile path : {file_path}\n')

            # Check if the file is a .zip or .rar
            if file_extension.lower() in ['.zip', '.rar']:
                # Create a folder with the same name as the file
                folder_path = os.path.join(os.path.dirname(file_path), file_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    logging.info(f"<Created Folder>: {folder_path}\n")
                    shutil.move(file_path, folder_path)
                    moved_file_path = os.path.join(folder_path, file_name+file_extension)
                    logging.info(f"<Moved File Path>: {moved_file_path}\n")
                    if file_extension == '.rar':
                        try:
                            # Open the rar file
                            with rarfile.RarFile(moved_file_path) as rf:
                                # Extract all files
                                rf.extractall(path=folder_path)
                                logging.info(f"== Extracted {moved_file_path} to {folder_path} ==")

                        except rarfile.BadRarFile:
                            logging.error(f"== File is not a valid RAR archive: {moved_file_path} ==")
                        except Exception as e:
                            # Check if the exception is related to password protection
                            if 'password' in str(e).lower():
                                logging.warning(f"== Skipping {moved_file_path}, password is required. {e} ==")
                            else:
                                logging.error(f"== Failed to extract {moved_file_path}: {e} ==")
                    # elif file_extension == '.zip':
                    #     try:
                    #         patoolib.extract_archive(moved_file_path, outdir=folder_path)
                    #     except patoolib.util.PatoolError as e:
                    #         if 'password' in str(e).lower():
                    #             logging.info(f"== Skipping extraction of {file_path}, password is required. ==")
                    #         else:
                    #             logging.info(f"== Failed to extract {file_path} due to an unexpected error: {e} ==")
                    # try:
                    #     patoolib.extract_archive(moved_file_path, outdir=folder_path)
                    # except patoolib.util.PatoolError as e:
                    #     if 'password' in str(e).lower():
                    #         logging.info(f"== Skipping extraction of {moved_file_path}, password is required. ==")
                    #     else:
                    #         logging.info(f"== Failed to extract {moved_file_path} due to an unexpected error: {e} ==")

def main():
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = os.path.dirname(os.path.abspath(__file__))
    logging.info(f'<Logging Path> : {path}')
    log_event_handler = LoggingEventHandler()
    log_observer = Observer()
    log_observer.schedule(log_event_handler, path, recursive=True)
    log_observer.start()
    try:
        while log_observer.is_alive():
            log_observer.join(1)
    finally:
        log_observer.stop()
        log_observer.join()

if __name__ == "__main__":
    folder_to_watch = getCWD()
    file_event_handler = FileMoveHandler()
    file_observer = Observer()
    file_observer.schedule(file_event_handler, folder_to_watch, recursive=False)
    file_observer.start()
    main()

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        file_observer.stop()
    file_observer.join()