"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
from students.views.contact_admin import ContactView
from students.views.students import  StudentUpdateView, StudentAddView, StudentDeleteView
from students.views.groups import  GroupDeleteView ,GroupUpdateView, GroupAddView
from students.views.exams import ExamsDeleteView, ExamsAddView, ExamsUpdateView


urlpatterns = patterns('',
                       url(r'^$','students.views.students.students_list',name='home'),
                       url(r'^students/add/$','students.views.students.students_add',name='students_add'),
                       url(r'^students/add_form/$',StudentAddView.as_view(),name='students_add_form'),

                       url(r'^students/(?P<sid>\d+)/edit_hand/$','students.views.students.students_edit_hand',name='students_edit_hand'),
                       url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),name='students_edit'),
                       url(r'^students/(?P<pk>\d+)/delete/$',StudentDeleteView.as_view(),name='students_delete'),
                       url(r'^students/(?P<sid>\d+)/delete_hand/$','students.views.students.students_delete',name='students_delete_hand'),

					   url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
                       url(r'^groups/add/$','students.views.groups.groups_add',name='groups_add'),
                       url(r'^groups/add_form/$',GroupAddView.as_view(),name='groups_add_form'),
                       url(r'^groups/(?P<pk>\d+)/edit/$',GroupUpdateView.as_view() ,name='groups_edit'),
                       url(r'^groups/(?P<gid>\d+)/edit_hand/$','students.views.groups.groups_edit',name='groups_edit_hand'),
                       url(r'^groups/(?P<pk>\d+)/delete/$',GroupDeleteView.as_view(),name='groups_delete'),
                       url(r'^groups/(?P<gid>\d+)/delete_hand/$','students.views.groups.groups_delete',name='groups_delete_hand'),

					   url(r'^admin/', include(admin.site.urls)),

                       url(r'^journal/$', 'students.views.journal.journal', name='journal'),
                       url(r'^journal/(?P<gid>\d+)/edit/$', 'students.views.journal.journal_edit', name='journal_edit'),

                       url(r'^exams/$', 'students.views.exams.exam_list', name='exams'),
                       url(r'^exams/add_form/$',ExamsAddView.as_view(),name='exams_add_form'),
                       url(r'^exams/add/$','students.views.exams.exams_add',name='exams_add'),
                       url(r'^exams/(?P<eid>\d+)/edit_hand/$','students.views.exams.exams_edit_hand',name='exams_edit_hand'),
                       url(r'^exams/(?P<pk>\d+)/edit/$',ExamsUpdateView.as_view(),name='exams_edit'),
                       url(r'^exams/(?P<pk>\d+)/delete/$', ExamsDeleteView.as_view(), name='exams_delete'),
                       url(r'^exams/(?P<eid>\d+)/delete_hand/$','students.views.exams.exams_delete',name='exams_delete_hand'),
                       url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),
                       )

if DEBUG:
    #serve files from media folder
    urlpatterns += patterns('',url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
