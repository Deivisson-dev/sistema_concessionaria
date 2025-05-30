from django import forms
from .models import Venda
import datetime

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        exclude = ['deleted', 'deleted_at'] 
        widgets = {
            'data_venda': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_venda'].initial = datetime.date.today()
        
    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if valor <= 0:
            raise forms.ValidationError("O valor deve ser positivo")
        return valor