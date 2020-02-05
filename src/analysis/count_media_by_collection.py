import json
import glob
import pandas as pd

id_map = {}

files = glob.glob("../../docs/item_sets/*.json")

for i in range(len(files)):
    if i % 100 == 0:
        print(str(i+1)+"/" + str(len(files)))
    file = files[i]
    with open(file) as f:
        df = json.load(f)

        item_set_id = df["o:id"]
        title = df["dcterms:title"][0]["@value"]

        id_map[item_set_id] = title

files = glob.glob("../data/item/*.json")

result = {}

for i in range(len(files)):
    if i % 100 == 0:
        print(str(i+1)+"/" + str(len(files)))
    file = files[i]
    with open(file) as f:
        df = json.load(f)

        medias = df["o:media"]

        itemsets = df["o:item_set"]
        for itemset in itemsets:
            item_set_id = itemset["o:id"]

            if item_set_id not in result:
                result[item_set_id] = {
                    "item": [],
                    "media": 0
                }

            obj = result[item_set_id]
            media = obj["media"]
            item = obj["item"]

            result[item_set_id]["media"] = media + len(medias)
            item.append(df["o:id"])

rows = []
rows.append(["id", "label", "# item", "# media"])

for item_set_id in result:
    obj = result[item_set_id]
    rows.append([item_set_id, id_map[item_set_id],
                 len(obj["item"]), obj["media"]])

df = pd.DataFrame(rows)
df.to_excel("../../docs/analysis/count_media_by_collection.xlsx", index=False, header=False)
