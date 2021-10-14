import datetime

from django.db import models


# Create your models here.
class Enterprises(models.Model):
    guid = models.CharField(primary_key=True, unique=True, max_length=64, db_column='guid')
    name = models.CharField(max_length=400, db_column='name')
    enterprise_code = models.IntegerField(db_column='enterprise_code')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'enterprises'
        managed = False
        ordering = ['enterprise_code']

    def get_list_shops(self):
        return Enterprises.objects.filter(enterprise_code__gte=3, enterprise_code__lte=999)


class ExtWorkerRecord(models.Model):
    guid = models.CharField(primary_key=True, unique=True, max_length=64, db_column='guid')
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    dts = models.DateField(db_column='dts')
    person_name = models.CharField(db_column='person_name', max_length=128)
    f_time = models.TimeField(db_column='f_time')
    t_time = models.TimeField(db_column='t_time')
    duration = models.IntegerField(db_column='duration', default=0)

    class Meta:
        db_table = 'extworkers_data'
        ordering = ['enterprise', 'dts']
