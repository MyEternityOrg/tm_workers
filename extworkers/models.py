import uuid

from django.contrib.auth.models import User
from django.db import models
from outsourcing.models import Enterprises


# Create your models here.


class ExtWorkerRecord(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='guid')
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    dts = models.DateField(db_column='dts')
    person_name = models.CharField(db_column='person_name', max_length=128)
    f_time = models.TimeField(db_column='f_time')
    t_time = models.TimeField(db_column='t_time')
    p_city = models.CharField(db_column='city', max_length=128)
    p_birthday = models.DateField(db_column='birthday')
    author = models.CharField(db_column='author', max_length=512, default='System')

    class Meta:
        db_table = 'extworkers_data'
        managed = False
        ordering = ['enterprise', 'dts']

    def __str__(self):
        return self.person_name


class ExtWorkerRecordHistory(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4(), db_column='guid')
    data_guid = models.CharField(max_length=64, editable=False, db_column='data_guid')
    change_time = models.DateTimeField(auto_now_add=True, db_column='change_time')
    action = models.CharField(max_length=64, default='Добавление', db_column='action')
    enterprise_guid = models.CharField(max_length=64, db_column='enterprise_guid')
    dts = models.DateField(db_column='dts')
    person_name = models.CharField(db_column='person_name', max_length=128)
    f_time = models.TimeField(db_column='f_time')
    t_time = models.TimeField(db_column='t_time')
    p_city = models.CharField(db_column='city', max_length=128)
    p_birthday = models.DateField(db_column='birthday')
    author = models.CharField(db_column='author', max_length=512, default='System')

    class Meta:
        db_table = 'extworkers_data_history'
        managed = False
