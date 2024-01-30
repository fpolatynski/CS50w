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
        "content": util.get_entry(entries)
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
    # TODO: send changes to server
    default_data = {"title": entries, "entries": util.get_entry(entries)}
    edits = NewEntriesField(default_data)
    return render(request, "encyclopedia/new_wiki.html", {
        "form": edits
    })
