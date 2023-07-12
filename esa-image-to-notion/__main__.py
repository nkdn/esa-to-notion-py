from notion.block import (
    ImageBlock,
    PageBlock
)
from notion.client import NotionClient
import settings
import sys
import wrapper
import traceback

def main():
    args = sys.argv
    parent_page_id = args[1]

    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    parent_page = client.get_block(parent_page_id)
    child_page_ids = []

    for block in parent_page.children:
        if type(block) == PageBlock:
            child_page_ids.append(block.id)

    print("処理する記事数: %d" % len(child_page_ids), flush=True)
    esa_notion_mapping = dict()

    for page_id in child_page_ids:
        page_id = page_id.replace("-", "")
        page = client.get_block(page_id)
        print("%s (%s)" % (page.title, page_id), flush=True)

        children = page.children
        esa_id = int(children[0].title.replace("ID: ", ""))
        esa_notion_mapping[esa_id] = page_id

        for block in children:
            for retry_count in range(30): # 通信エラーで死ににくいようにリトライ処理
                try:
                    reupload_image_recursively(block)
                except Exception as e:
                    print(e, flush=True)
                    print(traceback.format_exc())
                else:
                    break

    print(esa_notion_mapping, flush=True)
    print("処理数: %d" % len(esa_notion_mapping.keys()), flush=True)
    print("Successfully completed!!", flush=True)

# block 内にさらに block がある場合も再帰的に ImageBlock を探し、Notion 向けに画像アップロードをおこなう
def reupload_image_recursively(block):
    if len(block.children) == 0:
        if type(block) == ImageBlock:
            url = block.source

            if url.startswith("https://img.esa.io") or url.startswith("https://i.gyazo.com"):
                if url.endswith(".svg"): return # SVG ファイルは PIL.UnidentifiedImageError が起こるのでスルー
                print("Re-uploading %s ..." % url, flush=True)
                wrapper.upload_image_by_url(image_block=block, url=url)
    else:
        for child_block in block.children:
            reupload_image_recursively(child_block)

main()
