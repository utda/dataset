import json
import utils
from SingleCollectionBatch import single_collection_batch

site_arr = utils.load_config()

for i in range(len(site_arr)):
    site = site_arr[i]
    print(i+1, len(site_arr), site["site_name"])
    single_collection_batch(site)