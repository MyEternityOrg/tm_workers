from django.contrib.auth.models import User
from django.db import models

from extworkers.models import Enterprises


# Create your models here.
class ProfileUser(models.Model):
    user_id = models.IntegerField(db_column='user_id', primary_key=True)
    ent_guid = models.CharField(max_length=64, db_column='entreprise_id', null=True, blank=True)
    ip_shop = models.CharField(max_length=30, db_column='ip_shop', blank=True)

    def __str__(self):
        return str([self.user_id, self.ent_guid, self.ip_shop])

    class Meta:
        db_table = 'TimeSheet_profileuser'
        managed = False
