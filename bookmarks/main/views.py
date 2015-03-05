from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.db import DatabaseError

# Create your views here.

from main.models import Link, Tag

def index(request):
    # Request the context of the request.
    # The context contains information such as the clients machine details, for exmaple.
    context = RequestContext(request)

    # Get all links
    links = Link.objects.all()

    return render_to_response('main/index.html', {'links': links, 'active': 'index'}, context)

def tags(request):
    context = RequestContext(request)

    tags = Tag.objects.all()

    return render_to_response('main/index.html', {'tags': tags, 'active': 'tags'}, context)

def tag(request, tag_name):
    context = RequestContext(request)
    the_tag = Tag.objects.get(name=tag_name)
    links = the_tag.link_set.all()

    return render_to_response('main/index.html', {'links': links, 'tag_name':'#' + tag_name}, context)

def add_link(request):
    context = RequestContext(request)
    if request.method == 'POST':
        url = request.POST.get("url", "")
        tags = request.POST.get("tags", "")
        title = request.POST.get("title", "")

        tag_list = tags.split(r'/,\s*/')

        try:
            entry = Link.objects.create(url=url, title=title)
        except DatabaseError:
            return redirect(index)


        for ta in tag_list:
            try:
                entry.tags.create(name=ta)
            except DatabaseError:
                entry.tags.add(Tag.objects.get(name=ta))

    return redirect(index)