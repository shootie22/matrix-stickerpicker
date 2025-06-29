import os
import subprocess

packs_dir = "../PACKS"
add_to_index = "../web/packs"

for folder in os.listdir(packs_dir):
    folder_path = os.path.join(packs_dir, folder)
    if os.path.isdir(folder_path):
        command = [
            "sticker-pack",
            folder_path,
            "--title", folder,
            "--add-to-index", add_to_index
        ]
        print("Executing:", " ".join(command))
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {folder}: {e}")
