import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from document import CouchdbDocument
import os

class SimpleWatcher(FileSystemEventHandler):

    def process(self, event):
        print event.src_path, event.event_type
        if os.path.isfile(event.src_path):
            CouchdbDocument(event.src_path).save()

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)


if __name__ == "__main__":
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(SimpleWatcher(), path=args[0] if args else '.', recursive=True)
    observer.start()
    print "start"

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()






