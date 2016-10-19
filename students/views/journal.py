# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
def journal(request):
	journal_students = (
		{'id' : 1,
		'name': u'Подоба Віталій'},
		{'id' : 2,
		'name': u'Корост Андрій'},
		{'id' : 3,
		'name': u'Притула Тарас'}

	)
	return render(request, 'students/journal.html',
	    {"journal_students": journal_students})

def journal_edit(request, gid):
	return HttpResponse('<h1>Edit journal %s</h1>' %gid)