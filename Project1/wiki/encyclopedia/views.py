from django.shortcuts import render
import markdown as md

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
