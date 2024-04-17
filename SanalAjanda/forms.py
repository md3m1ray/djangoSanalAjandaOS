from django import forms
from .models import CustomUser


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