import backup_verifier_functions.py

hashes_drive_1 = hash_folder("drive_1_path")
save_hashes(hashes_drive_1, "output_hash_1_path.json")

hashes_drive_2 = hash_folder("drive_2_path")
save_hashes(hashes_drive_2, "output_hash_2_path.json")

compare_hashes(hashes_drive_1, hashes_drive_2)