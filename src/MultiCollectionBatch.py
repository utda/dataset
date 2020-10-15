import json
from SingleCollectionBatch import single_collection_batch

json_path = "../docs/collections/list.json"

site_arr = []

with open(json_path) as f:
    df = json.load(f)

for key in df:
    site_obj = dict()
    site_arr.append(site_obj)

    config = df[key]

    item_set_id_arr = config["item_set_id"]

    item_set_id = ""
    for i in range(len(item_set_id_arr)):
        item_set_id += str(item_set_id_arr[i])
        if i != len(item_set_id_arr) - 1:
            item_set_id += ","

    site_obj["item_set_id"] = item_set_id
    site_obj["site_name"] = key
    site_obj["label"] = config["label"] if "label" in config else None
    site_obj["label_en"] = config["label_en"] if "label_en" in config else None
    site_obj["description"] = config["description"] if "description" in config else None
    site_obj["description_en"] = config["description_en"] if "description_en" in config else None

flg = True

for i in range(len(site_arr)):
    site = site_arr[i]
    print(i+1, len(site_arr), site["site_name"])
    
    if site["site_name"] == "50nenshi":
        flg = False
    if flg:
        single_collection_batch(site)