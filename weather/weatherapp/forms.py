from django import forms
from . import models

class SitiesForm(forms.ModelForm):

    NameSity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-sity', 'placeholder':"Город"}))

    class Meta:
        model = models.Sities
        fields = ('NameSity',)








        
