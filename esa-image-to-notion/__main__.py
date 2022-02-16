from notion.block import (
    ImageBlock
)
from notion.client import NotionClient
import settings
import sys
import wrapper

def main():
    args = sys.argv
    page_id = args[1]

    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    page = client.get_block(page_id)
    children = page.children
    print(children)

    for block in children:
        if type(block) == ImageBlock:
            url = block.source

            if url.startswith("https://img.esa.io") or url.startswith("https://i.gyazo.com"):
                wrapper.upload_image_by_url(image_block=block, url=url)

main()
