# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CourseStruct.released'
        db.add_column('learning_analytics_coursestruct', 'released',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CourseStruct.released'
        db.delete_column('learning_analytics_coursestruct', 'released')


    models = {
        'learning_analytics.courseaccesses': {
            'Meta': {'unique_together': "((u'student_id', u'course_id'),)", 'object_name': 'CourseAccesses'},
            'accesses': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '2000'}),
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_calc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'learning_analytics.coursestruct': {
            'Meta': {'unique_together': "((u'module_state_key', u'course_id'),)", 'object_name': 'CourseStruct'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['learning_analytics.CourseStruct']", 'null': 'True', 'blank': 'True'}),
            'graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'module_state_key': ('xmodule_django.models.LocationKeyField', [], {'max_length': '255', 'db_column': "u'module_id'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'released': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'section_type': ('django.db.models.fields.CharField', [], {'default': "u'chapter'", 'max_length': '32', 'db_index': 'True'})
        },
        'learning_analytics.coursetime': {
            'Meta': {'unique_together': "((u'student_id', u'course_id'),)", 'object_name': 'CourseTime'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_calc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {}),
            'time_spent': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '1000'})
        },
        'learning_analytics.sortgrades': {
            'Meta': {'unique_together': "((u'label', u'course_id'),)", 'object_name': 'SortGrades'},
            'category': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'last_calc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'num_fail': ('django.db.models.fields.IntegerField', [], {}),
            'num_not': ('django.db.models.fields.IntegerField', [], {}),
            'num_pass': ('django.db.models.fields.IntegerField', [], {}),
            'num_prof': ('django.db.models.fields.IntegerField', [], {}),
            'sort_type': ('django.db.models.fields.CharField', [], {'default': "u'GS'", 'max_length': '32'})
        },
        'learning_analytics.studentgrades': {
            'Meta': {'unique_together': "((u'student_id', u'course_id'),)", 'object_name': 'StudentGrades'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'grade_group': ('django.db.models.fields.CharField', [], {'default': "u'FAIL'", 'max_length': '32'}),
            'grades': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_calc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'learning_analytics.timeschedule': {
            'Meta': {'unique_together': "((u'student_id', u'course_id'),)", 'object_name': 'TimeSchedule'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_calc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {}),
            'time_schedule': ('django.db.models.fields.TextField', [], {'default': "u''"})
        }
    }

    complete_apps = ['learning_analytics']