from notion.block import (
    PageBlock
)
from notion.client import NotionClient
import settings
import sys

MAX_LAYER = 3

def main():
    args = sys.argv
    parent_page_id = args[1]

    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    parent_page = client.get_block(parent_page_id)
    add_root_and_move(parent_page)
    print("Successfully completed!!", flush=True)

def add_root_and_move(parent_page, layer=1):
    children = parent_page.children
    root_blocks = []

    for block in children:
        if type(block) != PageBlock: continue

        page_title = block.title
        splitted_title = page_title.split("::")
        if len(splitted_title) == 1: continue
        root_title = splitted_title[0]

        # 最終階層はスラッシュ区切りにするか迷う……
        new_page_title = "::".join(splitted_title[1:])
        # if layer <= MAX_LAYER:
        #     new_page_title = "::".join(splitted_title[1:])
        # else:
        #     new_page_title = "/".join(splitted_title[1:])

        same_title_blocks = list(
            filter(lambda root_block: root_block.title == root_title, root_blocks))
        if len(same_title_blocks):
            exists_root_block = same_title_blocks[0]
            block.move_to(exists_root_block)
            block.title = new_page_title
        else:
            root_block = children.add_new(PageBlock, title=root_title)
            root_blocks.append(root_block)
            print("=== Added '%s' page ===" % root_title, flush=True)
            block.move_to(root_block)
            block.title = new_page_title
        print(new_page_title, flush=True)

    if layer <= MAX_LAYER:
        for root_block in root_blocks:
            add_root_and_move(root_block, layer=layer + 1)

main()
