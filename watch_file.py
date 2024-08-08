from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


def watch_file(watch_dir=None,
               on_created=lambda event: False,
               on_modified=lambda event: False,
               on_deleted=lambda event: False,
               on_moved=lambda event: False,
               on_any_event=lambda event: False):
    observer = Observer()
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    event_handler.on_any_event = on_any_event
    observer.schedule(event_handler, watch_dir, True)
    observer.start()
    return observer, event_handler
