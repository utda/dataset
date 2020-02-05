import sys
import urllib
import json
import argparse
import urllib.request
import os
import shutil

dir = "data/media"
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir, exist_ok=True)

def base_generator():
    api_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api"

    loop_flg = True
    page = 1

    while loop_flg:
        url = api_url + "/media?page=" + str(
            page)
        print(url)

        page += 1

        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]

                oid = str(obj["o:id"])

                with open(dir+"/"+oid+".json", 'w') as outfile:
                    json.dump(obj, outfile, ensure_ascii=False,
                              indent=4, sort_keys=True, separators=(',', ': '))

                '''

                medias = obj["o:media"]

                for media in medias:
                    request = urllib.request.Request(media["@id"])
                    response = urllib.request.urlopen(request)

                    response_body = response.read().decode("utf-8")
                    media_obj = json.loads(response_body.split('\n')[0])

                    mid = str(media_obj["o:id"])

                    with open("data/media/"+mid+".json", 'w') as outfile:
                        json.dump(media_obj, outfile, ensure_ascii=False,
                                  indent=4, sort_keys=True, separators=(',', ': '))

                '''

        else:
            loop_flg = False


if __name__ == "__main__":

    base_generator()
