import sys
import utils
import urllib
import json
import argparse
import urllib.request
import os
import glob
import requests

files = glob.glob("../docs/api/items/*.json")

skip_flag = True

for i in range(len(files)):

    if i % 20 == 0:
        print(i+1, len(files))

    file = files[i]
    
    with open(file) as f:
        obj = json.load(f)

        uuid = str(obj["o:id"])

        if "bibo:identifier" in obj:
            uuid = obj["bibo:identifier"][0]["@value"]
        else:
            print(uuid)

        path = "../docs/iiif/"+uuid+"/manifest.json"

        # スキップフラグがTrueかつすでにファイルが存在する場合
        if skip_flag and os.path.exists(path):
            continue

        manifest_uri = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/" + uuid + "/manifest"

        try:

            manifest = requests.get(manifest_uri).json()

            # ディレクトリ作成
            dirpath = os.path.dirname(path)
            os.makedirs(dirpath, exist_ok=True)

            fw = open(path, 'w')
            json.dump(manifest, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


        except Exception as e:
            print(uuid, e)

    # break