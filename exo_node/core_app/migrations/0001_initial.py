# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MediaGroup'
        db.create_table(u'core_app_mediagroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sub_groups', null=True, to=orm['core_app.MediaGroup'])),
            ('short_name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image_filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail_filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core_app', ['MediaGroup'])

        # Adding model 'MediaItem'
        db.create_table(u'core_app_mediaitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media_type', self.gf('django.db.models.fields.IntegerField')()),
            ('info_status', self.gf('django.db.models.fields.IntegerField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='items', null=True, to=orm['core_app.MediaGroup'])),
            ('short_name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('media_filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('image_filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail_filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('imdb_id', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('media_hash', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_viewed', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('season_number', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('episode_numbers', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=255)),
        ))
        db.send_create_signal(u'core_app', ['MediaItem'])

        # Adding model 'MediaDownload'
        db.create_table(u'core_app_mediadownload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('download_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('download_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('info_hash', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('total_length', self.gf('django.db.models.fields.IntegerField')()),
            ('completed_length', self.gf('django.db.models.fields.IntegerField')()),
            ('percent_complete', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core_app', ['MediaDownload'])


    def backwards(self, orm):
        # Deleting model 'MediaGroup'
        db.delete_table(u'core_app_mediagroup')

        # Deleting model 'MediaItem'
        db.delete_table(u'core_app_mediaitem')

        # Deleting model 'MediaDownload'
        db.delete_table(u'core_app_mediadownload')


    models = {
        u'core_app.mediadownload': {
            'Meta': {'object_name': 'MediaDownload'},
            'completed_length': ('django.db.models.fields.IntegerField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'download_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'download_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'percent_complete': ('django.db.models.fields.IntegerField', [], {}),
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