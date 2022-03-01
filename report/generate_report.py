import asyncio
from pyppeteer import launch
import os
import numpy as np
from base64 import b64encode
from tqdm import tqdm
import pandas as pd
from string import Template
from datetime import datetime
from api.image10k import get_data, get_path_image10k

# Manually set the number of reports to generate
# Use 0 to generate all possible reports
n_report = -1


def _generate_screenshot(url, image):
    try:
        async def main():
            browser = await launch()
            page = await browser.newPage()
            await page.goto(url)
            await page.screenshot({"path": image}, type='jpeg')
            await browser.close()

        asyncio.get_event_loop().run_until_complete(main())
        status = 'success'
    except:
        status = 'crash'
    return status


def _unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def _get_category(df, n_report=-1):
    list_category = _unique(df["tag"])
    list_category = [category.replace(", ", "-") for category in list_category]
    if n_report > 0:
        list_category = list_category[0 : np.min([n_report, len(list_category)])]
    return list_category


def _bytesIO_to_base64(handle_io):
    """Encode the content of a bytesIO virtual file as base64.
    Also closes the file.
    Returns: data
    """
    handle_io.seek(0)
    data = b64encode(handle_io.read()).decode("utf-8")
    handle_io.close()
    return data


def _get_html_template(template_file):
    """Get an HTML file from package data"""
    with open(template_file, "rb") as f:
        return Template(f.read().decode("utf-8"))


# Set up path and load dataset
path_image10k = get_path_image10k()
path_report = os.path.join(os.path.split(path_image10k)[0], "image10k_report")
path_template = os.path.join(os.path.split(path_image10k)[0], "report")
df = pd.read_csv(os.path.join(path_image10k, "image10k.tsv"), sep="\t")

# Identify unique categories
list_category = _get_category(df, n_report)

# loop over reports
for category in tqdm(list_category):
    df_category = df[[label == category.replace("-", ", ") for label in df["tag"]]]

    # Build div element containing the images
    template_image = _get_html_template(
        os.path.join(path_template, "template_image.html")
    )
    report_image = []
    for row in df_category.itertuples():
        if getattr(row, "source_url") != "none":

            # Convert image file in base64
            file_name = os.path.join(
                path_image10k, getattr(row, "tag").replace(', ', os.sep), getattr(row, "name")
            )
            with open(file_name, 'rb') as f: img_base64 = _bytesIO_to_base64(f)

            # Screenshot website and convert in base64
            file_tmp = os.path.join(path_report, 'image_tmp.bin')
            status = _generate_screenshot(getattr(row, "source_url"), file_tmp)
            #with open(file_tmp, 'wb') as f:
            #    _generate_screenshot(getattr(row, "source_url"), f)
            if status == 'success':
                with open(file_tmp, 'rb') as f: img_screenshot = _bytesIO_to_base64(f)
            else:
                img_screenshot='crash'

            # Update template
            report_image.append(
                template_image.safe_substitute(
                    LABEL=getattr(row, "name"),
                    AUTHOR=getattr(row, "author"),
                    URL=getattr(row, "source_url"),
                    IMAGE=img_base64,
                    SCREENSHOT=img_screenshot
                )
            )

    # Assemble the complete report with html header
    report = _get_html_template(os.path.join(path_template, "template_report.html"))
    with open(os.path.join(path_report, f"report_{category}.html"), "w") as f:
        f.write(
            report.safe_substitute(
                TITLE=category, DATE=datetime.now(), IMAGES="\n".join(report_image)
            )
        )
