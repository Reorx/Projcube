from django.dispatch import Signal

# import all related model
from proj.models import Proj, Task
from components.comment.models import Comment
from models import Noti

NOTI_CONTENT_TPL = '%(username)s has %(action)s a $(obj_type)s $(extra)s'

def activity_receiver(owner, user, obj, ref, **kwargs):
    print 'received!'
    noti = Noti(
        owner = owner,
        obj_type = obj.type,
        obj_uid = obj.uid,
        user_username = user.username,
        user_id = user.id,
        ref_type = ref.type,
        ref_uid = ref.uid
    )
    cdic = {
        'username': user.username
    }
    if isinstance(obj, Comment):
        cdic['action'] = 'make'
        cdic['obj_type'] = 'comment'
        # TODO def type2display
        cdic['extra'] = 'on %s #%s' % (ref.type, ref.id) 

        noti.quote = obj.content[:250]

    noti.content = NOTI_CONTENT_TPL % cdic
    noti.save()

noti_signal = Signal(providing_args=['owner', 'user', 'obj', 'ref'])
noti_signal.connect(activity_receiver)
