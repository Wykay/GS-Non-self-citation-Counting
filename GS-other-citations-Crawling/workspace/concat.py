from utils import load_json, save_json


file1 = load_json("data/HCP.json")
file2 = load_json("data/HCP_cite_info_part3.json")

for item2 in file2:
     file1.append(item2)

save_json(file1,"data/HCP.json")