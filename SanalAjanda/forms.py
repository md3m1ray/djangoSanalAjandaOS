from django import forms
from .models import CustomUser


class MyForm(forms.Form):
    tarih = forms.DateField(label='Tarih Seç',
                            widget=forms.DateInput(attrs={'type': 'date', 'style': 'width: 120px;'}))
    not_metni = forms.CharField(max_length=250,
                                widget=forms.TextInput(attrs={'type': 'text', 'style': 'width: 100%;'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False


class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['automatic_notifications']
        labels = {'automatic_notifications': 'Otomatik Bildirim Tercihi'}

    def __init__(self, *args, **kwargs):
        super(NotificationPreferenceForm, self).__init__(*args, **kwargs)

        if self.instance:
            mevcut_bildirim = self.instance.automatic_notifications
            if mevcut_bildirim is not None:
                self.fields['automatic_notifications'].initial = mevcut_bildirim
