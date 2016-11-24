# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student
from ..models.groups import Group
from datetime import datetime
from PIL import Image
from django.contrib import messages
from django import forms
from django.views.generic import UpdateView, CreateView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse_lazy


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
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # TODO: validate input from user
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім`я є обов`язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов’язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов’язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] ='Введіть коректний формат дати(напр.1984-12-30)'
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов’язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', "").strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                if photo.name.split(".")[-1].lower() not in ('jpg', 'jpeg', 'png', 'gif'):
                    errors['photo'] = u"Файл має бути одного з наступних типів: jpg, jpeg, png, gif"
                else:
                    try:
                        Image.open(photo)
                    except Exception:
                        errors['photo'] = u"Завантажений файл не є файлом зображення або пошкоджений"
                    else:
                        if photo.size > 2 * 1024 * 1024:
                            errors['photo'] = u"Фото занадто велике (розмір файлу має бути менше 2Мб)"
                        else:
                            data['photo'] = photo

            if not errors:
                # create student object
                student = Student(**data)
                # save it to database
                student.save()
                # redirect user to students list
                messages.success(request, u'Студента %s %s %s успішно додано!' %
                                 (data['first_name'],data['middle_name'],data['last_name']))
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                messages.error(request,u'Виправте наступні помилки!')
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.warning(request,u'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                        {'groups': Group.objects.all().order_by('title')})

# def students_edit(request, sid):
#     return render(request, 'students/student_edit.html')

class StudentAddForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('students_add_form')
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


class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_form.html'
    form_class = StudentAddForm



    def get_success_url(self):
        messages.success(self.request, u'Студента успішно збережено!')
        return reverse('home')


    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання студента'
        return context



    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Додавання студента відмінено!')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return super(StudentAddView, self).post(request,*args,**kwargs)






class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('students_edit',kwargs={'pk': kwargs['instance'].id})
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


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_form.html'
    form_class = StudentUpdateForm



    def get_success_url(self):
        messages.success(self.request, u'Студента успішно збережено!')
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування студента'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Редагування студента відмінено!')

            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request,*args,**kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Студента успішно видалено!' )
        return reverse('home')


# def students_edit(request, sid):
# 	return HttpResponse('<h1>Edit Student %s</h1>' %sid)

def students_delete(request, sid):
    try:
        student = Student.objects.get(pk=sid)
    # import pdb;pdb.set_trace()
    except:
        messages.error(request, 'Даного студента не існує.')
        return HttpResponseRedirect(reverse('home'))

    if request.method == "POST":

        if request.POST.get('confirm_button') is not None:
            student = Student.objects.get(pk=sid)
            student.delete()
            messages.success(request, "Успішно видалено: %s." % student)
            return HttpResponseRedirect(reverse('home'))
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, "Видалення студента скасовано.")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, "Упс! Щось пішло не так. Повторіть спробу пізніше.")
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,
                      'students/students_delete_hand.html',{'student':student })



