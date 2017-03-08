import json
import shutil
from celery.task import task
from django.conf import settings
from django.db.models import Q
from downloader_ctrl import DownloadManager
from models import MediaDownload


@task()
def sync_downloads():

    # get the list of active downloads
    downloader = DownloadManager(settings.DOWNLOAD_ROOT, settings.PIDFILE_FILENAME, settings.ARIA2_CONF_FILENAME)
    downloader.launch_if_required()

    valid_gids = []

    downloads = downloader.get_active_downloads()

    for info in downloads:

        gid = info['gid']

        valid_gids.append(gid)

        total_length = int(info['totalLength'])
        completed_length = int(info['completedLength'])
        download_speed = int(info['downloadSpeed'])
        seeder_count = 0
        leecher_count = 0

        status = info['status']

        name = 'Unknown'

        if 'bittorrent' in info:

            seeder_count = int(info['numSeeders'])
            leecher_count = int(info['connections'])

            bt = info['bittorrent']

            if 'info' in bt:
                bt_info = bt['info']
                name = bt_info['name']
            else:
                name = 'Retrieving download info...'

            print info

        try:
            item = MediaDownload.objects.get(download_id=gid)
        except MediaDownload.DoesNotExist:
            item = MediaDownload(
                download_id=gid,
                download_url='http://google.com',
                display_name=name,
                info_hash='',
                percent_complete=0,
            )

        item.total_length = total_length
        item.completed_length = completed_length

        item.download_speed_bps = download_speed
        item.seeder_count = seeder_count
        item.leecher_count = leecher_count

        item.file_info_json=json.dumps(info['files'])

        if item.total_length > 0:
            item.percent_complete = int((float(item.completed_length) / float(item.total_length)) * 100.00)

        item.save()

    # invalids = MediaDownload.objects.filter(~Q(download_id__in=valid_gids))
    #
    # for invalid in invalids:
    #     invalid.delete()