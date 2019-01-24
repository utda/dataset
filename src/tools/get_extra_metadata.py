import sys
import csv
import urllib.request, json
import argparse


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'output_path',
        action='store',
        type=str,
        help='Ful path to output csv file.')

    parser.add_argument(
        'item_set',
        action='store',
        type=str,
        help='item set id.')

    return parser.parse_args(args)


def get_thumbnail(manifest_iri):
    try:
        response = urllib.request.urlopen(manifest_iri)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body)

        return data["sequences"][0]["canvases"][0]["thumbnail"]["@id"]
    except:
        return ""


def main(output_path, item_set):
    flg = True
    page = 1

    fo = open(output_path, 'w')
    writer = csv.writer(fo, lineterminator='\n')
    writer.writerow(
        ["bibo:identifier", "dcterms:title", "OmekaID", "uterms:manifestUri", "rdfs:seeAlso", "foaf:thumbnail"])

    while flg:
        url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api/items?item_set_id=" + item_set + "&page=" + str(page)
        print(url)

        page += 1

        response = urllib.request.urlopen(url)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]
                if "bibo:identifier" in obj or "dcterms:identifier" in obj:
                    id = ""
                    if "bibo:identifier" in obj:
                        id = obj["bibo:identifier"][0]["@value"]
                    omeka_id = obj["o:id"]

                    title = obj["dcterms:title"][0]["@value"]

                    manifest_uri = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/" + str(id) + "/manifest"
                    see_also = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api/items/" + str(omeka_id)
                    thumbnail_url = ""
                    if len(obj["o:media"]) > 0:
                        thumbnail_url = get_thumbnail(manifest_uri)
                    writer.writerow([id, title, omeka_id, manifest_uri, see_also, thumbnail_url])

        else:
            flg = False

    fo.close()

    print("output_path:\t" + output_path)


if __name__ == "__main__":
    args = parse_args()

    main(args.output_path, args.item_set)
