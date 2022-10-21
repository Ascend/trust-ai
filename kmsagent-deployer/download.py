import os.path
import json
from urllib import request
from urllib.error import ContentTooShortError, URLError


def download_files(url_dict, retry_time=3):
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
                f = request.urlopen(url)
                with open(total_path, "wb") as download:
                    download.write(f.read())
                    print("download %s successfully" % file_name)
                    download.close()
            return
        except ContentTooShortError as cte:
            print(cte)
        except URLError as err:
            print(err)
        except ConnectionResetError:
            print("connection reset by peer, retry...")
        finally:
            pass


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
    # check whether resources file exits
    check_dir("resources")

    # load json file
    json_path = "download_url.json"
    dict_json = read_json(json_path)

    # download files
    for k in dict_json.keys():
        val = dict_json.get(k)
        dict_input = {k: val}
        download_files(dict_input)