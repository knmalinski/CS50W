from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random

from . import util

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,name):
    entry = util.get_entry(name)
    if entry == None:
            return render(request, "encyclopedia/error.html",{
            "error": "No Article!"
        })
    else:
        markdownentry = Markdown()
        htmlentry = markdownentry.convert(entry)
        return render(request,"encyclopedia/entry.html",{
            "entry_text": htmlentry,
            "entry_name": name
        })

def search(request): 
    matches = []
    if request.method == "POST":
        querry = request.POST.get("q")
        entries = util.list_entries()
        #### check if exact match
        for article in entries:
            if article.lower() == querry.lower().strip():
                #### redirect to querry####
                return HttpResponseRedirect(f"wiki/{querry}")
            elif querry.lower().strip() in article.lower().strip(): 
                matches.append(article)
            else:
                pass

        if len(matches) > 0: 
            return render(request,"encyclopedia/search.html",{
                "matches": matches 
                })
        else:
            return render(request, "encyclopedia/error.html",{
                "error": "No Search Results"
                })
    else: 
        pass

def new_page(request):
     if request.method == "POST":
        new_title = request.POST.get("new_title")
        new_post = request.POST.get("new_page")
        if check_if_entry(new_title):
            util.save_entry(new_title, new_post)
            return HttpResponseRedirect(f"wiki/{new_title}")
        else:
            return render(request, "encyclopedia/error.html",{
                "error": "Entry allready exists!"
                })
     else:
        return render(request,"encyclopedia/new_page.html",{
                    "title":"Title",
                    "message": "New Page here"  
                    })


def error(request):
    return render(request, "encyclopedia/error.html",{
            "error": "help!!"
        })
                  

def check_if_entry(name):
    entries = util.list_entries()
    if name in entries:
        return False
    else: 
        return True
    
def edit_page(request):
    if request.method == "POST":
        edit_title = request.POST.get("entry_name")
        edit_post = util.get_entry(edit_title)
        return render(request,"encyclopedia/edit_page.html",{
                    "title": edit_title,
                    "entry_text": edit_post 
                    })

def save_page(request):
    if request.method == "POST":
        save_title = request.POST.get("edit_title")
        save_post = request.POST.get("entry_text")
        util.save_entry(save_title, save_post)
        return HttpResponseRedirect(f"wiki/{save_title}")

def rand(request):
    random_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(f"wiki/{random_entry}")