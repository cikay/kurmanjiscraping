def normalize_text(
    text_list: list[str], title: str, exclude_texts=None
) -> tuple[str, str]:
    exclude_texts = exclude_texts or []
    stripped_list = []
    for text in text_list:
        stripped = text.strip()
        if stripped and stripped not in exclude_texts:
            stripped_list.append(stripped)

    title = title.strip()
    content = "\n".join(stripped_list)
    if content.startswith(title):
        return title, content

    return title, f"{title}\n\n{content}"
