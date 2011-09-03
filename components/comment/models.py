from django.db.models.base import Model
from django.db.models import *

from base.models import BaseRModel

from django.contrib.auth.models import User

class Comment(BaseRModel):
    """
    to avoid conflicts caused by 'id' change, mostly happened when Task is reseted,
    use 'uid' instead of 'id'
    """
    master_type = CharField(max_length=16)
    master_uid = CharField(max_length=32)
    creator = ForeignKey(User)
    content = CharField(max_length=1024)

    def __unicode__(self):
        return self.content[:20]

    def stdout(self):
        data = super(Comment, self).stdout(['content'])
        return data
