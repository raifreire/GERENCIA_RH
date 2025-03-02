from django import forms 
from .models import Colaborador, Contrato

class ColaboradorForm(forms.ModelForm):
    telefone = forms.CharField(widget=forms.TextInput(attrs={'minlength':'15', 'maxlength':'15','onkeyup':'handlePhone(event)'}))
    tel_auxiliar = forms.CharField(widget=forms.TextInput(attrs={'minlength':'15', 'maxlength':'15','onkeyup':'handlePhone(event)'}))
    
    data_nascimento = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    foto = forms.FileInput()
    
    class Meta:
        model = Colaborador
        fields = ['nome','cpf','data_nascimento','matricula',
                  'departamento','classificacao','data_entrada','data_saida',
                  'telefone','tel_auxiliar','email','foto',
                  'observacao'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['nome'].widget.attrs.update({'class':'form-control'})
        self.fields['cpf'].widget.attrs.update({'class':'form-control'})
        self.fields['data_nascimento'].widget.attrs.update({'class':'form-control'})
        self.fields['matricula'].widget.attrs.update({'class':'form-control'})
        self.fields['departamento'].widget.attrs.update({'class':'form-control'})
        self.fields['classificacao'].widget.attrs.update({'class':'form-control'})
        self.fields['data_entrada'].widget.attrs.update({'class':'form-control'})
        self.fields['data_saida'].widget.attrs.update({'class':'form-control'})
        self.fields['telefone'].widget.attrs.update({'class':'form-control'})
        self.fields['tel_auxiliar'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['foto'].widget.attrs.update({'class':'form-control'})        
        self.fields['observacao'].widget.attrs.update({'class':'form-control'})


class ContratoForm(forms.ModelForm):
    contrato = forms.FileField()
    data_inicio = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    data_termino = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
        
    class Meta:
        model = Contrato
        fields = ['num_contrato','data_inicio','data_termino','periodo','contrato','colaborador']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['num_contrato'].widget.attrs.update({'class':'form-control'})
        self.fields['data_inicio'].widget.attrs.update({'class':'form-control'})
        self.fields['data_termino'].widget.attrs.update({'class':'form-control'})
        self.fields['periodo'].widget.attrs.update({'class':'form-control'})
        self.fields['contrato'].widget.attrs.update({'class':'form-control'})
        self.fields['colaborador'].widget.attrs.update({'class':'form-control'})