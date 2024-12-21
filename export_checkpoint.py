
import zipfile
import os

def export_checkpoint():
    with zipfile.ZipFile('checkpoint_v1_export.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('checkpoint_v1'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'checkpoint_v1')
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    export_checkpoint()
    print("Checkpoint exported to checkpoint_v1_export.zip")
