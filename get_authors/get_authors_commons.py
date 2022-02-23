import requests
import argparse
import json
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

def _init_df(filename):
    df = pd.read_excel(filename)
    return df


def _get_id(df, row):
    id = df["online_image_id"][row] + df["extension"][row]
    return id


def _get_index(df, num):
    index = df.loc[df["url"] == "https://commons.wikimedia.org"].index
    if num > 0:
        index = index[:num]
    return index


def _rest_query(id):
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=Image:{id}&prop=imageinfo&iiprop=extmetadata&format=json"
    response = requests.get(api_url)
    return response.json()


def _get_license(data):
    key = list(data["query"]["pages"].keys())[0]
    try:
        license_url = data["query"]["pages"][key]["imageinfo"][0]["extmetadata"]["LicenseUrl"]["value"]
    except:
        license_url = ""
    license_name = data["query"]["pages"][key]["imageinfo"][0]["extmetadata"]["LicenseShortName"]["value"]
    return f"{license_name} {license_url}"


def _get_license_code(license, all_license):
    # Check if we already encountered this license
    if license in all_license.values():
        # The license was already seen, just return its code
        index = list(all_license.values()).index(license)
        license_code  = list(all_license.keys())[index]
    else:
        # The license was never seen, create a new code and add it to the
        # dictionary of licenses
        n_license = len(list(all_license.keys()))
        license_code = f"C{n_license}"
        all_license[license_code] = license
    return license_code


def _get_author(data):
    key = list(data["query"]["pages"].keys())[0]
    author_html = data["query"]["pages"][key]["imageinfo"][0]["extmetadata"]["Artist"]["value"]
    soup = BeautifulSoup(author_html, 'html.parser')
    try:
        author_url = f" ({soup.a.get('href')})"
        author_url = author_url.replace('//commons.wikimedia.org', 'https://commons.wikimedia.org')
    except:
        author_url = ""
    author_name = soup.a.get_text()
    return f"{author_name}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Use the wikimedia commons API to add authors and license information."
    )
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
    all_license = {}
    for row in tqdm(index):
        id = _get_id(df, row)
        metadata = _rest_query(id)
        try:
            df.loc[row, "metadata"] = str(metadata)
            df.loc[row, "include"] = True
            df.loc[row, "license"] = _get_license(metadata)
            df.loc[row, "license_code"] = _get_license_code(df.loc[row, "license"], all_license)
            df.loc[row, "author"] = _get_author(metadata)

        except:
            df.loc[row, "include"] = False
            print(f"an error occured in row {row}")
    with open('license_commons.json', 'w') as f: json.dump(all_license, f, indent=3)
    df.to_excel(args.output[0])
