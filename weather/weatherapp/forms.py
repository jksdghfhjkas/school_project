from django import forms
from . import models

class SitiesForm(forms.ModelForm):

    NameSity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-sity', 'placeholder':"Город"}))

    class Meta:
        model = models.Sities
        fields = ('NameSity',)

class DeleteSitiesForm(forms.Form):
    record = forms.ModelChoiceField(queryset=None, 
                                    empty_label="Выберете местность")
    
    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        if user: 
            self.fields['record'].queryset = models.Sities.objects.filter(user=user)











        
