from io import BytesIO
import os
from PIL import Image
import requests
from urllib.parse import urlparse

def main():
    url = "https://upload.wikimedia.org/wikipedia/commons/e/ef/StarfieldSimulation004.gif"
    image = Image.open(BytesIO(requests.get(url).content))
    print(type(image))
    print(Image.MIME)

    filename = os.path.basename(urlparse(url).path)
    print(filename)
    mimetype = Image.MIME[image.format]
    print(mimetype)

    return filename, mimetype

main()
