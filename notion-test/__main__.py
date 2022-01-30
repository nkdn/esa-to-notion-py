from notion.block import (
    HeaderBlock,
    TextBlock,
    ImageBlock
)
from notion.client import NotionClient
import requests
import settings

def main():
    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    page = client.get_block("e2c3a61fb10a46f693db49b2b23f017a")
    print(page)

    page.children.add_new(HeaderBlock, title="はじめに")
    text = "まず、`.env` ファイルをコピーしてください。\nそれが**とても大事** :exclamation: です。"
    page.children.add_new(TextBlock, title=text)
    image = page.children.add_new(ImageBlock)
    image.upload_file_bin(requests.get("https://upload.wikimedia.org/wikipedia/commons/e/ef/StarfieldSimulation004.gif").content, "sample.gif", "image/gif")
    print(image.source)

main()
