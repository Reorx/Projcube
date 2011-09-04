from django.db.models.base import Model
from django.db.models import *
from django.contrib.auth.models import User

from utils.timer import get_time_delta

from base.models import BaseRModel

class Proj(BaseRModel):
    creator = ForeignKey(User, related_name='own_projs')
    name = CharField(max_length=64)
    description = CharField(max_length=256)
    members = ManyToManyField(User, related_name='in_projs', through='ProjMembership')

    def __unicode__(self):
        return self.name

    def judge_membership(self, user):
        if user in self.members.all():
            return True
        else:
            return False

    def stdout(self):
        data = super(Proj, self).stdout()
        #data.update()

        return data

class ProjMembership(Model):
    user = ForeignKey(User)
    proj = ForeignKey(Proj)
    #is_manager = BooleanField(default=False) # NOTE no need, creator is the only ?

class Task(BaseRModel):
    creator = ForeignKey(User, related_name='tasks')
    proj = ForeignKey(Proj, related_name='tasks')
    content = CharField(max_length=256)

    is_done = IntegerField(default=0)

    def __unicode__(self):
        return self.content[10:]

    def stdout(self):
        import datetime
        data = super(Task, self).stdout(['content'])
        data.update(
            time_delta = get_time_delta(data['created_time'],
                datetime.datetime.now()),
            status = self.is_done
            #proj = self.proj.stdout()
        )
        return data

class Daysum(BaseRModel):
    creator = ForeignKey(User, related_name='daysums')
    content = CharField(max_length=512)

    def __unicode__(self):
        return content[10:]

#class Note(BaseRModel):
    #user = ForeignKey(User, related_name='notes')
    #content = CharField(max_length=512)

    #def __unicode__(self):
        #return content[10:]
