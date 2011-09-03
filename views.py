from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import config

from utils.viewsbase import render_tpl, render_api, ApiBaseError,\
        get_rsrc, check_params

from proj.models import Proj, ProjMembership,\
        Task, Daysum
from proj import forms

COOKIE_CONTEXT_KEY = 'context_proj_id'

@login_required
def v_home(req, tpl='home.html'):
    cdic = {
        'context': None,
        'tasks': None,
        'notes': None
    }
    user = req.user
    # get context
    try:
        cdic['context'] = user.projs.get(id=req.COOKIES['context_proj_id'])
    except:
        try:
            cdic['context'] = user.projs.all()[0]
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

    data = [i.stdout() for i in user.projs.all()]

    return render_api(data)

def v_tasks(req, tpl='.html'):
    cdic = {}
    return render_tpl(req, tpl, cdic)

@check_params(['proj_id', 'mode'])
@get_rsrc('proj.Proj', 'proj_id')
def v_tasks_ajax(req):
    try:
        mode = int(req.GET['mode'])
    except:
        raise ApiBaseError(400, 'Mode Expect to be number')

    user = req.user
    target = req._target
    if 0 == mode:
        qs = target.tasks.all();
    elif 1 == mode:
        qs = target.tasks.filter(creator=user)
    elif 2 == mode:
        qs = target.tasks.exclude(creator=user)
    else:
        raise ApiBaseError(400, 'Params Not Validate')

    data = [i.stdout() for i in qs.order_by('-created_time')]

    return render_api(data)

@login_required
def v_tasks_ajax_create(req):
    print req.POST
    form = forms.TaskForm(user=req.user, data=req.POST.copy())
    if not form.is_valid():
        raise ApiBaseError(400, 'Bad Data')
    task = form.save()
    return render_api(task.stdout())

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

