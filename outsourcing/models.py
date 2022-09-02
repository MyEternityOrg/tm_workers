import datetime

from django.contrib.auth.models import User
from django.db import models
import uuid


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

    @staticmethod
    def active_divisions():
        return Enterprises.objects.raw(
            'select * from enterprises where guid in (select pdb_guid from [get_enterprise_workstatus] (%s, null) where activity = 1) order by enterprise_code',
            [datetime.datetime.today()])

    @classmethod
    def get_list_shops(cls):
        return cls.objects.filter(guid__in=[x.guid for x in cls.active_divisions()])


class OutsourcingTypes(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'outsourcing_types'
        managed = False


class OutsourcingContractors(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    name = models.CharField(max_length=256)
    inn = models.CharField(max_length=64)
    kpp = models.CharField(max_length=64)
    outsourcing_type = models.ForeignKey(OutsourcingTypes, db_column='outsourcing_type', on_delete=models.DO_NOTHING)
    marked = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'outsourcing_contractors'
        managed = False


class OutsourcingTimeline(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    name = models.CharField(max_length=128)
    outsourcing_type = models.ForeignKey(OutsourcingTypes, db_column='outsourcing_type', on_delete=models.DO_NOTHING)
    marked = models.IntegerField(default=0)

    class Meta:
        db_table = 'outsourcing_timeline'
        managed = False


class OutsourcingTimelineData(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    dts = models.DateField(db_column='dts')
    outsourcing_timeline = models.ForeignKey(OutsourcingTimeline, db_column='outsourcing_timeline',
                                             on_delete=models.CASCADE)
    hours = models.IntegerField()
    f_time = models.TimeField(db_column='f_time', default=datetime.time(0, 0, 0))
    t_time = models.TimeField(db_column='t_time', default=datetime.time(23, 59, 59))

    class Meta:
        db_table = 'outsourcing_timeline_data'
        managed = False


class OutsourcingDataP(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    dts = models.DateField(db_column='dts')
    outsourcing_contractor = models.ForeignKey(OutsourcingContractors, db_column='outsourcing_contractor',
                                               on_delete=models.CASCADE)
    outsourcing_timeline = models.ForeignKey(OutsourcingTimeline, db_column='outsourcing_timeline',
                                             on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise', on_delete=models.CASCADE)

    class Meta:
        db_table = 'outsourcing_data_p'
        managed = False


class OutsourcingPrices(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    dts = models.DateTimeField(db_column='dts')
    contractor = models.ForeignKey(OutsourcingContractors, db_column='contractor_guid', on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    price = models.FloatField(db_column='price')

    class Meta:
        db_table = 'outsourcing_prices'
        managed = False


class OutsourcingPPlanning(models.Model):
    Gender_Choices = [
        ('М', 'М'),
        ('Ж', 'Ж'),
        ('МЖ', 'МЖ'),
    ]

    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    dts = models.DateTimeField(db_column='dts')
    contractor = models.ForeignKey(OutsourcingContractors, db_column='contractor_guid', on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    amount = models.IntegerField(db_column='amount')
    gender = models.CharField(choices=Gender_Choices, max_length=32, db_column='gender', default='M', blank=False)

    class Meta:
        db_table = 'outsourcing_pplanning'
        managed = False
