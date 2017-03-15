# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView, CreateView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.encoding import smart_str, smart_unicode

from ..models.groups import Group
from ..models.students import Student
from ..models.exams import Exam
from ..util import paginate, get_current_group

def groups_list(request):
    groups = []
    current_group = get_current_group(request)

    if current_group:
        groups.append(current_group)
    else:
        groups = Group.objects.all()
    order_by = request.GET.get('order_by','')
    if order_by in ('title','leader','id'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()


    # paginate students
    # paginator = Paginator(groups, 3)
    # page = request.GET.get('page')
    #
    # try:
    #     groups = paginator.page(page)
    #
    # except PageNotAnInteger:
    #     # if page not an integer, delliver first page
    #     groups = paginator.page(1)
    #
    # except EmptyPage:
    #     #if page is out of range(e.g. 9999) , deliver last page of result
    #     groups = paginator.page(paginator.num_pages)


    context = paginate(groups, 3, request, {}, var_name='groups')

    return render(request, 'students/groups_list.html',context)

def groups_add(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}
            data = {'notes': request.POST.get('notes')}
            title = request.POST.get('title', '').strip()

            if not title:
                errors['title'] = u"Назва є обов'язковою."
            else:
                groups = Group.objects.filter(title=title)
                if len(groups) > 0:
                    errors['title'] = u"Така група вже існує"
                else:
                    data['title'] = title

            leader = request.POST.get('leader', "").strip()
            if leader:
                student = Student.objects.filter(pk=int(leader))
                if len(student) != 1:
                    errors['leader'] = u"Оберіть коректного студента"
                else:
                    group_leader = Group.objects.filter(leader=student)
                    if len(group_leader) != 0:
                        errors['leader'] = u"Даний студент є старостою іншої групи"
                    elif student[0].student_group is not None:
                        errors['leader'] = u"Студент не належить до цієї групи"
                    else:
                        data['leader'] = student[0]

            if not errors:
                group = Group(**data)
                group.save()
                messages.success(request, u'Групу %s успішно додано!' %(data['title']))
                return HttpResponseRedirect(reverse('groups'))
            else:
                # render form with errors and previous user input
                messages.error(request,u'Виправте наступні помилки!')
                return render(request, 'students/groups_add.html',
                    {'students': Student.objects.all().order_by('first_name'),'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.warning(request,u'Додавання групи скасовано!')
            return HttpResponseRedirect(reverse('groups'))
    else:
        # initial form render
        return render(request, 'students/groups_add.html',
                        {'students': Student.objects.all().order_by('first_name')})


class GroupAddForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('groups_add_form')
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


class GroupAddView(CreateView):
    model = Group
    template_name = 'students/groups_form.html'
    form_class = GroupAddForm



    def get_success_url(self):
        messages.success(self.request, u'Групу успішно збережено!')
        return reverse('groups')


    def get_context_data(self, **kwargs):
        context = super(GroupAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання групи'
        return context



    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Додавання групи відмінено!')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupAddView, self).post(request,*args,**kwargs)



class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('groups_edit',kwargs={'pk': kwargs['instance'].id})
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


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_form.html'
    form_class = GroupUpdateForm



    def get_success_url(self):
        messages.success(self.request, u'Групу успішно збережено!')
        return reverse('groups')

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування групи'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Редагування групи відмінено!')

            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request,*args,**kwargs)




def groups_edit(request, gid):
    groups = Group.objects.filter(pk=gid)
    students = Student.objects.all()

    if len(groups) !=1:
        messages.error(request, 'Обраної групи не існує')
        return HttpResponseRedirect(reverse('groups'))
    else:
        if request.method == "POST":
            group = Group.objects.get(pk=gid)
            if request.POST.get('save_button') is not None:
                errors = {}
                group.notes = request.POST.get('notes', '').strip()
                title = request.POST.get('title', '').strip()
                if not title:
                    errors['title'] = u"Назва є обов'язковою."
                else:
                    groups = Group.objects.filter(title=title)
                    if len(groups) > 0 and title != group.title:
                        errors['title'] = u"Така група вже існує"
                    else:
                        group.title = title

                leader = request.POST.get('leader', "").strip()
                if leader:
                    student = Student.objects.filter(pk=int(leader))
                    if len(student) != 1:
                        errors['leader'] = u"Оберіть коректного студента"

                    elif student[0].student_group.id != group.id:
                        errors['leader'] = u"Студент не належить до цієї групи"
                    else:
                        group_leader = Group.objects.filter(leader=student)
                        # import pdb;pdb.set_trace()
                        if len(group_leader) != 0 and int(leader) != group.leader.id:
                            errors['leader'] = u"Даний студент є старростою іншої групи"
                        else:
                            group.leader = student[0]
                if errors:
                    messages.error(request,u'Виправте наступні помилки!')
                    return render(request, 'students/groups_edit_hand.html',
                                  {'students': students,'errors': errors,'group':group , 'pk':gid})
                else:
                    group.save()
                    messages.success(request, u'Групу успішно збереженно!')
                    return HttpResponseRedirect(reverse('groups'))

            elif request.POST.get('cancel_button') is not None:
                messages.warning(request, 'Редагування групи скасовано.')
                return HttpResponseRedirect(reverse('groups'))
            else:
                messages.error(request, 'Упс! Щось пішло не так. Повторіть спробу пізніше.')
                return HttpResponseRedirect(reverse('groups'))
        else:
            return render(request,'students/groups_edit_hand.html',{'pk': gid, 'group': groups[0],
                                                                 'students': students.order_by('first_name')})




class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Групу успішно видалено!' )
        return reverse('groups')

def groups_delete(request, gid):
    try:
        group = Group.objects.get(pk=gid)
    # import pdb;pdb.set_trace()
    except:
        messages.error(request, 'Даної групи не існує.')
        return HttpResponseRedirect(reverse('groups'))

    if request.method == "POST":

        if request.POST.get('confirm_button') is not None:
            group = Group.objects.get(pk=gid)
            gr_students = Student.objects.filter(student_group = group)
            exam = Exam.objects.filter(group = group)
            if len(gr_students) != 0:
                messages.error(request, 'В даній групі є студенти.')
                return HttpResponseRedirect(reverse('groups'))
            elif len(exam) != 0:
                ex = ''
                for item in exam:
                    ex = ex + " " + str(item) + ","
                messages.error(request, 'В даній групі є екзамени %s.' % ex.strip(","))
                return HttpResponseRedirect(reverse('groups'))
            else:
                group.delete()
                messages.success(request, "Успішно видалено: %s." % group)
            return HttpResponseRedirect(reverse('groups'))
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, "Видалення групи скасовано.")
            return HttpResponseRedirect(reverse('groups'))
        else:
            messages.error(request, "Упс! Щось пішло не так. Повторіть спробу пізніше.")
            return HttpResponseRedirect(reverse('groups'))
    else:
        return render(request,
                      'students/groups_delete_hand.html',{'group':group })
