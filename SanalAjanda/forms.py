from django import forms


class MyForm(forms.Form):
    tarih = forms.DateField(label='Tarih Seç',
                            widget=forms.DateInput(attrs={'type': 'date', 'style': 'width: 120px;'}))
    not_metni = forms.CharField(max_length=250,
                                widget=forms.TextInput(attrs={'type': 'text', 'style': 'width: 100%;'}))
