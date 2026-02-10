import os
import webbrowser

from dotenv import load_dotenv
from notion_client import Client

from src.markdown.markdown_format import *

# -------- CONFIG --------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
# -----------------------

notion = Client(auth=NOTION_TOKEN)


def notion_page(markdown: str):
    blocks = markdown_to_blocks(markdown)

    # Create new Notion page
    page = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={"title": {"title": [{"text": {"content": "Notion Agent Notes"}}]}},
    )

    # Append blocks (Notion allows ~100 per call)
    for i in range(0, len(blocks), 50):
        notion.blocks.children.append(block_id=page["id"], children=blocks[i : i + 50])

    # Open page in browser
    page_id = page["id"].replace("-", "")
    webbrowser.open(f"https://www.notion.so/{page_id}")

    print("✅ Page created and opened!")
