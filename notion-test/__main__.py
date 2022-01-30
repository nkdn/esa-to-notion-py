from notion.client import NotionClient
import settings

def main():
	client = NotionClient(token_v2=settings.TOKEN_V2)
	page = client.get_block("https://www.notion.so/ce02ea0e970f4120b89efd39e5a354e2")
	print(page.title)

main()
