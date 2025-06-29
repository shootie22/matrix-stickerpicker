import os
from PIL import Image

def convert_jpg_to_png(root='.'):
    file_count = 0
    converted_count = 0
    deleted_count = 0

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg')):
                file_count += 1
                file_path = os.path.join(dirpath, filename)
                output_path = os.path.splitext(file_path)[0] + '.png'
                try:
                    img = Image.open(file_path)
                    img.save(output_path)
                    converted_count += 1
                    os.remove(file_path)  
                    deleted_count += 1
                    print(f"Converted and deleted: {file_path} -> {output_path}")
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")

    print(f"\nTotal .jpg/.jpeg files found: {file_count}")
    print(f"Files converted to .png: {converted_count}")
    print(f"Files deleted (originals): {deleted_count}")

if __name__ == "__main__":
    convert_jpg_to_png()
