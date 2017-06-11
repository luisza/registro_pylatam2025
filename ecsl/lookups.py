'''
Created on 5 jun. 2017

@author: luis
'''

from ajax_select import register, LookupChannel
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from proposal.models import Speech

@register('users')
class TagsLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(username__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q)
            )

    def format_item_display(self, item):
        return "<span class='tag'>(%s) %s</span>" % (item.username, item.get_full_name())
    
    def format_match(self, obj):
        return obj.get_full_name()


@register('charlas')
class SpeechLookup(LookupChannel):

    model = Speech

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(title__icontains=q)|Q(user__username__icontains=q
            )|Q(user__first_name__icontains=q)|Q(user__last_name__icontains=q)
            )

    def format_item_display(self, item):
        return "<span class='tag'>(%s) %s</span>" % (item.title, item.user.get_full_name())
    
    def format_match(self, obj):
        return obj.title
