import sys
import urllib
import utils
import json
import argparse
import urllib.request
import os

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


def items_generator(config):

    arg_item_set_id = config["item_set_id"]

    api_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api"

    output_dir = "../docs/api/items/"

    item_set_arr = arg_item_set_id.split(",")

    for item_set_id in item_set_arr:

        loop_flg = True
        page = 1

        while loop_flg:
            url = api_url + "/items?item_set_id=" + str(item_set_id) + "&page=" + str(
                page) + "&sort_by=uterms%3Asort&sort_order=asc"
            print(url)

            page += 1

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            response_body = response.read().decode("utf-8")
            data = json.loads(response_body.split('\n')[0])

            if len(data) > 0:
                for i in range(len(data)):
                    obj = data[i]

                    oid = obj["o:id"]

                    output_path = output_dir+"/"+str(oid)+".json"

                    with open(output_path, 'w') as outfile:
                        json.dump(obj, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

            else:
                loop_flg = False

if __name__ == "__main__":
    args = parse_args()
    key = args.site_name
    site_obj = utils.get_site_config(key)
    items_generator(site_obj)