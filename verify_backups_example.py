from backup_verifier_functions import *

folder_1 = "folder_1_path"
folder_2 = "folder_2_path"

hash_1_path = "hash_1.json"
hash_2_path = "hash_2.json"

hashes_folder_1 = hash_folder(folder_1)
save_hashes(hashes_folder_1, hash_1_path)

hashes_folder_2 = hash_folder(folder_2)
save_hashes(hashes_folder_2, hash_2_path)

compare_hashes(hashes_folder_1, hashes_folder_2)