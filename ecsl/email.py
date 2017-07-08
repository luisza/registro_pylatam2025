'''
Created on 8 jul. 2017

@author: luis
'''
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def email_template_redirect(request, code):

    return redirect("admin:ecsl_inscriptions_changelist")
