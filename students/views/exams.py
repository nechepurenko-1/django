# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView, CreateView, UpdateView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from crispy_forms.layout import Submit
from django.contrib import messages



from ..models.exams import Exam



def exam_list(request):
	exams = Exam.objects.all()
	order_by = request.GET.get('order_by','')
	if order_by in ('title','date_exam','teacher','group','id'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
	else:
	    exams = exams.order_by('title')

	# paginate students
	paginator = Paginator(exams, 3)
	page = request.GET.get('page')

	try:
		exams = paginator.page(page)

	except PageNotAnInteger:
		# if page not an integer, delliver first page
		exams = paginator.page(1)

	except EmptyPage:
		#if page is out of range(e.g. 9999) , deliver last page of result
		exams = paginator.page(paginator.num_pages)




	return render(request, 'students/exams_list.html',
				  {'exams': exams})

class ExamsAddForm(ModelForm):
    class Meta:
        model = Exam

    def __init__(self, *args, **kwargs):
        super(ExamsAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('exams_add_form')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        self.helper.add_input(Submit('save_button', u'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-link'))


class ExamsAddView(CreateView):
    model = Exam
    template_name = 'students/exams_form.html'
    form_class = ExamsAddForm



    def get_success_url(self):
        messages.success(self.request, u'Екзамен успішно збережено!')
        return reverse('exams')


    def get_context_data(self, **kwargs):
        context = super(ExamsAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання екзамену'
        return context



    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Додавання екзамену відмінено!')
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamsAddView, self).post(request,*args,**kwargs)


def exams_add(request):
	return HttpResponse('<h1>Exams Add Form</h1>')




def exams_edit(request, eid):
	return HttpResponse('<h1>Edit Exam %s</h1>' %eid)

class ExamsUpdateForm(ModelForm):
    class Meta:
        model = Exam
    def __init__(self, *args, **kwargs):
        super(ExamsUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('exams_edit',kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons

        self.helper.add_input(Submit('save_button', u'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-link'))
        # self.helper.layout.fields.append(FormActions(
        # Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
        # Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        # ))


class ExamsUpdateView(UpdateView):
    model = Exam
    template_name = 'students/exams_form.html'
    form_class = ExamsUpdateForm



    def get_success_url(self):
        messages.success(self.request, u'Групу успішно збережено!')
        return reverse('exams')

    def get_context_data(self, **kwargs):
        context = super(ExamsUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування групи'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Редагування групи відмінено!')

            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamsUpdateView, self).post(request,*args,**kwargs)



class ExamsDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Екзамен успішно видалено!' )
        return reverse('exams')


def exams_delete(request, eid):
    try:
        exam = Exam.objects.get(pk=eid)
    # import pdb;pdb.set_trace()
    except:
        messages.error(request, 'Даного екзамена не існує.')
        return HttpResponseRedirect(reverse('exams'))

    if request.method == "POST":

        if request.POST.get('confirm_button') is not None:
            exam.delete()
            messages.success(request, "Успішно видалено екзамен: %s." % exam)
            return HttpResponseRedirect(reverse('exams'))
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, "Видалення екзамену скасовано.")
            return HttpResponseRedirect(reverse('exams'))
        else:
            messages.error(request, "Упс! Щось пішло не так. Повторіть спробу пізніше.")
            return HttpResponseRedirect(reverse('exams'))
    else:
        return render(request,'students/exams_delete_hand.html',{'exam':exam})