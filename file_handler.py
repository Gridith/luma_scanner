from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from os.path import getsize
import threading
import requests
import buzzer
import time
import re

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, on_new_file):
        self.on_new_file = on_new_file

    def on_created(self, event):
        if not event.is_directory:
            self.on_new_file(event.src_path)

def monitor_folder(path, on_new_file):
    event_handler = NewFileHandler(on_new_file)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_monitoring_in_background(path, on_new_file):
    thread = threading.Thread(target=monitor_folder, args=(path, on_new_file), daemon=True)
    thread.start()
    return thread

def on_new_file_detected(file_path):
    print(f"New file detected: {file_path}\nWaiting before sending..")
    while True: 
        first_size = getsize(file_path)
        time.sleep(5)
        second_size = getsize(file_path)
        delta_size = second_size - first_size
        
        print(f"Start: %s\nEnd: %s\nDelta: %s" % (first_size, second_size, delta_size))
        
        if delta_size == 0:
            send_mp3_file(file_path)
            return


def send_mp3_file(file_path):
    extraction_pattern = r'\d{2}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}'
    match = re.search(extraction_pattern, file_path)
    url = "https://central.capture.360fabriek.nl/projects/file"  
    data = {
        'projectName': match.group(0),
        'organisationId': 1
        }
    files = {
        'file': open(file_path, 'rb')
        }

    # Send the POST request
    print(f"Uploading %s with id %s" % (file_path, match.group(0)))
    start_time = time.time()
    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        print("File uploaded successfully.")
        print("Response:", response)
        
    except requests.exceptions.RequestException as e:
        print("Error uploading file:", e)
    time_taken = time.time() - start_time
    print(f"Time elapsed: %s" % time_taken)
    buzzer.two_beep()
    


if __name__ == "__main__":
    start_monitoring_in_background("/home/pi/Gaussian Scanner", on_new_file_detected)
    while True:
        time.sleep(2)