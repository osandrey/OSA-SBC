from django import forms
from .models import Citizen, Stage


class CreateCitizen(forms.ModelForm):
    firstname = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


    lastname = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


    email = forms.EmailField(max_length=100,
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    age = forms.IntegerField(min_value=21,
                             max_value=120,
                             required=True,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))

    note = forms.CharField(max_length=1200,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    # widjet filter type = unknown
    # Stage.objects.all(), -> if un authenticated or role = guest
    # add phone address to models
    # add app services
    #Foreign key services - clients
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Citizen
        fields = ['firstname', 'lastname', 'email', 'age', 'note', 'stage']