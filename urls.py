from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.v_home),

    #(r'^projs$', views.v_projs),
    (r'^projs/create$', views.v_projs_create),
    (r'^projs/(?P<id>\d+)/switch$', views.v_projs_switch),
    (r'^projs/(?P<id>\d+)/members$', views.v_projs_members),
    #(r'^projs/(?P<c>\w+)/settings$', views.v_projs_settings),
    (r'^projs/ajax$', views.v_projs_ajax),

    (r'^tasks$', views.v_tasks),
    #(r'^tasks/undone$', views.v_tasks_undone),
    #(r'^tasks/done$', views.v_tasks_done),

    (r'^tasks/ajax$', views.v_tasks_ajax),
    (r'^tasks/ajax/create$', views.v_tasks_ajax_create),

    (r'^daysums$', views.v_daysums),
    #(r'^daysums/weekly$', views.v_daysums_weekly),
    #(r'^daysums/periodly$', views.v_daysums_periodly),

    (r'^messages$', views.v_messages),
    #(r'^messages/sent$', views.v_messages_sent),
    #(r'^messages/received$', views.v_messages_received),

    #(r'^settings$', views.v_settings),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^accounts/signup/$', 'account.signup'),
)


# admin
if False:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        (r'^admin/',include(admin.site.urls)),
    )

# enable static server in debug mode
from settings import DEBUG, MEDIA_ROOT
if DEBUG:
    urlpatterns += patterns( '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT
        }),
    )
