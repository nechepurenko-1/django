# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.views.generic.edit import FormView


from studentsdb.settings import ADMIN_EMAIL

class ContactForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(ContactForm, self).__init__(*args,**kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')


        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'sol-cm-10'

        self.helper.add_input(Submit('send_button', u'Надіслати'))



    from_email = forms.EmailField(label=u'Ваша Емейл Адреса')
    subject = forms.CharField(label=u"Заголовок листа",max_length=128)
    message = forms.CharField(label=u"Текст повідомлення",widget=forms.Textarea)





class ContactView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_admin')


    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']

        try:
            send_mail(subject, message, from_email, [ADMIN_EMAIL])
        except Exception:
            messages.warning(self.request, u'Під час відправки листа відбулась неочікувана помилка.'
                                           u'Будь-ласка спробуйте пізніше')
        else:
            messages.success(self.request, u'Листа успішно відправлено!')

        return super(ContactView, self).form_valid(form)


# def contact_admin(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             from_email = form.cleaned_data['from_email']
#
#             try:
#                 send_mail(subject, message, from_email, [ADMIN_EMAIL])
#
#             except Exception:
#                 messages.error(request,u'Під час відправки листа виникла непердбачувана помилка.Спробуйте даною формою пізніше.')
#                 # message = u'Під час відправки листа виникла непердбачувана помилка.Спробуйте даною формою пізніше.'
#
#             else:
#                 messages.success(request, u'Повідомлення успішно надіслане!')
#                 # message = u'повідомлення успішно надіслане!'
#             return HttpResponseRedirect(reverse('contact_admin'))
#
#         else:
#             messages.warning(request,u'Будь-ласка, виправте наступні помилки!')
#             return render(request, 'contact_admin/form.html',{'form':form})
#
#
#     else:
#         form = ContactForm()
#
#
#     return render(request, 'contact_admin/form.html',{'form':form})
