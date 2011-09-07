from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.v_home),
    (r'^accounts/login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^accounts/logout$', 'accounts.logout'),
    (r'^accounts/signup$', 'accounts.signup'),
    #(r'^accounts/settings$', views.v_accounts_settings),

    (r'^context$', views.v_context),
)

urlpatterns += patterns('',
    (r'^projs$', views.v_projs),
    (r'^projs/create$', views.v_projs_create),
    (r'^projs/(?P<id>\d+)/switch$', views.v_projs_switch),
    (r'^projs/(?P<id>\d+)/members$', views.v_projs_members),
    #(r'^projs/(?P<c>\w+)/settings$', views.v_projs_settings),
    (r'^projs/ajax$', views.v_projs_ajax),
    (r'^projs/ajax/show$', views.v_projs_ajax_show),
)

urlpatterns += patterns('',
    (r'^tasks$', views.v_tasks),
    (r'^tasks/ajax$', views.v_tasks_ajax),
    (r'^tasks/ajax/show$', views.v_tasks_ajax_show),
    (r'^tasks/ajax/create$', views.v_tasks_ajax_create),
    (r'^tasks/ajax/commenton$', views.v_tasks_ajax_commenton),
    #(r'^tasks/undone$', views.v_tasks_undone),
    #(r'^tasks/done$', views.v_tasks_done),
)

urlpatterns += patterns('',
    (r'^daysums$', views.v_daysums),
    #(r'^daysums/weekly$', views.v_daysums_weekly),
    #(r'^daysums/periodly$', views.v_daysums_periodly),
)

urlpatterns += patterns('',
    (r'^messages$', views.v_messages),
    #(r'^messages/sent$', views.v_messages_sent),
    #(r'^messages/received$', views.v_messages_received),
)
