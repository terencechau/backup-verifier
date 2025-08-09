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
    source_path = Path(source_path).resolve()
    hashes = {}
    for root, _, files in os.walk(source_path):
        for fname in files:
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