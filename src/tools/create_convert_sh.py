import os
import argparse
import sys


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'input_dir',
        action='store',
        type=str,
        help='Ful path to input dir.')

    parser.add_argument(
        'output_dir',
        action='store',
        type=str,
        help='Ful path to output dir.')

    parser.add_argument(
        'output_sh_file',
        action='store',
        type=str,
        help='Ful path to output sh file.')

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    output_path = args.output_sh_file

    files = os.listdir(input_dir)

    f = open(output_path, 'w')

    for root, dirs, files in os.walk(input_dir):
        for name in files:
            org_file_path = os.path.abspath(root) + "/" + name
            new_file_path = org_file_path.replace(input_dir, output_dir).split(".")[0] + ".tif"

            new_output_dir = os.path.abspath(root).replace(input_dir, output_dir)

            f.write("sudo mkdir -p " + new_output_dir + "\n")
            f.write(
                "sudo convert '" + org_file_path + "' -define tiff:tile-geometry=256x256 -compress jpeg 'ptif:" + new_file_path + "'\n")

    f.close()
