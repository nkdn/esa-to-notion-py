from notion.block import (
    ImageBlock
)
from notion.client import NotionClient
import settings
import wrapper

def main():
    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    page = client.get_block("05463d2c8f4b49078b9070f37643089f")
    children = page.children
    print(children)

    for block in children:
        if type(block) == ImageBlock:
            url = block.source

            if url.startswith("https://img.esa.io"):
                wrapper.upload_image_by_url(image_block=block, url=url)

main()
