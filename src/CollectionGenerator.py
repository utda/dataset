import sys
import utils
import urllib
import json
import argparse
import urllib.request
import os
import glob

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'site_name',
        action='store',
        type=str,
        help='Site name. ex: hyakki')

    return parser.parse_args(args)


def collection_generator(config):

    site_name = config["site_name"]
    arg_item_set_id = config["item_set_id"]

    collection_uri = "https://archdataset.dl.itc.u-tokyo.ac.jp/collections/" + site_name + "/image/collection.json"

    output_path = "../docs/collections/" + site_name + "/image/collection.json"

    collection = dict()
    collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
    collection["@id"] = collection_uri
    collection["@type"] = "sc:Collection"
    collection["vhint"] = "use-thumb"

    labels = []
    if "label" in config and config["label"] != None:
        labels.append({
            "@value" : config["label"],
            "@language" : "ja"
        })
    if "label_en" in config and config["label_en"] != None:
        labels.append({
            "@value" : config["label_en"],
            "@language" : "en"
        })
    if len(labels) > 0:
        collection["label"] = labels

    descriptions = []
    if "description" in config and config["description"] != None:
        descriptions.append({
            "@value" : config["description"],
            "@language" : "ja"
        })
    if "description_en" in config and config["description_en"] != None:
        descriptions.append({
            "@value" : config["description_en"],
            "@language" : "en"
        })
    if len(descriptions) > 0:
        collection["description"] = descriptions

    manifests = []
    collection["manifests"] = manifests

    item_set_arr = arg_item_set_id.split(",")

    files = glob.glob("../docs/api/items/*.json")

    targets = {}

    for file in files:
        with open(file) as f:
            df = json.load(f)

            if "o:item_set" not in df:
                continue

            item_set_objs = df["o:item_set"]
            for obj in item_set_objs:
                item_set_id = str(obj["o:id"])

                if item_set_id in item_set_arr:
                    sort = ""
                    if "uterms:sort" in df:
                        sort = df["uterms:sort"][0]["@value"]
                    
                    if sort not in targets:
                        targets[sort] = []
                    
                    if df not in targets[sort]:
                        targets[sort].append(df)

    for key in sorted(targets):

        arr = targets[key]

        for obj in arr:

            uuid = str(obj["o:id"])

            if "bibo:identifier" in obj:
                uuid = obj["bibo:identifier"][0]["@value"]
            else:
                print(uuid)

            manifest_uri = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/" + uuid + "/manifest"

            title = "No Title"

            if "dcterms:title" in obj:
                title = obj["dcterms:title"][0]["@value"]

            manifest = dict()
            manifests.append(manifest)
            manifest["@id"] = manifest_uri
            manifest["@type"] = "sc:Manifest"
            manifest["label"] = title

            if "dcterms:rights" in obj:
                manifest["license"] = obj["dcterms:rights"][0]["@id"]

            if "foaf:thumbnail" in obj:
                manifest["thumbnail"] = obj["foaf:thumbnail"][0]["@id"]

    fw = open(output_path, 'w')
    json.dump(collection, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == "__main__":
    args = parse_args()
    key = args.site_name
    site_obj = utils.get_site_config(key)
    collection_generator(site_obj)