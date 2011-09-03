from django.db.models.base import Model
from django.db.models import *

from utils import hashFN

class BaseRModel(Model):
    nid = CharField(max_length=10, null=True)
    md5id = CharField(max_length=32, null=True)
    created_time = DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return 'base resource model'
    class Meta:
        abstract = True

    @property
    def type(self):
        return '%s.%s' % (self._meta.app_label, self._meta.object_name)

    def set_nid(self):
        self.nid = hashFN.CreateNid(self.id)
    def set_md5id(self):
        s = str(time.time()) + self.__class__.__name__ + str(self.id)
        self.md5id = hashFN.Md5(s)

    def save(self, *args, **kwargs):
        print '%s save' % self.type
        if not self.id:
            print '1st save'
            super(BaseRModel, self).save(*args, **kwargs)
        if not self.nid or not self.md5id:
            print '2nd save'
            if not self.nid:
                self.set_nid()
            if not self.md5id:
                self.set_md5id()
        super(BaseRModel, self).save()

    @classmethod
    def by_nid(cls, nid):
        try:
            data = cls.objects.get(nid=nid)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return None
        return data

    @classmethod
    def by_id(cls, id):
        try:
            data = cls.objects.get(id=id)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return None
        return data

    def spout(self, fields):
        data = {}
        for i in fields:
            data[i] = self.__dict__.get(i)
        return data

    def stdout(self, fields=[]):
        data = {
            'type': self.type,
            'id': self.id,
            'md5id': self.md5id,
            'created_time': self.created_time
        }
        if hasattr(self, 'name'):
            data['name'] = self.name

        if hasattr(self, 'creator'):
            data.update(
                creator = dict(
                    username = self.creator.__dict__.get('username')
                )
            )

        for i in fields:
            data[i] = self.__dict__.get(i)
        return data
