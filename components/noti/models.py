from django.db.models.base import Model
from django.db.models import *

from base.models import BaseRModel

from django.contrib.auth.models import User

class Noti(BaseRModel):
    owner = ForeignKey(User)
    user_username = CharField(max_length=32)
    user_id = IntegerField()
    obj_type = CharField(max_length=16)
    obj_uid = CharField(max_length=32)
    ref_type = CharField(max_length=16)
    ref_uid = CharField(max_length=32)
    content = CharField(max_length=128)
    quote = CharField(max_length=256)

    def __unicode__(self):
        return self.content[:20]

    def stdout(self):
        data = super(Noti, self).stdout(['content'])
        return data

