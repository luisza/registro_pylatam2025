# encoding: utf-8

'''
Free as freedom will be 27/10/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.conf.urls import url, include
from proposal.views import proposals
from django.urls import re_path

urlpatterns = [
    re_path(r'proposal/', include(proposals.get_urls(), namespace='speech')),
]