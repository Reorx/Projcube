from django.db.models.base import Model
from django.db.models import *
from django.contrib.auth.models import User

from base.models import BaseRModel

class Msg(BaseRModel):
    from_user = ForeignKey(User, related_name='sent_msgs')
    to_users = ManyToManyField(User, related_name='received_msgs')
    content = CharField(max_length=256)

    def __unicode__(self):
        return self.content[:10]
