from notion.block import (
    BasicBlock,
    PageBlock
)
from notion.client import NotionClient
import re
import settings
import sys

def main():
    args = sys.argv
    parent_page_id = args[1]

    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    parent_page = client.get_block(parent_page_id)
    children = parent_page.children

    last_block = children[-1]

    new_block = children.add_new(PageBlock, title="test")
    last_block.move_to(new_block)
    return

    child_pages = []

    for block in parent_page.children:
        if type(block) == PageBlock:
            child_pages.append({"id": block.id, "title": block.title})

    print(child_pages, flush=True)
    return

    for child_page in child_pages:
        page_id = child_page["id"]
        page_id = page_id.replace("-", "")
        page = client.get_block(page_id)
        print("%s (%s)" % (page.title, page_id))

        for block in page.children:
            change_url_recursively(block, esa_notion_mapping)

main()
