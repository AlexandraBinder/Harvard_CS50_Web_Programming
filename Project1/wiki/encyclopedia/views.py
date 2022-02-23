from django.shortcuts import render
import markdown as md
import random

from . import util


def index(request):
    entries = util.list_entries()
    entries.remove("ERROR")
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def title(request, title):
    
    # If the entry does exist, the user should be presented 
    # with a page that displays the content of the entry. 
    # The title of the page should include the name of the entry.
    try: 
        return render(request, "encyclopedia/entry.html",{
            "entry": md.markdown(util.get_entry(title)),
            "title": title
        })

    # If an entry is requested that does not exist, 
    # the user should be presented with an error page 
    # indicating that their requested page was not found. 
    except:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.markdown(util.get_entry("ERROR"))
        })

def random_page(request):
    
    entries = util.list_entries()
    entries.remove("ERROR")
    selected_page = random.choice(entries)
    return render(request, "encyclopedia/entry.html",{
        "entry": md.markdown(util.get_entry(selected_page)),
        "title": selected_page
    })

def search(request):
    query = request.GET['q']

    # if entry with query name doesnt exists, returns None
    if util.get_entry(query):
        # query matches entry name
        return HttpResponseRedirect(reverse("entry", args=(query,)))
    else:
        # query does not match!
        return render(request, "encyclopedia/index.html", {
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
            "title": f'"{query}" search results',
            "heading": f'Search Results for "{query}"'
        })