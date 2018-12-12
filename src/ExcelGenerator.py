import sys
import urllib
import json
import argparse
import urllib.request
import unicodedata
import pandas as pd


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


def excel_generator(site_name, arg_item_set_id):
    label_map = dict()
    label_map["bibo:identifier"] = "ID"
    label_map["dcterms:isPartOf"] = "ウェブサイトURL"
    label_map["dcterms:relation"] = "アイテムURL"
    label_map["dcterms:rights"] = "利用条件"
    label_map["dcterms:title"] = "タイトル"
    label_map["foaf:thumbnail"] = "サムネイル"
    label_map["rdfs:seeAlso"] = "機械可読ドキュメント"
    label_map["sc:attributionLabel"] = "帰属"
    label_map["sc:viewingDirection"] = "viewingDirection"
    label_map["uterms:databaseLabel"] = "コレクション"
    label_map["uterms:manifestUri"] = "IIIFマニフェストURI"
    label_map["uterms:sort"] = "ソート用項目"
    label_map["uterms:year"] = "年"

    table = []
    rows = []
    keySet = {}
    template_arr = []
    sorted_keys = []

    api_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api"

    output_path = "../docs/collections/" + site_name + "/metadata/data.xlsx"

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

                    if obj["o:resource_template"] != None:

                        template_id = obj["o:resource_template"]["@id"]
                        if template_id not in template_arr:
                            template_arr.append(template_id)

                    for key in obj:
                        if not key.startswith("o:") and key != "@type":
                            if key not in keySet and isinstance(obj[key], list):
                                if "property_label" in obj[key][0]:
                                    keySet[key] = obj[key][0]["property_label"]

                    rows.append(obj)

            else:
                loop_flg = False

    for template_id in template_arr:
        response = urllib.request.urlopen(template_id)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])
        property_arr = data["o:resource_template_property"]
        for property in property_arr:

            property_label = property["o:alternate_label"]

            property_id = property["o:property"]["@id"]

            response = urllib.request.urlopen(property_id)
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body.split('\n')[0])

            term = data["o:term"]

            sorted_keys.append(term)

            if property_label:
                label_map[term] = property_label

    for term in label_map:
        if term not in sorted_keys:
            sorted_keys.append(term)

    for term in sorted(keySet):
        if term not in sorted_keys:
            sorted_keys.append(term)

    row = []
    table.append(row)
    for term in sorted_keys:
        if term in label_map:
            row.append(label_map[term])
        else:
            row.append(term)

    # 二行目以降
    for obj in rows:
        row = []
        table.append(row)
        for term in sorted_keys:  # sorted(keySet):
            text = ""
            if term in obj:
                values = obj[term]
                for i in range(len(values)):
                    value = values[i]
                    if "@value" in value:
                        text += value["@value"]
                    else:
                        text += value["@id"]
                    if i != len(values) - 1:
                        text += "|"
            row.append(unicodedata.normalize("NFKC", text))

    df = pd.DataFrame(table);

    df.to_excel(output_path, index=False, header=False)
    df.to_csv(output_path.replace("xlsx", "csv"), index=False, header=False)
    df.to_csv(output_path.replace("xlsx", "tsv"), index=False, header=False, sep='\t')


if __name__ == "__main__":
    args = parse_args()

    site_name = args.site_name
    arg_item_set_id = args.item_set_id

    excel_generator(site_name, arg_item_set_id)
