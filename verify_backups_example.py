from backup_verifier_functions import *

# List with path to parent directory inside drives to be compared
# (assume there are two drives)
drive_list = [" "]

# List with names of each folder to be compared inside parent directory
# (assume they're named the same way in each drive)
folder_list = [" "]

# Hash backup folder path
# (save location for hashes, ideally a third location not in either drive, 
# e.g., cloud storage)
backup_path = " "

# Hash each folder in each drive
# Save their hashes in a json file
# Compare each pair of hashes
for folder in folder_list:
    # Hash the same folder in each drive
    hashes = []
    for drive in drive_list:
        # Start time
        start_time = datetime.now()
        print(f"Hashing {folder} in {drive} started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Hash folder
        full_path = f"/{drive}/{folder}"
        current_hash = hash_folder(full_path)

        # End time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"Duration: {duration:.2f} seconds")

        # Save hash
        output_path = os.path.join(backup_path, json_name_from_path(drive, name=folder))
        save_hashes(current_hash, output_path)

        hashes.append(current_hash)

    # Compare the two hashes in memory
    start_time = datetime.now()
    print(f"Comparing folder {folder} hashes started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    hash_1, hash_2 = hashes
    print(compare_hashes(hash_1, hash_2))
    
    end_time = datetime.now()
    print(f"Comparison duration: {duration:.2f} seconds")