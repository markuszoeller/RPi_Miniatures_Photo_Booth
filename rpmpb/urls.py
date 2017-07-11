from django.conf.urls import url

from . import views


app_name = 'rpmpb'

# TODO: maybe put the CRUDL actions into the URLs?
# something like:
# new/minis/
# show/minis/<slug>
# edit/minis/<slug>
# del/minis/<slug>
# list/minis/
# We're not at a REST API level here, so maybe that would be OK.
# Would remove some conditionals in the code.




urlpatterns = [
    url(r'^list/minis/$', 
    	views.MiniatureIndexView.as_view(), 
    	name='mini-index'),
    url(r'^show/minis/(?P<slug>[\w-]+)/$', 
    	views.MiniatureDetailView.as_view(), 
    	name='mini-detail'),
    url(r'^del/minis/(?P<slug>[\w-]+)/$',
        views.MiniatureDeleteView.as_view(),
        name="mini-delete"),
    url(r'^new/minis/$',
    	views.MiniatureCreateView.as_view(),
    	name='mini-create'),
    url(r'^edit/minis/(?P<slug>[\w-]+)/$',
        views.MiniatureUpdate.as_view(),
        name='mini-update'),
    url(r'^albums/$', 
    	views.AlbumIndexView.as_view(), 
    	name='album-index'),
    url(r'^albums/(?P<slug>[\w-]+)/$', 
    	views.album_detail, 
    	name='album-detail'),
    url(r'^tags/$', 
    	views.tag_index, 
    	name='tag-index'),
    url(r'^tags/(?P<slug>[\w-]+)/$', 
    	views.tag_detail, 
    	name='tag-detail'),
    url(r'^photo/$', 
    	views.photo_index, 
    	name='photo-index'),
    url(r'^$', 
    	views.index, 
    	name='index'),
]