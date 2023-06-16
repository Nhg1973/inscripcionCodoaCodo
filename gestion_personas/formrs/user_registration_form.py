from django.contrib.auth.models import User
from django import forms
from gestion_personas.models import Alumno

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['foto', 'nombre', 'apellido', 'estudio', 'trabajo', 'pais', 'direccion', 'telefono', 'twitter', 'facebook', 'linkedin']
        widgets = {
            'estudio': forms.TextInput(attrs={'class': 'form-control'}),
            'trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
        }

    foto = forms.ImageField(required=False, initial='defaul.jpg')
    nombre = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')

        if not nombre and not apellido:
            raise forms.ValidationError('Debe ingresar al menos el nombre o apellido.')

