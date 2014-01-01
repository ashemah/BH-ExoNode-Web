import json
import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import guessit
from core_app.models import MediaGroup, MediaItem, MediaDownload
from django.template.defaultfilters import slugify
from core_app.downloader_ctrl import DownloadManager


class Command(BaseCommand):
    args = '--rebuild'
    help = 'Updates the media library'

    def handle(self, *args, **options):

        count = 0

        self.stdout.write('Beginning library update...\n')

        # List everything in the media inbox
        # For each file in there that is a media file (mp4, mkv) run guessit on it to work out where it goes
        # Copy it to the media directory in the right placce

        # Movies root folder
        if not os.path.exists(settings.MOVIES_ROOT):
            os.makedirs(settings.MOVIES_ROOT)

        if not os.path.exists(settings.TVSHOWS_ROOT):
            os.makedirs(settings.TVSHOWS_ROOT)

        if not os.path.exists(settings.DOWNLOAD_ROOT):
            os.makedirs(settings.DOWNLOAD_ROOT)

        if not os.path.exists(settings.MEDIA_INBOX_ROOT):
            os.makedirs(settings.MEDIA_INBOX_ROOT)

        # Move any completed files
        self.move_completed_files()

        matches = []
        for root, dirnames, filenames in os.walk(settings.MEDIA_INBOX_ROOT):

            for filename in filenames:
                rest, ext = os.path.splitext(filename)
                ext = ext[1:]
                if ext in settings.ALLOWED_MEDIA_FILE_EXTENSIONS:
                    filepath = os.path.join(root, filename)
                    matches.append(filepath)

        self.process_matches(matches)

        self.stdout.write('Processed %d files.\n' % count)

    def move_completed_files(self):

        downloader = DownloadManager(settings.DOWNLOAD_ROOT, settings.PIDFILE_FILENAME, settings.ARIA2_CONF_FILENAME)
        downloader.launch_if_required()

        print "Moving completed files..."

        completed = MediaDownload.get_completed_items()

        for item in completed:

            print 'Moving "%s" to inbox...' % item

            # Skip if it's invalid
            if not item.file_info_json or len(item.file_info_json) == 0:
                continue

            files = json.loads(item.file_info_json)

            for f in files:
                path = f['path']
                fname, ext = os.path.splitext(path)
                ext = ext[1:]
                if ext in settings.ALLOWED_MEDIA_FILE_EXTENSIONS:
                    basename = os.path.basename(path)
                    final_pathname = os.path.join(settings.MEDIA_INBOX_ROOT, basename)

                    if os.path.exists(path):
                        shutil.move(path, final_pathname)
                    else:
                        print "Could not find '%s' to move." % path

            downloader.remove_download(item.download_id)

            item.delete()

        downloader.purge_results()

    def process_matches(self, matches):

        for filepath in matches:
            guess = guessit.guess_video_info(filepath)
            media_type = guess['type']

            if media_type == 'movie':
                self.process_movie(guess, filepath)
            elif media_type == 'episode':
                self.process_show(guess, filepath)

    def process_show(self, info, filepath):

        # print info
        # print filepath

        season_number = int(info['season'])
        series_name = info['series']
        season_name = "Season %s" % season_number

        if 'episodeList' in info:
            episode_list = info['episodeList']
        else:
            episode_list = [info['episodeNumber']]

        episode_long_list = ["%02d" % int(episode) for episode in episode_list]
        episodes = "+".join(episode_long_list)

        display_name = "%s - %d x %s" % (series_name, season_number, episodes)
        final_path = os.path.join(settings.TVSHOWS_ROOT, series_name, season_name)
        if not os.path.exists(final_path):
            os.makedirs(final_path)

        filename = "%s - %d x %s.%s" % (series_name, season_number, episodes, info['container'])
        final_filename = os.path.join(final_path, filename)

        if os.path.exists(final_filename):
            os.unlink(final_filename)

        shutil.move(filepath, final_filename)
        series_name_slug = slugify(series_name)

        try:
            series_group = MediaGroup.objects.get(short_name=series_name_slug)
        except MediaGroup.DoesNotExist:
            series_group = MediaGroup(
                group_type=MediaGroup.GROUP_TYPE_TVSHOW,
                display_name=series_name,
                short_name=series_name_slug
            )
            series_group.save()

        # Update db
        item_name_slug = slugify(display_name)

        try:
            item = MediaItem.objects.get(short_name=item_name_slug)
        except MediaItem.DoesNotExist:
            item = MediaItem(
                media_type=MediaItem.MEDIA_TYPE_TVSHOW,
                info_status=MediaItem.INFO_STATUS_NONE,
                group=series_group,
                display_name=display_name,
                short_name=item_name_slug,
                episode_numbers=episode_list,
                season_number=season_number,
            )

            item.media_filename.name = final_filename
            item.save()

        self.stdout.write('Moved file: "%s" -> %s.\n' % (display_name, final_filename))

    def process_movie(self, info, filepath):

        print info
        print filepath

        title = info['title']

        has_year = False
        if 'year' in info:
            year = info['year']
            has_year = True

        container = info['container']

        # Copy it to its new location
        # Write some info about it into the db
        if has_year:
            display_name = "%s (%s)" % (info['title'], info['year'])
        else:
            display_name = "%s" % info['title']

        final_path = os.path.join(settings.MOVIES_ROOT, display_name)
        if not os.path.exists(final_path):
            os.makedirs(final_path)

        if has_year:
            filename = "%s (%s).%s" % (info['title'], info['year'], info['container'])
        else:
            filename = "%s.%s" % (info['title'], info['container'])

        final_filename = os.path.join(final_path, filename)

        if os.path.exists(final_filename):
            os.unlink(final_filename)

        shutil.move(filepath, final_filename)

        item_name_slug = slugify(display_name)

        # Update db
        try:
            item = MediaItem.objects.get(short_name=item_name_slug)
        except MediaItem.DoesNotExist:
            item = MediaItem(
                media_type=MediaItem.MEDIA_TYPE_MOVIE,
                info_status=MediaItem.INFO_STATUS_NONE,
                display_name=display_name,
                short_name=item_name_slug
            )

            item.media_filename.name = final_filename
            item.save()

        self.stdout.write('Moved file: "%s" -> %s.\n' % (display_name, final_filename))
