import time
from typing import Literal, Union, NamedTuple

import requests
import bs4
import math
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_screenshot(url: str):
    chrome_options = Options()  #
    chrome_service = Service("./chromedriver.exe")
    chrome_options.headless = True
    chrome_options.add_argument("--window-size=1920x1080")

    browser = webdriver.Chrome(options=chrome_options, service=chrome_service)
    browser.get(url)
    time.sleep(1)
    return browser.get_screenshot_as_base64()


def get_images(
    url: str,
    desired_aspect_ratio: float = 16 / 9,
    min_width: float = 0,
    max_width: float = math.inf,
    min_height: float = 0,
    max_height: float = math.inf,
):
    # get and parse html content
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    closest_tag, closest_ratio = None, None

    # for every img tag
    for tag in soup.find_all("img"):
        if tag.get("src"):
            # Ensure height and width are given
            if (height := tag.attrs.get("height")) and (
                width := tag.attrs.get("width")
            ):
                # Ensure height and width are in specified range
                if (
                    min_height <= float(height) <= max_height
                    and min_width <= float(width) <= max_width
                ):
                    # Check to see if this aspect ratio is the closest match seen thus far
                    ratio = float(width) / float(height)
                    if closest_ratio:
                        # Is the current aspect ratio closer to the target than the previous best match?
                        if abs(closest_ratio - desired_aspect_ratio) > abs(
                            ratio - desired_aspect_ratio
                        ):
                            # mark as new best match
                            closest_tag, closest_ratio = tag, ratio
                    # First valid tag found is best by default
                    else:
                        closest_tag, closest_ratio = tag, ratio

    if closest_tag:
        stripped_src = closest_tag.get("src").lstrip("/")
        return stripped_src
    else:
        return None


ImageResult = NamedTuple("ImageResult", type=str, img_url=str)


def get_image_or_screenshot(
    url: str,
    desired_aspect_ratio: float = 16 / 9,
    min_width: float = None,
    max_width: float = None,
    min_height: float = None,
    max_height: float = None,
) -> (Union[Literal["BASE64"], Literal["LINK"]], str):
    img_url = get_images(
        url=url,
        desired_aspect_ratio=desired_aspect_ratio,
        min_width=min_width,
        max_width=max_width,
        min_height=min_height,
        max_height=max_height,
    )
    if not img_url:
        return_type = "BASE64"
        img_url = get_screenshot(url=url)
    else:
        return_type = "LINK"
    return ImageResult(return_type, img_url)


if __name__ == "__main__":
    # foo = get_images(
    #     "https://www.loveandlemons.com/baked-potato/",
    #     desired_aspect_ratio=16 / 9,
    #     min_width=100,
    # )
    # bar = get_images(
    #     "https://en.wikipedia.org/wiki/Foobar",
    #     desired_aspect_ratio=16 / 9,
    #     min_width=100,
    # )
    # baz = get_images(
    #     "https://google.com",
    #     desired_aspect_ratio=16 / 9
    # )
    img_result = get_image_or_screenshot("https://adamschwartz.co/magic-of-css/")
    print(img_result)
