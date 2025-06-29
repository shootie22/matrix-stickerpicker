import os
import json

def find_json_files(directory):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def prompt_paths():
    paths = []
    print("Enter folder paths (enter 'X' to finish):")
    while True:
        p = input("Path: ").strip()
        if p.upper() == "X":
            break
        if not os.path.isdir(p):
            print("Invalid path. Try again.")
            continue
        paths.append(p)
    return paths

def prompt_sizes(paths):
    entries = []
    for path in paths:
        while True:
            size_str = input(f"Enter square size for '{path}': ").strip()
            if size_str.isdigit():
                entries.append({
                    "path": path,
                    "size": int(size_str),
                    "files": find_json_files(path)
                })
                break
            print("Invalid input. Must be an integer.")
    return entries

def show_overview(entries):
    print("\n=== OVERVIEW ===")
    for i, entry in enumerate(entries, 1):
        print(f"[{i}] Path: {entry['path']}")
        print(f"    Size: {entry['size']}")
        print(f"    JSONs: {len(entry['files'])} file(s)")
    print("================\n")

def apply_changes(entries):
    for entry in entries:
        for file in entry["files"]:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for sticker in data.get("stickers", []):
                    info = sticker.get("info", {})
                    thumbnail_info = info.get("thumbnail_info", {})

                    info["w"] = info["h"] = entry["size"]
                    thumbnail_info["w"] = thumbnail_info["h"] = entry["size"]

                with open(file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

            except Exception as e:
                print(f"Error processing {file}: {e}")

def main():
    paths = prompt_paths()
    if not paths:
        print("No paths given. Exiting.")
        return

    entries = prompt_sizes(paths)

    while True:
        show_overview(entries)
        choice = input("Accept changes (A), Abort (Q), or Change a size (enter number): ").strip().upper()

        if choice == "A":
            apply_changes(entries)
            print("Changes applied.")
            break
        elif choice == "Q":
            print("Aborted.")
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(entries):
                while True:
                    new_size = input(f"Enter new size for '{entries[idx]['path']}': ").strip()
                    if new_size.isdigit():
                        entries[idx]["size"] = int(new_size)
                        break
                    else:
                        print("Invalid input. Must be an integer.")
            else:
                print("Invalid index.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
