from django.conf import settings
from django.db import models


class MediaGroup(models.Model):

    GROUP_TYPE_UNKNOWN = 0
    GROUP_TYPE_TVSHOW = 1
    GROUP_TYPE_MUSIC_ALBUM = 2
    GROUP_TYPE_PHOTO_ALBUM = 3

    GROUP_TYPE_CHOICES = (
        (GROUP_TYPE_UNKNOWN, "Unknown"),
        (GROUP_TYPE_TVSHOW, "TV Show"),
        (GROUP_TYPE_MUSIC_ALBUM, "Music Album"),
        (GROUP_TYPE_PHOTO_ALBUM, "Photo Album"),
    )

    group_type = models.IntegerField(choices=GROUP_TYPE_CHOICES, default=GROUP_TYPE_UNKNOWN)
    parent = models.ForeignKey("MediaGroup", null=True, related_name='sub_groups')
    short_name = models.SlugField(max_length=255)
    display_name = models.CharField(max_length=255)
    image_filename = models.ImageField(null=True, blank=True, upload_to=settings.MEDIA_ROOT)
    thumbnail_filename = models.ImageField(null=True, blank=True, upload_to=settings.MEDIA_ROOT)
    date_created = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.display_name

    @property
    def sorted_items(self):
        return self.items.order_by('-id')


class MediaItem(models.Model):

    MEDIA_TYPE_UNKNOWN = 0
    MEDIA_TYPE_MOVIE = 1
    MEDIA_TYPE_TVSHOW = 2
    MEDIA_TYPE_MUSIC = 3
    MEDIA_TYPE_PHOTO = 4

    MEDIA_TYPE_CHOICES = (
        (MEDIA_TYPE_UNKNOWN, "Unknown"),
        (MEDIA_TYPE_MOVIE, "Movie"),
        (MEDIA_TYPE_TVSHOW, "TV Show"),
        (MEDIA_TYPE_MUSIC, "Music"),
        (MEDIA_TYPE_PHOTO, "Photo"),
    )

    INFO_STATUS_NONE = 0
    INFO_STATUS_BASIC = 1
    INFO_STATUS_FULL = 2

    INFO_STATUS_CHOICES = (
        (INFO_STATUS_NONE, "No info"),
        (INFO_STATUS_BASIC, "Basic info"),
        (INFO_STATUS_FULL, "Full info")
    )

    # Shared
    media_type = models.IntegerField(choices=MEDIA_TYPE_CHOICES)
    info_status = models.IntegerField(choices=INFO_STATUS_CHOICES)
    group = models.ForeignKey(MediaGroup, null=True, default=None, related_name='items')
    short_name = models.SlugField(max_length=255)
    display_name = models.CharField(max_length=255)
    media_filename = models.FileField(null=True, blank=True, upload_to=settings.MEDIA_ROOT)
    image_filename = models.ImageField(null=True, blank=True, upload_to=settings.MEDIA_ROOT)
    thumbnail_filename = models.ImageField(null=True, blank=True, upload_to=settings.MEDIA_ROOT)
    description = models.TextField(null=True, blank=True)
    imdb_id = models.URLField(null=True, blank=True)
    media_hash = models.CharField(max_length=255, null=True, blank=True)

    date_created = models.DateField(null=True, blank=True)
    date_viewed = models.DateField(null=True, blank=True)

    # TV Shows
    season_number = models.IntegerField(default=-1)
    episode_numbers = models.CommaSeparatedIntegerField(max_length=255)

    # Search
    original_download_name = models.CharField(max_length=255, default="")

    def __unicode__(self):
        return self.display_name


class MediaDownload(models.Model):
    download_id = models.CharField(max_length=20)
    download_url = models.URLField()
    info_hash = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=255)
    total_length = models.IntegerField()
    completed_length = models.IntegerField()
    percent_complete = models.IntegerField()
    download_speed_bps = models.IntegerField(default=0)
    seeder_count = models.IntegerField(default=0)
    leecher_count = models.IntegerField(default=0)
    file_info_json = models.TextField(null=True, blank=True)

    def is_complete(self):
        return self.completed_length == self.total_length

    def download_speed_kps(self):
        return self.download_speed_bps / 1000

    def __unicode__(self):
        return "%s - %s" % (self.download_id, self.display_name,)

    @classmethod
    def get_completed_items(cls):
        return MediaDownload.objects.filter(percent_complete=100)


class NowPlaying(models.Model):

    display_name = models.CharField(max_length=255)

    @classmethod
    def get_now_playing(cls):

        try:
            return NowPlaying.objects.first()
        except NowPlaying.DoesNotExist:
            return None

    @classmethod
    def set_now_playing(cls, display_name):

        now_playing = NowPlaying(display_name=display_name)
        now_playing.save()

        return now_playing

    @classmethod
    def clear_now_playing(cls):

        NowPlaying.objects.all().delete()