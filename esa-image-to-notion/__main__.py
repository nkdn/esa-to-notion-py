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
        reupload_image_recursively(block)

# block 内にさらに block がある場合も再帰的に ImageBlock を探し、画像の Notion 用のアップロードをおこなう
def reupload_image_recursively(block):
    if len(block.children) == 0:
        if type(block) == ImageBlock:
            url = block.source

            if url.startswith("https://img.esa.io") or url.startswith("https://i.gyazo.com"):
                wrapper.upload_image_by_url(image_block=block, url=url)
    else:
        for child_block in block.children:
            reupload_image_recursively(child_block)

main()
