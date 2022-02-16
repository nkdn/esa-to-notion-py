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
    child_page_ids = client.search_pages_with_parent(page_id)
    esa_notion_mapping = dict()

    for page_id in child_page_ids:
        page_id = page_id.replace("-", "")
        page = client.get_block(page_id)
        print("%s (%s)" % (page.title, page_id))

        children = page.children
        esa_id = int(children[0].title.replace("ID: ", ""))
        esa_notion_mapping[esa_id] = page_id

        for block in children:
            reupload_image_recursively(block)

    print(esa_notion_mapping)

# block 内にさらに block がある場合も再帰的に ImageBlock を探し、Notion 向けに画像アップロードをおこなう
def reupload_image_recursively(block):
    if len(block.children) == 0:
        if type(block) == ImageBlock:
            url = block.source

            if url.startswith("https://img.esa.io") or url.startswith("https://i.gyazo.com"):
                print("Re-uploading %s ..." % url)
                wrapper.upload_image_by_url(image_block=block, url=url)
    else:
        for child_block in block.children:
            reupload_image_recursively(child_block)

main()
