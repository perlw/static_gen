import re

def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    blocks = re.split(r"\n\n", markdown)
    for b in blocks:
        stripped = b.strip()
        if stripped == "":
            continue
        result.append(stripped)
    return result
