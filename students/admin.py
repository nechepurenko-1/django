# -*- coding: utf-8 -*-
from django.contrib import admin
from .models.students import Student
from .models.groups import Group
from .models.exams import Exam
from django.core.urlresolvers import reverse
from django.forms import ModelForm,ValidationError



class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        groups = Group.objects.filter(leader = self.instance)
        if len(groups) >0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data['student_group']

class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        leader = self.cleaned_data['leader']
        if leader.student_group != self.instance:
            raise ValidationError(u"Студент навчається в іншій групі.", code='invalid')
        return self.cleaned_data['leader']



class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name','first_name','ticket','student_group']
    list_display_links = ['last_name','first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name','first_name','middle_name','ticket','notes']
    form = StudentFormAdmin
    def view_on_site(self, obj):
        return reverse('students_edit' , kwargs={'pk': obj.id})

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title','leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['title']
    list_per_page = 10
    search_fields = ['title','leader']
    form = GroupFormAdmin
    def view_on_site(self, obj):
        return reverse('groups_edit' , kwargs={'pk': obj.id})



# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
