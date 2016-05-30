# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OutputLoggedRequest.response_headers'
        db.alter_column(u'security_outputloggedrequest', 'response_headers', self.gf('jsonfield.fields.JSONField')(null=True))

        # Changing field 'OutputLoggedRequest.queries'
        db.alter_column(u'security_outputloggedrequest', 'queries', self.gf('jsonfield.fields.JSONField')(null=True))

        # Changing field 'OutputLoggedRequest.request_headers'
        db.alter_column(u'security_outputloggedrequest', 'request_headers', self.gf('jsonfield.fields.JSONField')(null=True))

        # Changing field 'InputLoggedRequest.response_headers'
        db.alter_column(u'security_inputloggedrequest', 'response_headers', self.gf('jsonfield.fields.JSONField')(null=True))

        # Changing field 'InputLoggedRequest.request_headers'
        db.alter_column(u'security_inputloggedrequest', 'request_headers', self.gf('jsonfield.fields.JSONField')(null=True))

        # Changing field 'InputLoggedRequest.queries'
        db.alter_column(u'security_inputloggedrequest', 'queries', self.gf('jsonfield.fields.JSONField')(null=True))

    def backwards(self, orm):

        # Changing field 'OutputLoggedRequest.response_headers'
        db.alter_column(u'security_outputloggedrequest', 'response_headers', self.gf('json_field.fields.JSONField')(null=True))

        # Changing field 'OutputLoggedRequest.queries'
        db.alter_column(u'security_outputloggedrequest', 'queries', self.gf('json_field.fields.JSONField')(null=True))

        # Changing field 'OutputLoggedRequest.request_headers'
        db.alter_column(u'security_outputloggedrequest', 'request_headers', self.gf('json_field.fields.JSONField')(null=True))

        # Changing field 'InputLoggedRequest.response_headers'
        db.alter_column(u'security_inputloggedrequest', 'response_headers', self.gf('json_field.fields.JSONField')(null=True))

        # Changing field 'InputLoggedRequest.request_headers'
        db.alter_column(u'security_inputloggedrequest', 'request_headers', self.gf('json_field.fields.JSONField')(null=True))

        # Changing field 'InputLoggedRequest.queries'
        db.alter_column(u'security_inputloggedrequest', 'queries', self.gf('json_field.fields.JSONField')(null=True))

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'security.inputloggedrequest': {
            'Meta': {'ordering': "(u'-request_timestamp',)", 'object_name': 'InputLoggedRequest'},
            'error_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exception_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'is_secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'queries': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'request_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'request_headers': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'request_timestamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'response_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'response_headers': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'response_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'security.outputloggedrequest': {
            'Meta': {'ordering': "(u'-request_timestamp',)", 'object_name': 'OutputLoggedRequest'},
            'error_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exception_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'queries': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'request_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'request_headers': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'request_timestamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'response_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'response_headers': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'response_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'security.outputloggedrequestrelatedobjects': {
            'Meta': {'object_name': 'OutputLoggedRequestRelatedObjects'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'output_logged_request': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'related_objects'", 'to': u"orm['security.OutputLoggedRequest']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['security']