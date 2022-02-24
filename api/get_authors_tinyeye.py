import pandas as pd
import argparse
from tqdm import tqdm
from pytineye import TinEyeAPIRequest
from image10k import get_data

def _get_human_face():
    df = get_data()
    human = df[df['tag'].str.contains('human')]
    face = df[df['tag'].str.contains('face')]
    return pd.merge(human, face)


def _get_index(df, num):
    index = df.index
    if num > 0:
        index = index[:num]
    return index

def _api_tineye(api_key):
    return TinEyeAPIRequest(
        api_url='https://api.tineye.com/rest/',
        api_key=api_key
    )


def _parse_response(response):
    links = ""
    flickr = ""
    try:
        for match in response.matches:
            for backlink in match.backlinks:
                links = f"{backlink.url}, {backlink.backlink}; {links}"
                if "static.flickr" in backlink.url:
                    flickr = backlink.url.split("/")[-1]
    except:
        links = "Error"
    return links, flickr



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Use the tineye API to locate source of images."
    )
    parser.add_argument("key", type=str, nargs="+", help="the tineye API key")
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

    df = pd.DataFrame(columns=['file', 'backlink', 'flicker_id'])
    human_face = _get_human_face()
    index = _get_index(human_face, args.num)
    api = _api_tineye(args.key[0])
    for row in tqdm(index):
        file = human_face.loc[row, 'file']
        with open(file, 'rb') as f: data = f.read()
        response = api.search_data(data=data)
        df.loc[row, 'file'] = file
        df.loc[row, 'backlink'], df.loc[row, 'flicker_id'] = _parse_response(response)

    df.to_excel(args.output[0])
