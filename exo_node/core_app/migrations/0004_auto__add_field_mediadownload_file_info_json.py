# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MediaDownload.file_info_json'
        db.add_column(u'core_app_mediadownload', 'file_info_json',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MediaDownload.file_info_json'
        db.delete_column(u'core_app_mediadownload', 'file_info_json')


    models = {
        u'core_app.mediadownload': {
            'Meta': {'object_name': 'MediaDownload'},
            'completed_length': ('django.db.models.fields.IntegerField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'download_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'download_speed_bps': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'download_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'file_info_json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'leecher_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percent_complete': ('django.db.models.fields.IntegerField', [], {}),
            'seeder_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_length': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core_app.mediagroup': {
            'Meta': {'object_name': 'MediaGroup'},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_groups'", 'null': 'True', 'to': u"orm['core_app.MediaGroup']"}),
            'short_name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'thumbnail_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core_app.mediaitem': {
            'Meta': {'object_name': 'MediaItem'},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_viewed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'episode_numbers': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'to': u"orm['core_app.MediaGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'imdb_id': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'info_status': ('django.db.models.fields.IntegerField', [], {}),
            'media_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'media_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'media_type': ('django.db.models.fields.IntegerField', [], {}),
            'season_number': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'short_name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'thumbnail_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core_app']