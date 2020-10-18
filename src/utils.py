import json

def load_config():
    site_arr = []
    path = "../docs/collections/list.json"

    with open(path) as f:
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

    return site_arr

def get_site_config(key):

    site_arr = load_config()

    for obj in site_arr:
        if obj["site_name"] == key:
            return obj

    return None