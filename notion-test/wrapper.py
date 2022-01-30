from io import BytesIO
import os
from PIL import Image
import requests
from urllib.parse import urlparse

def upload_image_by_url(image_block, url):
    image_bytes = requests.get(url).content
    image = Image.open(BytesIO(image_bytes))
    filename = os.path.basename(urlparse(url).path)
    mimetype = Image.MIME[image.format]

    image_block.upload_file_bin(image_bytes, filename, mimetype)
