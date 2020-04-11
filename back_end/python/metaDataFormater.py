


def format_meta(metaKey):
    for char in metaKey:
        if char.isalpha() or char.isdigit() or char == '_':
            continue
        else:
            metaKey = metaKey.replace(char, "_")
    return metaKey

