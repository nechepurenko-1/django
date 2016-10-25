# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Exam(models.Model):
    '''Group Model'''

    class Meta(object):
        verbose_name = u"Екзамен"
        verbose_name_plural = u"Екзамени"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва предмету")

    date_exam = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата та час проведення",
        null=True)

    teacher =  models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач")

    group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.title, self.group.title, self.teacher)