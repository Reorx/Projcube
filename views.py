from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import config

from utils.viewsbase import render_tpl, render_api, ApiBaseError,\
        get_rsrc, check_params

from proj.models import Proj, ProjMembership,\
        Task, Daysum
from proj import forms

from components import comment as _comment_

COOKIE_CONTEXT_KEY = 'context_proj_id'

def change_context(resp, context):
    resp.set_cookie(COOKIE_CONTEXT_KEY, context.id,
            max_age = 60*60*24*7 )

@login_required
def v_home(req, tpl='home.html'):
    user = req.user

    context_id = req.COOKIES.get('context_proj_id')
    if context_id:
        context_id = int(context_id)
        try:
            context = user.in_projs.get(id=context_id)
        except:
            context = None
        if context:
            resp = render_tpl(req, tpl)
            change_context(resp, context)
            return resp

    return HttpResponseRedirect('/context')

def v_context(req, tpl='context.html'):
    user = req.user
    if 'POST' == req.method:
        pass
    else:
        cdic = {
            'in_projs': user.in_projs.all()
        }
        return render_tpl(req, tpl, cdic)

def v_user(req):
    pass

def v_user_projs(req):
    pass

def v_user_tasks(req):
    pass

def v_projs(req, tpl='projs.html'):
    user = req.user
    cdic = {
        'in_projs': user.in_projs.all(),
        'own_projs': user.own_projs.all()
    }
    return render_tpl(req, tpl, cdic)

def v_projs_create(req, tpl='projs_create.html'):
    cdic = {}
    if 'POST' == req.method:
        form = forms.ProjForm(user=req.user, data=req.POST)
        if not form.is_valid():
            raise ApiBaseError(400, 'Form Data Error')
        form.save()
        return HttpResponseRedirect('/')
    else:
        cdic['form'] = forms.ProjForm()
        return render_tpl(req, tpl, cdic)

def v_projs_join(req, tpl='projs_join.html'):
    if 'POST' == req.method:
        try:
            proj = Proj.objects.get(name = req.POST['name'])
        except:
            raise ApiBaseError(400)
        pass
    else:
        cdic = {}
        cdic['projs'] = Proj.objects.all()
        return render_tpl(req, tpl, cdic)

def v_projs_switch(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

@login_required
def v_projs_members(req, id, tpl='projs_members.html'):
    cdic = {}
    p = Proj.by_id(id)
    if not p:
        return ApiBaseError(404)
    cdic['members'] = p.members.all()
    return render_tpl(req, tpl, cdic)

def v_projs_settings(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_projs_ajax(req):
    # NOTE ??
    if False:
        try:
            user_is_creator = int(req.GET.get('is_creator'))
        except:
            raise ApiBaseError(400, 'param error')
    user = req.user

    data = [i.stdout() for i in user.in_projs.all()]

    return render_api(data)

@get_rsrc('proj.Proj', 'proj_id')
def v_projs_ajax_show(req):
    return render_api(req._target.stdout())

def v_tasks(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

@get_rsrc('proj.Proj', 'proj_id')
def v_tasks_ajax(req):
    opts = {
        'people': req.GET.get('people') or 'me',
        'status': int(req.GET.get('status')) or 0
    }

    user = req.user
    proj = req._target

    if 'me' == opts['people']:
        Q0 = Q(creator = user)
    elif 'others' == opts['people']:
        Q0 = ~Q(creator = user)
    else:
        Q0 = Q()

    if 2 == opts['status']:
        Q1 = Q()
    else:
        Q1 = Q(is_done = opts['status'])

    qs = proj.tasks.filter(Q0, Q1)
    data = [i.stdout() for i in qs.order_by('-created_time')]

    return render_api(data)

@login_required
@get_rsrc('proj.Task', 'task_id')
def v_tasks_ajax_show(req):
    task = req._target
    data = task.stdout()
    data['comments'] = _comment_.get_comments(task)
    return render_api(data)

@login_required
def v_tasks_ajax_create(req):
    print req.POST
    form = forms.TaskForm(user=req.user, data=req.POST.copy())
    if not form.is_valid():
        print form.errors
        raise ApiBaseError(400, 'Bad Data')
    task = form.save()
    return render_api(task.stdout())

@login_required
@get_rsrc('proj.Task', 'task_id')
def v_tasks_ajax_update(req):
    task = req._target
    task.content = req.POST['content']
    task.save()
    return render_api(task.stdout())

@login_required
@get_rsrc('proj.Task', 'task_id')
def v_tasks_ajax_delete(req):
    task = req._target
    task.delete()
    return render_api({})

@login_required
@get_rsrc('proj.Task', 'task_id')
def v_tasks_ajax_commenton(req):
    print req.POST
    _comment_.create_comment(req._target, req.user, req.POST['content'])
    return render_api({'msg': 'OK'})

@login_required
@get_rsrc('proj.Task', 'task_id')
def v_tasks_ajax_done(req):
    task = req._target
    if task.is_done:
        raise ApiBaseError(400)
    task.done()
    return render_api({})

@get_rsrc('proj.Task', 'task_id')
def v_tasks_ajax_undone(req):
    task = req._target
    if not task.is_done:
        raise ApiBaseError(400)
    task.undone()
    return render_api({})

def v_daysums(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_daysums_weekly(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_daysums_periodly(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_messages(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_messages_sent(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_messages_received(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_settings(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

