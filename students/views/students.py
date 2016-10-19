# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Student


def students_list(request):
	students = Student.objects.all()
	#try to order srudents list
	order_by = request.GET.get('order_by','')
	if order_by in ('last_name','first_name','ticket', 'id','student_group'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
	    students = students.order_by('last_name')

	# paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page')

	try:
		students = paginator.page(page)

	except PageNotAnInteger:
		# if page not an integer, delliver first page
		students = paginator.page(1)

	except EmptyPage:
		#if page is out of range(e.g. 9999) , deliver last page of result
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html',
		{'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return render(request, 'students/student_edit.html')


# def students_edit(request, sid):
# 	return HttpResponse('<h1>Edit Student %s</h1>' %sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' %sid)

