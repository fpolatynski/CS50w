import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from typing import List


def search_entries(query: str) -> List[str]:
    all_entries = list_entries()
    ans = []
    for x in all_entries:
        temp = re.findall(query, x)
        if len(temp) > 0:
            ans.append(x)
    return ans


# Save markdown text to .md file
def save_entries(entries_text: str, title: str) -> None:
    with open("entries/"+title + ".md", "w") as entries:
        entries.write(entries_text)


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
