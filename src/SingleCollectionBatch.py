import csv
import os
import argparse
import sys
from CollectionGenerator import collection_generator
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

    parser.add_argument(
        'item_set_id',
        action='store',
        type=str,
        help='ID of itemSet. ex: 2')

    return parser.parse_args(args)


def single_collection_batch(site_name, arg_item_set_id):
    site_dir = "../docs/collections/" + site_name

    if not os.path.isdir(site_dir):
        os.mkdir(site_dir)

    img_dir = site_dir + "/image"

    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)

    collection_generator(site_name, arg_item_set_id)

    metadata_dir = site_dir + "/metadata"

    if not os.path.isdir(metadata_dir):
        os.mkdir(metadata_dir)

    ld_generator(site_name, arg_item_set_id)
    excel_generator(site_name, arg_item_set_id)


if __name__ == "__main__":
    args = parse_args()

    site_name = args.site_name
    arg_item_set_id = args.item_set_id

    single_collection_batch(site_name, arg_item_set_id)