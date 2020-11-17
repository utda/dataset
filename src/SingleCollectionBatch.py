import csv
import os
import argparse
import utils
import sys
from CollectionGenerator import collection_generator
from ItemsGenerator import items_generator
from LdGenerator import ld_generator
from ExcelGenerator import excel_generator


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


def single_collection_batch(config):

    items_generator(config)

    site_name = config["site_name"]

    site_dir = "../docs/collections/" + site_name

    if not os.path.isdir(site_dir):
        os.mkdir(site_dir)

    img_dir = site_dir + "/image"

    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    
    print("collection")
    collection_generator(config)

    metadata_dir = site_dir + "/metadata"

    if not os.path.isdir(metadata_dir):
        os.mkdir(metadata_dir)

    print("ld")
    ld_generator(config)
    
    print("excel")
    excel_generator(config)


if __name__ == "__main__":
    args = parse_args()
    key = args.site_name
    site_obj = utils.get_site_config(key)
    single_collection_batch(site_obj)