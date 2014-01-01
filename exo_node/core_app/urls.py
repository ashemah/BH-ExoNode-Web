from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, RedirectView
from views import MovieListView, TVShowListView, SearchView, DownloadListView, DownloadView, DownloadItemsView, NowPlayingView, MediaControlView

urlpatterns = patterns('',
    url(r'^movies/$', MovieListView.as_view(), name='movies'),
    url(r'^tvshows/$', TVShowListView.as_view(), name='tvshows'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^search/results/$', SearchView.as_view(), name='search-results'),
    url(r'^downloads/$', DownloadListView.as_view(), name='downloads'),
    url(r'^downloads/add/$', DownloadView.as_view(), name='download-add'),
    url(r'^downloads/list/$', DownloadItemsView.as_view(), name='download-items'),
    url(r'^media/control/$', csrf_exempt(MediaControlView.as_view()), name='media-control'),
    url(r'^media/nowplaying/$', NowPlayingView.as_view(), name='nowplaying'),
)
