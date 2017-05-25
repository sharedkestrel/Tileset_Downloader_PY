from bs4 import BeautifulSoup
import requests
import os.path
import shutil


def request(url, streamtype):
    attempts = 0
    while attempts < 5:
        try:
            print("Connecting to %s..." % url)
            r = requests.get(url, timeout = 30, stream = streamtype)
            return r
        except ConnectionError:
            print("Connection failed, trying again...\n")
            attempts += 1
        except TimeoutError:
            print("Connection timed out, trying again...\n")
            attempts += 1
    print("The program could not receive data, check your internet connection.")
    raise ConnectionError


def parse(url):
    r = request(url, False)
    html = r.text
    s = BeautifulSoup(html, "html.parser")
    return s


def find_tilesets(soup):
    li = soup.find("li", id="post-256")
    images_tag = li.find_all("img")
    images = []
    for tag in images_tag:
        images.append(tag.get("src"))
        banana = tag.get("src")
    return images


def download_tileset(url):
    if "photobucket" in url:
        filename = url.rsplit("/", 1)[-1]
        r = request(url, True)
        r.raw.decode_content = True
        if not os.path.exists("images"):
            os.makedirs("images")
        with open(os.path.join('', 'images', filename), 'wb') as f:
            print("Downloading %s...\n" % filename)
            shutil.copyfileobj(r.raw, f)
        del r


html = parse("https://forums.rpgmakerweb.com/index.php?threads/steampunk-tiles.65/")
images_list = find_tilesets(html)
for image_link in images_list:
    download_tileset(image_link)
