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
from datetime import datetime


from ..models.exams import Exam
from ..models.groups import Group



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
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}
            data = {}


            group = request.POST.get('group', "").strip()
            if group:
                groups = Group.objects.filter(pk=int(group))
                if len(groups) != 1:
                    errors['group'] = u"Оберіть коректну групу"
                else:
                    data['group'] = groups[0]
            else:
                errors['group'] = u"Група є обов'язковою."

            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва є обов'язковою."
            else:
                data['title'] = title

            teacher = request.POST.get('teacher', '').strip()
            if not teacher:
                errors['teacher'] = u"Викладач є обов’язковим"
            else:
                data['teacher'] = teacher

            date_exam = request.POST.get('date_exam', '').strip()
            if not date_exam:
                errors['date_exam'] = u"Дата екзамену є обов’язковою"
            else:
                try:
                    datetime.strptime(date_exam, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    errors['date_exam'] ='Введіть коректний формат дати(напр.1984-12-30 12:30:00)'
                else:
                    data['date_exam'] = date_exam

            if not errors:
                exam = Exam(**data)
                exam.save()
                messages.success(request, u'Екзамен %s успішно додано!' %(data['title']))
                return HttpResponseRedirect(reverse('exams'))
            else:
                # render form with errors and previous user input
                messages.error(request,u'Виправте наступні помилки!')
                return render(request, 'students/exams_add.html',
                    {'groups': Group.objects.all().order_by('title'),'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.warning(request,u'Додавання екзамну скасовано!')
            return HttpResponseRedirect(reverse('exams'))
    else:
        # initial form render
        return render(request, 'students/exams_add.html',
                        {'groups': Group.objects.all().order_by('title')})



def exams_edit_hand(request, eid):
    exams = Exam.objects.filter(pk=eid)
    groups = Group.objects.all()

    if len(exams) !=1:
        messages.error(request, 'Обраного екзамену не існує')
        return HttpResponseRedirect(reverse('exams'))
    else:
        if request.method == "POST":
            exam = Exam.objects.get(pk=eid)
            if request.POST.get('save_button') is not None:

                errors = {}
                title = request.POST.get('title', '').strip()
                if not title:
                    errors['title'] = u"Імʼя є обовʼязковим."
                else:
                    exam.title = title


                date_exam = request.POST.get('date_exam', '').strip()
                if not date_exam:
                        errors['date_exam'] = u"Дата екзамену є обов’язковою"
                else:
                    try:
                        datetime.strptime(date_exam, '%Y-%m-%d %H:%M:%S')
                    except Exception:
                        errors['date_exam'] ='Введіть коректний формат дати(напр.1984-12-30 12:30:00)'
                    else:
                        exam.date_exam = date_exam

                teacher = request.POST.get('teacher', '').strip()
                if not teacher:
                    errors['teacher'] = u"Викладач є обов’язковим"
                else:
                    exam.teacher = teacher


                group = request.POST.get('group', '').strip()
                if not group:
                    errors['group'] = u"Група є обовʼязковою"
                else:
                    group = Group.objects.filter(pk=int(group))
                    if len(group) != 1:
                        errors['student_group'] = u"Оберіть коректну групу"
                    else:
                        exam.group = group[0]


                if errors:
                    messages.error(request,u'Виправте наступні помилки!')
                    return render(request, 'students/exams_edit_hand.html',
                                  {'groups': groups,'errors': errors,'exam':exam , 'pk':eid})
                else:
                    exam.save()
                    messages.success(request, u'Екзамен успішно збереженно!')
                    return HttpResponseRedirect(reverse('exams'))

            elif request.POST.get('cancel_button') is not None:
                messages.warning(request, 'Редагування екзамену скасовано.')
                return HttpResponseRedirect(reverse('exams'))
            else:
                messages.error(request, 'Упс! Щось пішло не так. Повторіть спробу пізніше.')
                return HttpResponseRedirect(reverse('exams'))
        else:
            return render(request,'students/exams_edit_hand.html',{'pk': eid, 'exam': exams[0],
                                                                   'groups': groups.order_by('title')})

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