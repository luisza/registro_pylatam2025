# encoding: utf-8

'''
Free as freedom will be 27/10/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.conf.urls import url, include
from proposal.views import proposals
from ecsl.charlas import Charlas

urlpatterns = [
    url(r'proposal/', include(proposals.get_urls(), namespace='speech')),
    url(r'charlas', Charlas.as_view(), name="list_charlas"),
]