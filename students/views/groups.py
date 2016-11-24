# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models.groups import Group

def groups_list(request):
	groups = Group.objects.all()
	order_by = request.GET.get('order_by','')
	if order_by in ('title','leader','id'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			groups = groups.reverse()
	else:
	    groups = groups.order_by('title')

	# paginate students
	paginator = Paginator(groups, 3)
	page = request.GET.get('page')

	try:
		groups = paginator.page(page)

	except PageNotAnInteger:
		# if page not an integer, delliver first page
		groups = paginator.page(1)

	except EmptyPage:
		#if page is out of range(e.g. 9999) , deliver last page of result
		groups = paginator.page(paginator.num_pages)




	return render(request, 'students/groups_list.html',
	    {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' %gid)

# def groups_delete(request, gid):
# 	return HttpResponse('<h1>Delete Group %s</h1>' %gid)

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Групу успішно видалено!' )
        return reverse('groups')
