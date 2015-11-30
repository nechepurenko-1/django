# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


def students_list(request):
	students = (
		{'id' : 1,
		'first_name': 'Віталій',
		'last_name': 'Подоба',
		'ticket': 235,
		'image': 'img/1.jpeg'},
		{'id' : 2,
		'first_name': u'Андрій',
		'last_name': u'Корост',
		'ticket': 2123,
		'image': 'img/2.jpeg'},
		{'id' : 3,
		'first_name': u'Тарас',
		'last_name': u'Притула',
		'ticket': 5332,
		'image': 'img/3.jpg'}
	)
        return render(request, 'students/students_list.html',
	    {'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' %sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' %sid)



def groups_list(request):
	return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' %gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' %gid)
# Create your views here.
