from django.shortcuts import render
from django import forms
import markdown as md
import random

from . import util


def index(request):
    """
    Home page (index page)
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry_title):
    
    # If the entry does exist, the user should be presented 
    # with a page that displays the content of the entry. 
    # The title of the page should include the name of the entry.
    try: 
        return render(request, "encyclopedia/entry.html",{
            "entry": md.markdown(util.get_entry(entry_title)),
            "title": entry_title
        })

    # If an entry is requested that does not exist, 
    # the user should be presented with an error page 
    # indicating that their requested page was not found. 
    except:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.markdown(util.get_entry("ERROR")),
            "title": "ERROR"
        })

def random_page(request):
    
    selected_page = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html",{
            "entry": md.markdown(util.get_entry(selected_page)),
            "title": selected_page
        })

def search(request):
    query = request.GET['q']

    # if entry with query name doesnt exists, returns None
    if util.get_entry(query):
        # query matches entry name
        return render(request, "encyclopedia/entry.html",{
            "entry": md.markdown(util.get_entry(query)),
            "title": query
        })
    else:
        # query does not match, check name in lowercase
        return render(request, "encyclopedia/index.html", {
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
        })

def new_page(request):
    return render(request, "encyclopedia/new-page.html")

def save_page(request):
    """ Returns the information from the POST request on the Create new page template. Then saves the page """

    if request.method == 'POST':
        input_title = request.POST['title']
        input_text = request.POST['text_body']
        
        if util.get_entry(input_title):
            # entry already exists
            return render(request, "encyclopedia/already-exists.html",{
                "entry": md.markdown(util.get_entry(input_title)),
                "title": input_title
                })

        else:
            # entry does not exist, check name in lowercase
            check = [entry for entry in util.list_entries() if input_title.lower() in entry.lower()]
            print("check = ", check)
            print(check != [])
            if check != []:
                return render(request, "encyclopedia/index.html", {
                    "entries": md.markdown(util.get_entry(input_title.lower())),
                    })
            else:
                print("GUARDANDO")
                util.save_entry(input_title, input_text)

                return render(request, "encyclopedia/entry.html",{
                    "entry": md.markdown(util.get_entry(input_title)),
                    "title": input_title
                    })

def edit_page (request):
    
    """Function called after pressing edit button. Renders a page with a form"""
    
    if request.method == 'POST':
        # get entry using entry title
        entry_title = request.POST['title']
        entry = util.get_entry(entry_title)

        # Initiate form with latest entry text
        # We don't turn this into html because the user uses markdown
        return render(request, "encyclopedia/edit-page.html",{
            "entry": entry,
            "title": entry_title
            })

def save_page_edit(request):
    # After editing the page, save it
    if request.method == "POST":
        entry_title = request.POST['title']
        entry = request.POST['text_body']

        util.save_entry(entry_title, entry)

        return render(request, "encyclopedia/entry.html", {
            "entry": md.markdown(util.get_entry(entry_title)),
            "title": entry_title
        })

