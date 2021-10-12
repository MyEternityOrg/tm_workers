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
    enterprise_guid = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    dts = models.DateField(db_column='dts', auto_now_add=True)
    person_name = models.CharField(db_column='person_name', max_length=128)
    person_birth_day = models.DateField(db_column='person_birthd')
    person_birth_place = models.CharField(db_column='person_birthp', max_length=128, default='')
    time_start = models.TimeField(db_column='time_start', default=datetime.time)
    time_stop = models.TimeField(db_column='time_stop')
    duration = models.IntegerField(db_column='duration', default=0)
    contractor_name = models.CharField(db_column='contractor_name', default='ООО "Рога и Копыта"', max_length=50)

    class Meta:
        db_table = 'extworkers_data'
        managed = False
        ordering = ['enterprise_guid', 'dts']
