import os
import shutil
import time
import json

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    else:
        config = {}
    return config

def cleanup_dist_folder(dist_folder):
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)

def main():
    config = load_config()
    cleanup_config = config.get('cleanup', {})
    cleanup_enabled = cleanup_config.get('enabled', False)
    cleanup_interval = cleanup_config.get('interval', 60)
    dist_folder = config.get('cleanup_folder_path', './dist')

    if cleanup_enabled:
        while True:
            cleanup_dist_folder(dist_folder)
            time.sleep(cleanup_interval)

if __name__ == '__main__':
    main()
