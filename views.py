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

@login_required
def v_home(req, tpl='home.html'):
    user = req.user

    if not user.in_projs.all():
        tpl = 'no_context.html'
        return render_tpl(req, tpl)
    else:
        cdic = {
            'context': None,
            'tasks': None,
            'notes': None
        }
        # get context
        try:
            cdic['context'] = user.in_projs.get(id=req.COOKIES['context_proj_id'])
        except:
            try:
                cdic['context'] = user.in_projs.all()[0]
            except:
                pass

        # get tasks
        if cdic['context']:
            cdic['tasks'] = cdic['context'].tasks.all().order_by('-created_time')

        # get notes

        resp = render_tpl(req, tpl, cdic)
        if cdic['context']:
            resp.set_cookie(COOKIE_CONTEXT_KEY, cdic['context'].id)

        return resp

def v_projs_create(req, tpl='proj_create.html'):
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

def v_projs_switch(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

@login_required
def v_projs_members(req, id, tpl='proj_members.html'):
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
def v_tasks_ajax_commenton(req):
    print req.POST
    _comment_.create_comment(req._target, req.user, req.POST['content'])
    return render_api({'msg': 'OK'})

def v_tasks_undone(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

def v_tasks_done(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

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

