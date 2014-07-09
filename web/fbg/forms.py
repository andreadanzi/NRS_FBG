from django import forms
from fbg.models import NrsEnvironment
from django.contrib.admin import widgets

class FilterForm(forms.Form):
    env_choices = []
    env_list = NrsEnvironment.objects.all().order_by('-title')
    if env_list:
        for env in env_list: 
            env_choices.append((env.id,env.title))
    environment = forms.ChoiceField(label="Scegliere il sito",choices = env_choices)
    datetime_from = forms.DateTimeField(label="Limite inferiore",widget=widgets.AdminSplitDateTime())
    datetime_to = forms.DateTimeField(label="Limite superiore",widget=widgets.AdminSplitDateTime())
    view_option = forms.ChoiceField(label="Vista",choices = (('map','Mappa'),('serie','Serie')))
    aggregate_option = forms.ChoiceField(label="Elaborazione",choices = (('avg','Valore Medio'),('last','Ultimo Campione'),('first','Primo Campione'),('min','Valore Minimo'),('max','Valore Massimo')))
    interpolation_method = forms.ChoiceField(label=" ",choices = (('linear','Lineare'),('cubic','Cubica'),('nearest','Nearest')))
    class Media:
        css = {
            'all': ( 'layout.css',)
        }
