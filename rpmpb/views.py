from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Miniature
from .models import Album
from .models import Tag
from .models import PhotoSession

def index(request):
    context = {}
    return render(request, 'rpmpb/index.html', context)


def mini_index(request):
    minis = Miniature.objects.order_by('name')
    context = {'minis': minis}
    return render(request, 'rpmpb/mini_index.html', context)


def mini_detail(request, slug):
    mini = get_object_or_404(Miniature, slug_name=slug)
    context = {'mini': mini}
    return render(request, 'rpmpb/mini_detail.html', context)


def album_index(request):
    albums = Album.objects.order_by('name')
    context = {'albums': albums}
    return render(request, 'rpmpb/album_index.html', context)


def album_detail(request, slug):
    context = {}
    if request.method =="POST" and not slug == "new":
        # update existing album
        album = get_object_or_404(Album, slug_name=slug)
        album.slug_name = request.POST['album-slug']
        album.name = request.POST['album-name']
        album.save()
        return HttpResponseRedirect(reverse('rpmpb:album-detail', 
            args=(album.slug_name,)))
    elif request.method == "POST" and slug == "new":
        if request.POST['album-slug'] == "new":
            error_message = "The slug needs to be changed."
            context['error_message'] = error_message
            album = Album(slug_name="new")
            return render(request, 'rpmpb/album_detail.html', context)
        else:
            album = Album()
            album.slug_name = request.POST['album-slug']
            album.name = request.POST['album-name']
            album.save()
            return HttpResponseRedirect(reverse('rpmpb:album-detail', 
                args=(album.slug_name,)))
    elif request.method == "GET" and not slug == "new":
        # show existing one
        album = get_object_or_404(Album, slug_name=slug)
        context['album'] = album
        return render(request, 'rpmpb/album_detail.html', context)
    elif request.method == "GET" and slug == "new":
        # create a new album
        album = Album(slug_name="new", name="New Album")
        context['album'] = album
        return render(request, 'rpmpb/album_detail.html', context)
    else:
        # something's wrong
        pass
        # TODO
    
    


def album_update(request, id):
    album = get_object_or_404(Album, pk=id)
    

def tag_index(request):
    tags = Tag.objects.order_by('slug_name')
    context = {'tags': tags}
    return render(request, 'rpmpb/tag_index.html', context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug_name=slug)
    context = {'tag': tag}
    return render(request, 'rpmpb/tag_detail.html', context)


def photo_index(request):
    photo = PhotoSession.objects.order_by('slug_name')
    context = {'photo': photo}
    return render(request, 'rpmpb/photo_index.html', context)