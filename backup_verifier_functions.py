import os
import hashlib
from pathlib import Path
import json
from datetime import datetime

def file_checksum(path):
    hash_sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_sha.update(chunk)
    return hash_sha.hexdigest()

def hash_folder(source_path):
    ignore_files = {".DS_Store"}  # add more filenames here if needed
    
    source_path = Path(source_path).resolve()
    hashes = {}
    for root, _, files in os.walk(source_path):
        for fname in files:
            if fname in ignore_files:
                continue  # skip unwanted files
            
            full_path = Path(root) / fname
            rel_path = str(full_path.relative_to(source_path))
            hashes[rel_path] = file_checksum(full_path)

    result = {
        "source_drive": source_path.name,
        "base_path": str(source_path),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "file_hashes": hashes
    }
    return result

def json_name_from_path(folder_path, name=None):
    folder_path = os.path.normpath(folder_path)
    ts = datetime.now().strftime("%Y%m%d")
    
    if folder_path.startswith("/Volumes/"):
        parts = folder_path.split(os.sep)
        base = parts[2] if len(parts) > 2 else "unknown_drive"
    elif folder_path.startswith("/Users/"):
        base = "local"
    else:
        base = os.path.basename(folder_path)
    
    if name:
        base = f"{base}_{name}"
    
    return f"hash_{base}_{ts}.json"

def save_hashes(hashes, output_path):
    with open(output_path, "w") as f:
        json.dump(hashes, f, indent=2)

def compare_hashes(data1, data2):
    hashes1 = data1["file_hashes"]
    hashes2 = data2["file_hashes"]

    all_files = set(hashes1) | set(hashes2)

    missing_in_2 = []
    missing_in_1 = []
    mismatches = []

    for file in all_files:
        h1 = hashes1.get(file)
        h2 = hashes2.get(file)
        if h1 is None:
            missing_in_1.append(file)
        elif h2 is None:
            missing_in_2.append(file)
        elif h1 != h2:
            mismatches.append(file)

    print(f"Missing in second: {len(missing_in_2)} files")
    print(f"Missing in first: {len(missing_in_1)} files")
    print(f"Mismatched files: {len(mismatches)} files")

    return missing_in_1, missing_in_2, mismatches