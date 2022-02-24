import argparse
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a binary inclusion vector from a list of licenses."
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

    df = pd.read_excel(args.filename[0])
    index = df.index
    df.insert(len(df.columns), "include", "None")

    for row in tqdm(index):
        license = df.loc[row, "license_code"]
        df.loc[row, "include"] = (license != 0) and (license != "None")
    df.to_excel(args.output[0])
