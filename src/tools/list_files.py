import os
import argparse
import sys
import csv


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'path_to_dir',
        action='store',
        type=str,
        help='Full path to dir.')

    parser.add_argument(
        'path_to_output_file',
        action='store',
        type=str,
        help='Full path to output file.')

    return parser.parse_args(args)


def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def main(path_to_dir, path_to_oFile):
    f = open(path_to_oFile, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["path"])

    for file in find_all_files(path_to_dir):
        writer.writerow([file])

    f.close()


if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_dir, args.path_to_oFile)
