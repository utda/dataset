import json
from SingleCollectionBatch import single_collection_batch

json_path = "../docs/collections/list.json"

site_arr = []

with open(json_path) as f:
    df = json.load(f)

for key in df:
    site_obj = dict()
    site_arr.append(site_obj)

    item_set_id_arr = df[key]["item_set_id"]

    item_set_id = ""
    for i in range(len(item_set_id_arr)):
        item_set_id += str(item_set_id_arr[i])
        if i != len(item_set_id_arr) - 1:
            item_set_id += ","

    site_obj["item_set_id"] = item_set_id
    site_obj["site_name"] = key

for site in site_arr:
    print(site)
    single_collection_batch(site["site_name"], site["item_set_id"])
