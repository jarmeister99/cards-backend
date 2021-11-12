import requests
import bs4
import math


def get_images(
    url: str,
    desired_aspect_ratio: float,
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
        return closest_tag.get("src")
    else:
        return None


if __name__ == "__main__":
    foo = get_images(
        "https://www.loveandlemons.com/baked-potato/",
        desired_aspect_ratio=16 / 9,
        min_width=100,
    )
    bar = get_images(
        "https://en.wikipedia.org/wiki/Foobar",
        desired_aspect_ratio=16 / 9,
        min_width=100,
    )
    print(foo)
    print(bar)
