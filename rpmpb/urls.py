from django.conf.urls import url

from . import views


app_name = 'rpmpb'

urlpatterns = [
    url(r'^minis/$', views.mini_index, name='mini-index'),
    url(r'^minis/(?P<slug>[\w-]+)/$', views.mini_detail, name='mini-detail'),
    url(r'^albums/$', views.album_index, name='album-index'),
    url(r'^albums/(?P<slug>[\w-]+)/$', views.album_detail, name='album-detail'),
    url(r'^tags/$', views.tag_index, name='tag-index'),
    url(r'^tags/(?P<slug>[\w-]+)/$', views.tag_detail, name='tag-detail'),
    url(r'^photo/$', views.photo_index, name='photo-index'),
    url(r'^$', views.index, name='index'),
]