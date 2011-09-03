from django.db.models import get_model
from utils.errors import ApiBaseError

class rsrc(object):
    def __init__(self, model):
        if isinstance(model, str):
            self.model = get_model(*model.split('.'))
        else:
            self.model = model

    def get(self, id):
        try:
            target = self.model.objects.get(id=id)
        except:
            raise ApiBaseError(404)
        return target
