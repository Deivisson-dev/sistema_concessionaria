from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'data-mask': '000.000.000-00'})
        self.fields['telefone'].widget.attrs.update({'data-mask': '(00) 00000-0000'})

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if self.instance.pk: 
            if Cliente.objects.exclude(pk=self.instance.pk).filter(cpf=cpf).exists():
                raise forms.ValidationError("CPF já cadastrado para outro cliente")
        else:
            if Cliente.objects.filter(cpf=cpf).exists():
                raise forms.ValidationError("CPF já cadastrado")
        return cpf

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk:
            if Cliente.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError("E-mail já cadastrado para outro cliente")
        else:
            if Cliente.objects.filter(email=email).exists():
                raise forms.ValidationError("E-mail já cadastrado")
        return email