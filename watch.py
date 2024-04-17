import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher(FileSystemEventHandler):
    def __init__(self, cmd):
        self.cmd = cmd

    def process(self, event):
        """
        重新啟動Flask應用程式
        """
        print(f'Restarting Flask app due to file change: {event.src_path}')
        self.restart_app()

    def restart_app(self):
        """
        執行重新啟動Flask應用程式的命令
        """
        subprocess.run(self.cmd, shell=True)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

if __name__ == "__main__":
    # Flask app啟動命令
    cmd = "python main.py"

    # 監聽當前目錄
    event_handler = Watcher(cmd)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
