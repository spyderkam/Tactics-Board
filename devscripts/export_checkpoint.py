#!/usr/bin/env python3

import os
import zipfile

def export_checkpoint(directory):
    with zipfile.ZipFile(f'{directory}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('checkpoint_v1'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'checkpoint_v1')
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    import sys
  
    if len(sys.argv) < 2:
        print("Usage: python export_checkpoint.py <folder_path>")

    directory = sys.argv[1]
    export_checkpoint(directory)
    print(f"Checkpoint exported to {directory}.zip")
