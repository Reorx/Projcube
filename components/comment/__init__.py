from components.noti import noti_signal
from models import Comment

def get_comments(master):
    qs = Comment.objects.filter(master_type=master.type, master_uid=master.uid)
    data = [i.stdout() for i in qs.order_by('created_time')]
    return data

def create_comment(master, creator, content):
    cmt = Comment(
        master_type = master.type,
        master_uid = master.uid,
        creator = creator,
        content = content
    )
    cmt.save()
    
    # after save, send signal
    print 'send signal'
    noti_signal.send(sender=Comment,
            owner = master.creator,
            user = creator,
            obj = cmt,
            ref = master)
