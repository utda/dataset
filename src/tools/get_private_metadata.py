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

    parser.add_argument(
        'key_identity',
        action='store',
        type=str,
        help='key identity.')

    parser.add_argument(
        'key_credential',
        action='store',
        type=str,
        help='key credential.')

    return parser.parse_args(args)


def get_thumbnail(media_iri):
    try:
        response = urllib.request.urlopen(media_iri+"?key_identity=uPGzhgfaXakUSiqSNlTWIW2i3Aw4En3i&key_credential=RdL0RPbekHHOXC6BF86zofHyfOK1CQg2")
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body)

        return data["o:thumbnail_urls"]["medium"]
    except:
        return ""


def main(output_path, item_set, key_identity, key_credential):
    flg = True
    page = 1

    fo = open(output_path, 'w')
    writer = csv.writer(fo, lineterminator='\n')
    writer.writerow(
        ["bibo:identifier", "OmekaID", "uterms:manifestUri", "rdfs:seeAlso", "foaf:thumbnail"])

    while flg:
        url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api/items?item_set_id=" + item_set + "&page=" + str(page)+"&key_identity="+key_identity+"&key_credential="+key_credential
        print(url)

        page += 1

        response = urllib.request.urlopen(url)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]

                id = ""
                if "bibo:identifier" in obj:
                    id = obj["bibo:identifier"][0]["@value"]

                omeka_id = obj["o:id"]

                see_also = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api/items/" + str(omeka_id)

                manifest_uri = ""
                thumbnail_url = ""

                tmp_id = (str(omeka_id) if id == "" else str(id))

                if len(obj["o:media"]) > 0:
                    manifest_uri = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/" + str(tmp_id) + "/manifest"
                    thumbnail_url = get_thumbnail(obj["o:media"][0]["@id"])

                writer.writerow([id, omeka_id, manifest_uri, see_also, thumbnail_url])

        else:
            flg = False

    fo.close()

    print("output_path:\t" + output_path)


if __name__ == "__main__":
    args = parse_args()

    main(args.output_path, args.item_set, args.key_identity, args.key_credential)
