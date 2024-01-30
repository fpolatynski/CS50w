import secrets
import markdown2

from django import forms

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from . import util


class NewEntriesField(forms.Form):
    title = forms.CharField(label="Title")
    entries = forms.CharField(label="Enter markdown text", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entries):
    return render(request, "encyclopedia/entry_page.html", {
        "title": entries,
        "content": markdown2.markdown(util.get_entry(entries))
    })


def search(request):
    query = request.GET.get('q', None)
    if not query:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
    searched_pages = util.search_entries(query)
    return render(request, "encyclopedia/index.html", {
        "entries": searched_pages
    })


def add(request):
    if request.method == 'POST':
        form = NewEntriesField(request.POST)
        if form.is_valid():
            entries_text = form.cleaned_data["entries"]
            entries_title = form.cleaned_data["title"]
            if entries_title in util.list_entries():
                messages.add_message(request, messages.ERROR, "entry already exist")
            else:
                util.save_entries(entries_text, entries_title)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
    return render(request, "encyclopedia/new_wiki.html", {
        "form": NewEntriesField
    })


def edit(request, entries):
    default_data = {"title": entries, "entries": util.get_entry(entries)}
    if request.method == 'POST':
        edits = NewEntriesField(request.POST)
        if edits.is_valid():
            edits_text = edits.cleaned_data["entries"]
            edits_title = edits.cleaned_data["title"]
            print(edits.cleaned_data)
            util.save_entry(edits_title, edits_text)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    return render(request, "encyclopedia/edit_wiki.html", {
        "edit_form": NewEntriesField(initial=default_data),
        "title": entries,
    })


def random_page(request):
    entries = util.list_entries()
    entry = secrets.choice(entries)
    text = util.get_entry(entry)
    return render(request, "encyclopedia/entry_page.html",{
        "title": entry,
        "content": markdown2.markdown(text)
    })
