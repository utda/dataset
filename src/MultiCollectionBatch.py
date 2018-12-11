import csv
import os
from SingleCollectionBatch import single_collection_batch

csv_path = "data/list.csv"

site_arr = []

with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        site_obj = dict()
        site_arr.append(site_obj)
        site_obj["item_set_id"] = row[0]
        site_obj["site_name"] = row[1]

for site in site_arr:
    single_collection_batch(site["site_name"], site["item_set_id"])
