def normalize_text(text_list: list[str], exclude_texts=None):
    exclude_texts = exclude_texts or []
    stripped_list = []
    for text in text_list:
        stripped = text.strip()
        if stripped and stripped not in exclude_texts:
            stripped_list.append(stripped)

    return "\n".join(stripped_list)
