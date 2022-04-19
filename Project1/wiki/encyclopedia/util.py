import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def full_list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def list_entries():
    """
    Returns a list of all names of encyclopedia entries. Without the ERROR entry
    """
    entry_list = full_list_entries()
    entry_list.remove("ERROR")
    return entry_list


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    print("ADENTRO SAVE_ENTRY")
    filename = f"entries/{title}.md"
    print("filename = ", filename)
    print("default_storage.exists(filename) = ", default_storage.exists(filename))
    if default_storage.exists(filename):
        default_storage.delete(filename)
    print("ANTES LINEA FINAL")
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
