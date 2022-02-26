import pandas as pd
import argparse
import os
import re
from itertools import compress
from tqdm import tqdm


def _get_index(df, num):
    index = df.index
    if num > 0:
        index = index[:num]
    return index


def _get_name(file):
    head, tail = os.path.split(file)
    return tail

def _parse_backlink(backlink, keyword):
    list_url = backlink.split('; ')
    mask = [keyword in url for url in list_url]
    url = list(compress(list_url, mask))[0]
    file, source_url = url.split(', ')
    head, image_id = os.path.split(file)
    return source_url, image_id


def _get_source(backlink):
    image_id = 'none'
    source_url = 'none'
    if (not pd.isna(backlink)) and ('flickr' in backlink):
        source_url, image_id = _parse_backlink(backlink, 'flickr')
        if image_id == "":
            head, image_id = os.path.split(source_url)
    elif (not pd.isna(backlink)) and 'wikimedia.org' in backlink:
        source_url, image_id = _parse_backlink(backlink, 'wikimedia.org')
        image_id = image_id.split('px-')[-1]
        source_url = f'https://commons.wikimedia.org/wiki/File:{image_id}'
    elif (not pd.isna(backlink)) and 'unsplash.com/photos' in backlink:
        source_url, image_id = _parse_backlink(backlink, 'unsplash.com/photos')
        source_url = source_url.split('?')[0]
    elif (not pd.isna(backlink)) and 'pexels.com/photo' in backlink:
        source_url, image_id = _parse_backlink(backlink, 'pexels.com/photo')
        source_url = source_url.split('?')[0]
    elif (not pd.isna(backlink)) and 'pixabay.com/photo' in backlink:
        source_url, image_id = _parse_backlink(backlink, 'pixabay.com/photo')
        source_url = source_url.split('?')[0]
    return image_id, source_url

def _get_website(backlink, source):

    website = 'none'
    url = 'none'

    for num, keyword in enumerate(source['keyword']):
        if (not pd.isna(backlink)) and (keyword in backlink):
            website = source.loc[num, 'reference']
            url = source.loc[num, 'URL']

    return website, url

def _clean_dataframe(df_raw, source):
    df_clean = pd.DataFrame(
        columns=[
            "name",
            "website",
            "url",
            "online_image_id",
            "extension",
            "metadata",
            "include",
            "license_code",
            "license",
            "author",
            "source_url",
        ]
    )
    index = _get_index(df_raw, args.num)

    for row in tqdm(index):
        df_clean.loc[row, "name"] = _get_name(df_raw.loc[row, "file"])
        website, url = _get_website(df_raw.loc[row, 'backlink'], source)
        df_clean.loc[row, "website"] = website
        df_clean.loc[row, "url"] = url
        image_id, source_url = _get_source(df_raw.loc[row, 'backlink'])
        df_clean.loc[row, "online_image_id"] = image_id
        df_clean.loc[row, "source_url"] = source_url

    return df_clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean up sources for pictures retrieved by tineye."
    )
    parser.add_argument(
        "input", type=str, nargs="+", help="the xls file name to clean up"
    )
    parser.add_argument(
        "source", type=str, nargs="+", help="a csv file describing web sources"
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
    source = pd.read_csv(args.source[0])
    df_raw = pd.read_excel(args.input[0])
    df_clean = _clean_dataframe(df_raw, source)
    df_clean.to_excel(args.output[0])
