'''
Created on 5 jun. 2017

@author: luis
'''
from django.views.generic.list import ListView
from proposal.models import SpeechSchedule
import datetime


class Charlas(ListView):
    models = SpeechSchedule
    order_by="start_time"
    
    def get_context_data(self, **kwargs):
        context =  ListView.get_context_data(self, **kwargs)
        
        dia_1_start = datetime.datetime(day=21, month=7, year=2017, hour=0, minute=0)
        dia_1_end = datetime.datetime(day=21, month=7, year=2017, hour=23, minute=59)

        dia_2_start = datetime.datetime(day=22, month=7, year=2017, hour=0, minute=0)
        dia_2_end = datetime.datetime(day=22, month=7, year=2017, hour=23, minute=59)
        
        charlas = {
            'dia1' : self.queryset.filter(
                start_time__gte=dia_1_start,
                start_time__lte=dia_1_end,
                ).order_by('start_time'),
            'dia2' : self.queryset.filter(
                start_time__gte=dia_2_start,
                start_time__lte=dia_2_end,
                ).order_by('start_time')            
            
            }
        
        
        
        return context