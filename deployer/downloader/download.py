import os.path
import json
from urllib import request
from urllib.error import ContentTooShortError, URLError
import ssl
import sys


def download_files(url_dict, context, retry_time=3):
    """
    download files
    Args:
        urls to download files
    """
    path_name = list(url_dict)[0]
    url_list = url_dict.get(path_name)
    for i in range(retry_time):
        try:
            for url in url_list:
                check_dir(path_name)
                file_name = url.split("/")[-1]
                total_path = path_name + file_name
                print("start downloading %s ..." % file_name)
                f = request.urlopen(url, context=context)
                with open(total_path, "wb") as download:
                    download.write(f.read())
                    print("download %s successfully" % file_name)
            return True
        except ContentTooShortError as cte:
            print(cte)
        except URLError as err:
            print(err)
        except ConnectionResetError:
            print("connection reset by peer, retry...")
        finally:
            pass
        return False


def check_dir(filepath):
    """
    check if directory exits, if not, create one
    Args:
        file path
    """
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        return


def read_json(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    json_path = "%s/download_url.json" % cur_dir
    dict_json = read_json(json_path)
    context = ssl._create_unverified_context()

    # download files
    for k in dict_json.keys():
        val = dict_json.get(k)
        dict_input = {k: val}
        res = download_files(dict_input, context=context)
        if not res:
            sys.exit(1)
