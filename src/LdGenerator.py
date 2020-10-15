import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
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

    parser.add_argument(
        'item_set_id',
        action='store',
        type=str,
        help='ID of itemSet. ex: 2')

    return parser.parse_args(args)


def ld_generator(site_name, arg_item_set_id):

    output_path = "../docs/collections/" + site_name + "/metadata/data.json"

    collection = []

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

            collection.append(obj)

    fw = open(output_path, 'w')
    json.dump(collection, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    # ld_str = json.dumps(collection)

    # g = Graph().parse(data=ld_str, format='json-ld')

    # g.serialize(format='n3', destination=output_path.replace(".json", ".n3"))
    # g.serialize(format='nt', destination=output_path.replace(".json", ".nt"))
    # g.serialize(format='turtle', destination=output_path.replace(".json", ".ttl"))
    # g.serialize(format='pretty-xml', destination=output_path.replace(".json", ".rdf"))


if __name__ == "__main__":
    args = parse_args()

    site_name = args.site_name
    arg_item_set_id = args.item_set_id

    ld_generator(site_name, arg_item_set_id)
