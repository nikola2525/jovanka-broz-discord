import unicodedata
import re


def slugify(value):
    """
    Convert spaces to hyphens. Remove characters that aren't 
    alphanumerics, underscores, or hyphens. Convert to lowercase.
    Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)
