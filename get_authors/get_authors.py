import requests
import argparse
import json
import pandas as pd
from tqdm import tqdm

with open("licenses.json", "r") as f:
    licenses_json = json.load(f)
accept_license = [1, 2, 4, 5, 9, 10]


def _init_df(filename):
    df = pd.read_excel(filename)
    df.insert(len(df.columns), "metadata", "None")
    df.insert(len(df.columns), "include", False)
    df.insert(len(df.columns), "license_code", "None")
    df.insert(len(df.columns), "license", "None")
    df.insert(len(df.columns), "author", "None")
    df.insert(len(df.columns), "source_url", "None")
    return df


def _get_id(df, row):
    id = df["online_image_id"][row].split("_")[0]
    return id


def _get_index(df, num):
    index = df.loc[df["url"] == "https://www.flickr.com/photos"].index
    if num > 0:
        index = index[:num]
    return index


def _rest_query(key, secret, id):
    api_url = f"https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key={key}&photo_id={id}&secret={secret}&format=json&nojsoncallback=1"
    response = requests.get(api_url)
    return response.json()


def _get_author(metadata):
    username = metadata["photo"]["owner"]["username"]
    realname = metadata["photo"]["owner"]["realname"]
    return f"{realname} (flickr {username})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Use the flickr API to add authors and license information."
    )
    parser.add_argument("key", type=str, nargs="+", help="the flickr API key")
    parser.add_argument("secret", type=str, nargs="+", help="the flickr API secret")
    parser.add_argument(
        "filename", type=str, nargs="+", help="the xls file name to be processed"
    )
    parser.add_argument(
        "output", type=str, nargs="+", help="the xls file name to save results"
    )
    parser.add_argument(
        "-n",
        "--num",
        metavar="num",
        type=int,
        default=-1,
        help="number of images to process",
    )

    args = parser.parse_args()

    df = _init_df(args.filename[0])
    index = _get_index(df, args.num)
    for row in tqdm(index):
        id = _get_id(df, row)
        metadata = _rest_query(args.key[0], args.secret[0], id)
        try:
            df.loc[row, "metadata"] = str(metadata)
            df.loc[row, "license_code"] = int(metadata["photo"]["license"])
            if df.loc[row, "license_code"] in accept_license:
                df.loc[row, "include"] = True
            df.loc[row, "license"] = licenses_json[metadata["photo"]["license"]]
            df.loc[row, "author"] = _get_author(metadata)
            df.loc[row, "source_url"] = metadata["photo"]["urls"]["url"][0]["_content"]
        except:
            print(f"an error occured in row {row}")
    df.to_excel(args.output[0])
