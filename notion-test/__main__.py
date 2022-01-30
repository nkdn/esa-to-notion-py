import emoji
from notion.block import (
    HeaderBlock,
    TextBlock,
    ImageBlock
)
from notion.client import NotionClient
import requests
import settings
import wrapper

def main():
    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    page = client.get_block("34793858ce6c4c60aab34b3f0f4691e6")
    children = page.children
    print(children)

    for block in children:
        if type(block) == ImageBlock:
            url = block.source

            if url.startswith("https://img.esa.io"):
                image_block = children.add_new(ImageBlock) # TODO: これだと最下部への追加になってしまう。block のすぐ下に block を作れるよう考える
                wrapper.upload_image_by_url(image_block=image_block, url=url)

    # page.children.add_new(HeaderBlock, title="はじめに")
    # text = emoji.emojize("まず、`.env` ファイルをコピーしてください。\nそれが**とても大事** :exclamation: です。", use_aliases=True)
    # page.children.add_new(TextBlock, title=text)
    # image = page.children.add_new(ImageBlock)
    # image.upload_file_bin(requests.get("https://upload.wikimedia.org/wikipedia/commons/e/ef/StarfieldSimulation004.gif").content, "sample.gif", "image/gif")
    # print(image.source)

main()
