import subprocess
import urllib
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from tasks import sync_downloads
from models import MediaItem, MediaGroup, MediaDownload, NowPlaying
import player_ctrl
import guessit
from KickassAPI import Search, Latest, User, CATEGORY, ORDER
from downloader_ctrl import DownloadManager

class MovieListView(ListView):
    model = MediaItem
    template_name = "movies.html"

    def get_queryset(self):
        return MediaItem.objects.filter(media_type=MediaItem.MEDIA_TYPE_MOVIE).order_by('display_name')


class TVShowListView(ListView):
    model = MediaItem
    template_name = "tvshows.html"

    def get_queryset(self):
        return MediaGroup.objects.filter(group_type=MediaGroup.GROUP_TYPE_TVSHOW).order_by('display_name')


class DownloadListView(ListView):
    model = MediaDownload
    template_name = "downloads.html"


class DownloadView(View):

    def get(self, request):

        url = request.GET.get('url')
        name = request.GET.get('name')

        downloader = DownloadManager(settings.DOWNLOAD_ROOT, settings.PIDFILE_FILENAME, settings.ARIA2_CONF_FILENAME)
        downloader.launch_if_required()
        gid = downloader.add_download(url)

        sync_downloads()

        from django.contrib import messages
        messages.success(request, "Successfully added '%s'." % name)

        return HttpResponseRedirect(redirect_to='/search/')


class DownloadItemsView(ListView):

    model = MediaDownload
    template_name = "downloads_list.html"

    def get_queryset(self):
        return MediaDownload.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DownloadItemsView, self).get_context_data(**kwargs)

        sync_downloads()

        return context


class SearchView(View):

    def get(self, request):

        target = request.GET.get('target', None)
        if target == 'search-results':
            return self.generate_search_results(request)
        else:
            search_query = request.session.get('search_query', None)
            return render(request, 'search.html', {
                'search_query': search_query
            })

    def generate_search_results(self, request):

        query = request.GET.get('q', None)

        cleaned_results = []

        if not query:
            cleaned_results = request.session.get('search_results', None)
            query = request.session.get('search_query', None)
        else:
            results = Search(query)

            cleaned_results = []

            for result in results:
                cleaned_results.append({
                    'display_name': result.name,
                    'url': result.magnet_link,
                    'seeder_count': result.seed,
                    'leecher_count': result.leech,
                })

            request.session['search_results'] = cleaned_results
            request.session['search_query'] = query

        return render(request, 'search_results.html', {'object_list': cleaned_results, 'search_query': query})


class MediaControlView(View):

    def post(self, request):

        player = player_ctrl.PlayerController(settings.VLC_PATH, settings.VLC_PIDFILENAME, settings.VLC_SOCKFILE)

        cmd = request.GET.get('cmd')

        res = ''

        if cmd == 'play':

            # Tell the frame to play something
            obj_id = request.GET.get('id')
            obj = MediaItem.objects.get(pk=obj_id)

            res = player.play(obj.media_filename.path)

        elif cmd == 'stop':

            res = player.stop()

        elif cmd == 'pause':

            res = player.pause()

        elif cmd == 'jump_forward':

            res = player.jump_forward()

        elif cmd == 'jump_backward':

            res = player.jump_backward()

        return HttpResponse(res)


class NowPlayingView(View):

    def get(self, request):

        player = player_ctrl.PlayerController(settings.VLC_PATH, settings.VLC_PIDFILENAME, settings.VLC_SOCKFILE)
        is_playing = player.get_is_playing()
        cur_time = player.get_time()
        total_length = player.get_length()
        title = player.get_title()

        return render(request, 'now_playing.html', {
            'is_playing': is_playing,
            'cur_time': cur_time,
            'total_length': total_length,
            'title': title
        })

class UpgradeView(View):

    def get(self, request):

        subprocess.Popen('python upgrade.py', shell=True, close_fds=True)

        return HttpResponseRedirect("/movies/")
