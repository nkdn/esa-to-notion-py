import ast
from notion.block import (
    BasicBlock,
    PageBlock
)
from notion.client import NotionClient
import re
import settings
import sys

ESA_POST_PATTERN = r'https://[^\.]+\.esa\.io/posts/(\d+)'

def main():
    with open("mapping.txt") as f:
        lines = f.readlines()
    esa_notion_mapping = dict()

    for line in lines:
        dict_str = line.strip()
        if len(dict_str) == 0: continue
        mapping = ast.literal_eval(dict_str)
        esa_notion_mapping.update(mapping)
    print("mapping の組み合わせ数: %d" % len(esa_notion_mapping.keys()), flush=True)

    args = sys.argv
    parent_page_id = args[1]

    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    parent_page = client.get_block(parent_page_id)
    print(parent_page.children, flush=True)

    for block in parent_page.children:
        change_url_recursively(block, esa_notion_mapping)

    # child_page_ids = []

    # for block in parent_page.children:
    #     if type(block) == PageBlock:
    #         child_page_ids.append(block.id)

    # print("処理する件数: %d" % len(child_page_ids), flush=True)

    # for page_id in child_page_ids:
    #     page_id = page_id.replace("-", "")
    #     page = client.get_block(page_id)
    #     print("%s (%s)" % (page.title, page_id))

    #     children = page.children
    #     esa_id = int(children[0].title.replace("ID: ", ""))

    #     for block in children:
    #         change_url_recursively(block, esa_notion_mapping)

# block 内にさらに block がある場合も再帰的に ImageBlock を探し、Notion 向けに画像アップロードをおこなう
def change_url_recursively(block, esa_notion_mapping):
    if len(block.children) == 0:
        if isinstance(block, BasicBlock):
            pattern = re.compile(ESA_POST_PATTERN)
            title = block.title

            if pattern.search(title):
                def replace_method(matched):
                    esa_id = int(matched.group(1))
                    notion_id = esa_notion_mapping[esa_id]
                    return "https://www.notion.so/%s" % notion_id

                print(title, flush=True)
                title = pattern.sub(replace_method, title)
                print(title, flush=True)
                block.title = title
    else:
        for child_block in block.children:
            change_url_recursively(child_block, esa_notion_mapping)

main()
