from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.v_home),

    #(r'^projects$', views.v_projects),
    (r'^projects/create$', views.v_projects_create),
    (r'^projects/(?P<id>\d+)/switch$', views.v_projects_switch),
    (r'^projects/(?P<id>\d+)/members$', views.v_projects_members),
    #(r'^projects/(?P<c>\w+)/settings$', views.v_projects_settings),
    (r'^projects/ajax$', views.v_projects_ajax),

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
