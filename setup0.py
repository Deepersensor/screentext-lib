import json
import os
import subprocess
import threading
import time
import shutil
# ...existing code...

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    default_config = {
        "screenshot_path": os.path.expanduser('~/Pictures/Screenshots'),
        "watch_screenshot_path": False,
        "run_on_startup": False
    }
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    else:
        config = default_config
    return config

def setup_run_on_startup(run_on_startup):
    if run_on_startup:
        # Create autostart directory if it doesn't exist
        autostart_dir = os.path.expanduser('~/.config/autostart')
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        
        # Path to the desktop entry file
        desktop_entry_path = os.path.join(autostart_dir, 'screentext.desktop')
        
        # Content of the desktop entry file
        desktop_entry_content = f"""[Desktop Entry]
Type=Application
Exec=python {os.path.abspath(__file__)}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=ScreenText
Comment=Extract text from screenshots automatically
"""
        # Write the desktop entry file
        with open(desktop_entry_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry_content)
    else:
        # Remove the desktop entry file if it exists
        desktop_entry_path = os.path.expanduser('~/.config/autostart/screentext.desktop')
        if os.path.exists(desktop_entry_path):
            os.remove(desktop_entry_path)


def setup_environment(config=None):
    if config is None:
        config = load_config()
    screenshot_path = config.get('screenshot_path', os.path.expanduser('~/Pictures/Screenshots'))
    run_on_startup = config.get('run_on_startup', False)
    
    # Set up screenshot path
    if screenshot_path and not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)
    
    # Set up run on startup
    setup_run_on_startup(run_on_startup)
    
    # Schedule cleanup task if enabled
    cleanup_config = config.get('cleanup', {})
    cleanup_enabled = cleanup_config.get('enabled', False)
    if cleanup_enabled:
        cleanup_thread = threading.Thread(target=run_cleanup_task, args=(config,))
        cleanup_thread.daemon = True
        cleanup_thread.start()
    
    # Return configurations for further use
    return config

def run_cleanup_task(config):
    cleanup_interval = config.get('cleanup', {}).get('interval', 60)
    dist_folder = config.get('cleanup_folder_path', './dist')
    while True:
        cleanup_dist_folder(dist_folder)
        time.sleep(cleanup_interval)

def cleanup_dist_folder(dist_folder):
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)

def watch_screenshots(screenshot_path, verbosity):
    # Watch the screenshot path for new images and process them
    import time
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class ScreenshotHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            else:
                # Process the new image file
                image_path = event.src_path
                if verbosity == 'aggressive':
                    print(f"New image detected: {image_path}")
                from screentext import process_image
                process_image(image_path, verbosity)

    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, path=screenshot_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    config = setup_environment()
    if config.get('watch_screenshot_path'):
        watch_screenshots(config.get('screenshot_path'), config.get('verbosity', 'normal'))
