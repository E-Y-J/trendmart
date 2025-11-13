import re
_slug_re = re.compile(r'[^a-z0-9]+')


def slugify(text: str) -> str:
    if not text:
        return ''
    slug = text.strip().lower()
    slug = _slug_re.sub('-', slug).strip('-')
    return slug[:100]
