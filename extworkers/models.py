import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Enterprises(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    name = models.CharField(max_length=400, db_column='name')
    enterprise_code = models.IntegerField(db_column='enterprise_code')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'enterprises'
        managed = False
        ordering = ['enterprise_code']

    @classmethod
    def get_list_shops(cls):
        return cls.objects.filter(enterprise_code__gte=3, enterprise_code__lte=999)


class ExtWorkerRecord(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='guid')
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    dts = models.DateField(db_column='dts', auto_now_add=True)
    person_name = models.CharField(db_column='person_name', max_length=128)
    f_time = models.TimeField(db_column='f_time')
    t_time = models.TimeField(db_column='t_time')

    class Meta:
        db_table = 'extworkers_data'
        managed = False
        ordering = ['enterprise', 'dts']

    def __str__(self):
        return self.person_name
