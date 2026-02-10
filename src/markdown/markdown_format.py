import re

def rich(text: str):
    parts = []
    pattern = re.compile(r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[.+?\]\(.+?\))")
    for chunk in pattern.split(text):
        if not chunk:
            continue

        if chunk.startswith("**"):
            parts.append(
                {
                    "type": "text",
                    "text": {"content": chunk[2:-2]},
                    "annotations": {"bold": True},
                }
            )
        elif chunk.startswith("*"):
            parts.append(
                {
                    "type": "text",
                    "text": {"content": chunk[1:-1]},
                    "annotations": {"italic": True},
                }
            )
        elif chunk.startswith("`"):
            parts.append(
                {
                    "type": "text",
                    "text": {"content": chunk[1:-1]},
                    "annotations": {"code": True},
                }
            )
        elif chunk.startswith("["):
            label, url = re.match(r"\[(.+?)\]\((.+?)\)", chunk).groups()
            parts.append(
                {"type": "text", "text": {"content": label, "link": {"url": url}}}
            )
        else:
            parts.append({"type": "text", "text": {"content": chunk}})

    return parts


def H(level, text):
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {"rich_text": rich(text)},
    }


def P(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich(text)},
    }


def B(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich(text)},
    }


def N(text):
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": rich(text)},
    }


def Q(text):
    return {"object": "block", "type": "quote", "quote": {"rich_text": rich(text)}}


def D():
    return {"object": "block", "type": "divider", "divider": {}}


def C(code, language="plain text"):
    return {
        "object": "block",
        "type": "code",
        "code": {
            "language": language,
            "rich_text": [{"type": "text", "text": {"content": code}}],
        },
    }


def table_block(headers, rows):
    # Build Notion table block
    table_rows = [{
        "type": "table_row",
        "table_row": {
            "cells": [[{"type": "text", "text": {"content": h}}] for h in headers]
        },
    }]

    # Header row

    # Data rows
    for row in rows:
        table_rows.append(
            {
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"type": "text", "text": {"content": cell}}] for cell in row
                    ]
                },
            }
        )

    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": len(headers),
            "has_column_header": True,
            "has_row_header": False,
            "children": table_rows,
        },
    }


def markdown_to_blocks(md: str):
    blocks = []
    lines = md.splitlines()

    in_code = False
    code_buffer = []
    code_language = ""

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        # Code fences
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_language = line[3:].strip()
                code_buffer = []
            else:
                blocks.append(C("\n".join(code_buffer), code_language))
                in_code = False
            i += 1
            continue

        if in_code:
            code_buffer.append(line)
            i += 1
            continue

        line = line.strip()
        if not line:
            i += 1
            continue

        # -------- TABLE DETECTION --------
        # Header | A | B |
        if (
            line.startswith("|")
            and i + 1 < len(lines)
            and lines[i + 1].strip().startswith("|-")
        ):
            header_line = line
            sep_line = lines[i + 1]

            headers = [h.strip() for h in header_line.strip("|").split("|")]
            rows = []

            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip("|").split("|")]
                rows.append(row)
                i += 1

            blocks.append(table_block(headers, rows))
            continue
        # -------- END TABLE --------

        if line == "---":
            blocks.append(D())
        elif line.startswith("> "):
            blocks.append(Q(line[2:]))
        elif re.match(r"\d+\.\s+", line):
            blocks.append(N(re.sub(r"^\d+\.\s+", "", line)))
        elif line.startswith("- "):
            blocks.append(B(line[2:]))
        elif line.startswith("### "):
            blocks.append(H(3, line[4:]))
        elif line.startswith("## "):
            blocks.append(H(2, line[3:]))
        elif line.startswith("# "):
            blocks.append(H(1, line[2:]))
        else:
            blocks.append(P(line))

        i += 1

    return blocks
