from django.contrib.auth.models import User
from django.db import models

from extworkers.models import Enterprises


# Create your models here.
class ProfileUser(models.Model):
    user_id = models.IntegerField(db_column='user_id', primary_key=True)
    ent_guid = models.CharField(max_length=64, db_column='entreprise_id', null=True, blank=True)
    ip_shop = models.CharField(max_length=30, db_column='ip_shop', blank=True)

    def __str__(self):
        return str({'id': self.user_id, 'ent': self.ent_guid, 'ip': self.ip_shop})

    @classmethod
    def get_profile_by_user_ip(cls, ip):
        try:
            __ip = '.'.join(str(ip).split('.')[0:3]) + '.'
            if __ip == '127.0.0.':
                return None
                #return ProfileUser.objects.get(user_id=2)
            else:
                return ProfileUser.objects.filter(ip_shop__contains=__ip).first()
        except Exception as E:
            print('Model ProfileUsers, parse IP exc: ', E)
            return None

    @classmethod
    def get_profile_by_user_id(cls, user_id):
        return ProfileUser.objects.get(user_id=user_id)

    class Meta:
        db_table = 'TimeSheet_profileuser'
        managed = False
