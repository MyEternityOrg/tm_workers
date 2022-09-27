import uuid

from django.contrib.auth.models import User
from django.db import models

from outsourcing.models import Enterprises, OutsourcingContractors, OutsourcingTimeline



class CleaningPlan(models.Model):

    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    dts = models.DateField(db_column='dts')
    contractor = models.ForeignKey(OutsourcingContractors, db_column='contractor_guid', on_delete=models.CASCADE)
    sheduler = models.ForeignKey(OutsourcingTimeline, db_column='sheduler_guid', on_delete=models.CASCADE)
    plan_hours = models.IntegerField(db_column='plan_hours')


    class Meta:
        db_table = 'cleaning_data_plan'
        managed = False


class CleaningFact(models.Model):

    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid')
    enterprise = models.ForeignKey(Enterprises, db_column='enterprise_guid', on_delete=models.CASCADE)
    dts = models.DateField(db_column='dts')
    fact_hours = models.IntegerField(db_column='fact_hours', default=0)


    class Meta:
        db_table = 'cleaning_data_fact'
        managed = False
